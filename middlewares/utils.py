from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
import re

from api.hse_perm_helper import get_courses, get_programs
from constants.texts import REGISTER_FAIL_BTN, REGISTER_OK_BTN, SCHEDULE_BTN, ACTIVITY_MAP_BTN, NU_KAK_TAM_S_DENGAMI_BTN
from constants.transcription import type_of_program_dict


async def get_courses_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="1", callback_data="course_1"),
        InlineKeyboardButton(text="2", callback_data="course_2"),
        InlineKeyboardButton(text="3", callback_data="course_3"),
        InlineKeyboardButton(text="4", callback_data="course_4"),
        InlineKeyboardButton(text="5", callback_data="course_5")
    )

    builder.adjust(2)
    return builder.as_markup()


async def get_programs_keyboard(course: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Международный бакалавриат по бизнесу и экономике", callback_data="program_МБ"),
        InlineKeyboardButton(text="Разработка информационных систем для бизнеса", callback_data="program_РИС"),
        InlineKeyboardButton(text="История", callback_data="program_И"),
        InlineKeyboardButton(text="Иностранные языки", callback_data="program_ИЯ"),
        InlineKeyboardButton(text="Юриспруденция", callback_data="program_Ю"),
        InlineKeyboardButton(text="Управление бизнесом", callback_data="program_УБ"),
        InlineKeyboardButton(text="Государственное и муниципальное управление", callback_data="program_ГМУ"),
        InlineKeyboardButton(text="Финансовые стратегии и аналитика", callback_data="program_ФСА"),
        InlineKeyboardButton(text="ИТ-Юрист", callback_data="program_ИЮ"),
        InlineKeyboardButton(text="Бизнес аналитика", callback_data="program_БА"),
        InlineKeyboardButton(text="Дизайн", callback_data="program_Д"),
        InlineKeyboardButton(text="Управление развитием бизнеса", callback_data="program_УРБ"),
        InlineKeyboardButton(text="ИТ-Юрист", callback_data="program_ИЮ"),
    )

    builder.adjust(1)
    return builder.as_markup()


async def get_registration_result_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=REGISTER_FAIL_BTN, callback_data="register_False"),
        InlineKeyboardButton(text=REGISTER_OK_BTN, callback_data="register_True")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=SCHEDULE_BTN),
                KeyboardButton(text=ACTIVITY_MAP_BTN),
            ],
            [
                KeyboardButton(text=NU_KAK_TAM_S_DENGAMI_BTN)
            ]
        ],
        resize_keyboard=True
    )


def parse_name(name: str) -> bool:
    try:
        return True if len(name.split(" ")) >= 2 else False
    except Exception as e:
        print("middlewares/utils.py: parse_name: Name parsing error")
        return False


def parse_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return True if re.match(pattern, email) else False


async def send_error_message(state: FSMContext, user_message: Message, text: str) -> None:
    error_message = await user_message.answer(text=text)
    await state.update_data(error_message_id=error_message.message_id)


async def is_error_message(state: FSMContext):
    try:
        return True if ((await state.get_data())["error_message_id"]) is not None else False
    except Exception as e:
        return False


async def remove_error_message(state: FSMContext, message: Message, bot: Bot):
    data = await state.get_data()
    error_message_id = data.get("error_message_id")

    if error_message_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=error_message_id,
            )
        except Exception as e:
            print(f"middlewares/utils.py: remove_error_message: {e}")

