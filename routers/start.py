from aiogram import Router, Bot
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from constants.transcription import type_of_program_dict
from middlewares.utils import get_courses_keyboard, get_programs_keyboard, parse_name, send_error_message, \
    is_error_message, remove_error_message, get_registration_result_keyboard, parse_email

router = Router()


class Form(StatesGroup):
    name = State()
    course = State()
    program = State()
    email = State()


# Command level


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    bot_message = await message.answer(
        "Здравствуйте! Давайте пройдем регистрацию. Введите фамилию, имя и отчество (при наличии) через пробел",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(info_message_id=bot_message.message_id)


# State level

@router.message(Form.name)
async def cmd_name(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        await message.delete()
    except:
        pass

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
            text="Пожалуйста, введите корректные фамилию, имя и отчество (при наличии)"
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
            print(f"State 'name' exception: {e}")

    new_message = await message.answer(
        "А теперь выберите Ваш курс:",
        reply_markup=keyboard
    )
    await state.update_data(info_message_id=new_message.message_id)


@router.message(Form.course)
async def cmd_course(message: Message, state: FSMContext) -> None:
    try:
        await message.delete()
    except:
        pass
    await state.update_data(course=message.text)


@router.message(Form.program)
async def cmd_program(message: Message, state: FSMContext) -> None:
    try:
        await message.delete()
    except:
        pass
    await state.update_data(program=message.text)


@router.message(Form.email)
async def cmd_email(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        await message.delete()
    except:
        pass

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
            text="Пожалуйста, введите корректный email адрес"
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
            print(f"State 'email' exception: {e}")

    keyboard = await get_registration_result_keyboard()

    await message.answer(
        text=f"Ваше ФИО: {data['name']}\n"
                              f"Ваш курс: {data['course']}\n"
                              f"Ваше направление: {type_of_program_dict[data['program']]}\n"
                              f"Ваш email: {data['email']}\n\n"
                              f"Все верно?",
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
    await callback.message.answer(f"Теперь направление:", reply_markup=keyboard)

    await state.set_state(Form.program)


@router.callback_query(F.data.startswith("program_"), Form.program)
async def process_program_choice(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_program = callback.data.replace("program_", "")
    await state.update_data(program=chosen_program)

    await callback.answer()

    await state.set_state(Form.email)
    await callback.message.delete()

    bot_message = await callback.message.answer(
        "Теперь введите Вашу почту:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(info_message_id=bot_message.message_id)


@router.callback_query(F.data.startswith("register_"))
async def register_end(callback: CallbackQuery, state: FSMContext) -> None:
    register_result = callback.data.replace("register_", "")
    await callback.message.delete()

    if register_result == "True":
        await callback.answer(
            text=f"Вы успешно зарегистрировались",
            show_alert=False
        )
        await state.clear()
    else:
        await state.clear()
        await cmd_start(callback.message, state)

