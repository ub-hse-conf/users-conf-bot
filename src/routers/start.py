from aiogram import Router, Bot
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from structlog import get_logger

from src.api import UserClient
from src.constants.texts import HELLO_TEXT, FIO_ERROR_TEXT, PROGRAM_CHANGE_TEXT, COURSE_CHANGE_TEXT, EMAIL_CHANGE_TEXT, \
    EMAIL_ERROR_TEXT, RESULT_TEXT, COMMAND_LIST_TEXT, COMPANY_VISIT, BAD_COMPANY_VISIT, USER_ALREADY_EXISTS_TEXT, \
    GIFTS_MESSAGE, HELP_MESSAGE
from src.constants.transcription import type_of_program_dict
from src.middlewares.utils import get_courses_keyboard, get_programs_keyboard, parse_name, send_error_message, \
    is_error_message, remove_error_message, get_registration_result_keyboard, parse_email, get_main_reply_keyboard, \
    send_company_info
from src.models import CreateUserRequest

router = Router()


class Form(StatesGroup):
    name = State()
    course = State()
    program = State()
    email = State()


# Command level


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, user_client: UserClient) -> None:
    if len(message.text.split()) > 1:
        raw_params = message.text.split()[1]
        company = await user_client.visit_company(message.chat.id, raw_params)
        if company:
            companyInfo = await user_client.get_company_info(company_id=company.target.id)
            await send_company_info(message, companyInfo)
        else:
            await message.answer(BAD_COMPANY_VISIT)
        return

    result = await user_client.exists_user(tg_id=message.chat.id)
    if result is True:
        bot_message = await message.answer(
            text=USER_ALREADY_EXISTS_TEXT,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await state.set_state(Form.name)
        bot_message = await message.answer(
            text=HELLO_TEXT,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(info_message_id=bot_message.message_id)


# State level

@router.message(Form.name)
async def cmd_name(message: Message, state: FSMContext, bot: Bot) -> None:

    if await is_error_message(state):
        await remove_error_message(
            state=state,
            bot=bot,
            message=message
        )

    if not parse_name(message.text):
        await send_error_message(
            user_message=message,
            state=state,
            text=FIO_ERROR_TEXT
        )
        return

    await state.update_data(name=message.text)

    data = await state.get_data()
    info_message_id = data.get("info_message_id")
    keyboard = await get_courses_keyboard()
    await state.set_state(Form.course)

    if info_message_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=info_message_id,
            )
        except Exception as e:
            get_logger().error("State 'name' exception", exc_info=e)

    new_message = await message.answer(
        text=COURSE_CHANGE_TEXT,
        reply_markup=keyboard
    )
    await state.update_data(info_message_id=new_message.message_id)


@router.message(Form.course)
async def cmd_course(message: Message, state: FSMContext) -> None:
    await state.update_data(course=message.text)


@router.message(Form.program)
async def cmd_program(message: Message, state: FSMContext) -> None:
    await state.update_data(program=message.text)


@router.message(Form.email)
async def cmd_email(message: Message, state: FSMContext, bot: Bot) -> None:

    if await is_error_message(state):
        await remove_error_message(
            state=state,
            bot=bot,
            message=message
        )

    if not parse_email(message.text):
        await send_error_message(
            user_message=message,
            state=state,
            text=EMAIL_ERROR_TEXT
        )
        return

    await state.update_data(email=message.text)
    data = await state.get_data()
    info_message_id = data.get("info_message_id")
    if info_message_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=info_message_id,
            )
        except Exception as e:
            get_logger().error("State 'email' exception", exc_info=e)

    keyboard = await get_registration_result_keyboard()

    await message.answer(
        text=RESULT_TEXT.format(
            fio=data["name"],
            email=data["email"],
            course=data["course"],
            program=type_of_program_dict[data["program"]]
        ),
        reply_markup=keyboard
    ),

    await state.set_state(None)


# Callback level

@router.callback_query(F.data.startswith("course_"), Form.course)
async def process_course_choice(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_course = int(callback.data.replace("course_", ""))
    await state.update_data(course=chosen_course)

    await callback.answer()

    keyboard = await get_programs_keyboard(chosen_course)
    await callback.message.delete()
    await callback.message.answer(text=PROGRAM_CHANGE_TEXT, reply_markup=keyboard)

    await state.set_state(Form.program)


@router.callback_query(F.data.startswith("program_"), Form.program)
async def process_program_choice(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_program = callback.data.replace("program_", "")
    await state.update_data(program=chosen_program)

    await callback.answer()

    await state.set_state(Form.email)
    await callback.message.delete()

    bot_message = await callback.message.answer(
        text=EMAIL_CHANGE_TEXT,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(info_message_id=bot_message.message_id)


@router.callback_query(F.data.startswith("register_"))
async def register_end(callback: CallbackQuery, state: FSMContext, user_client: UserClient) -> None:
    register_result = callback.data.replace("register_", "")
    await callback.message.delete()

    if register_result == "True":
        data = await state.get_data()
        await user_client.create_user(request=CreateUserRequest(
            course=data["course"],
            fullName=data["name"],
            email=data["email"],
            program=data["program"],
            tgId=callback.message.chat.id
        ))
        await callback.answer(
            text=RESULT_TEXT.format(
                fio=data["name"],
                email=data["email"],
                course=data["course"],
                program=data["program"]
            ),
            show_alert=False
        )
        await state.clear()

        await callback.message.answer(
            text=COMMAND_LIST_TEXT,
            reply_markup=get_main_reply_keyboard(),
            parse_mode=ParseMode.HTML
        )
        await callback.message.answer(
            text=GIFTS_MESSAGE,
            parse_mode=ParseMode.HTML
        )
        await callback.message.answer(
            text=HELP_MESSAGE,
            parse_mode=ParseMode.HTML
        )

    else:
        await state.clear()
        await cmd_start(callback.message, state, user_client)
