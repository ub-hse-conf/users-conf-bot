from typing import List

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
import re

from structlog import get_logger

from src.constants.texts import REGISTER_FAIL_BTN, REGISTER_OK_BTN, SCHEDULE_BTN, ACTIVITY_MAP_BTN, \
    NU_KAK_TAM_S_DENGAMI_BTN, SEND_QR, ATTENDED_ACTIVITY, COMPANY_VISIT, TO_SITE, TASK_LIST
from src.constants.transcription import type_of_program_dict
from src.models import VisitResult, TargetType
from src.models.company import Company


async def send_message(user_id: int, update: Update, text: str):
    await update.bot.send_message(chat_id=user_id, text=text)


async def get_user_id_from_update(update: Update) -> int:
    if update.message is not None:
        return update.message.from_user.id
    elif update.callback_query is not None:
        return update.callback_query.from_user.id


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
    for key in type_of_program_dict.keys():
        builder.add(InlineKeyboardButton(text=type_of_program_dict[key], callback_data=f"program_{key}"))
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
                KeyboardButton(text=SEND_QR),
                KeyboardButton(text=TASK_LIST)
            ],
            [
                KeyboardButton(text=SCHEDULE_BTN),
                KeyboardButton(text=ACTIVITY_MAP_BTN),
            ],
            [
                KeyboardButton(text=NU_KAK_TAM_S_DENGAMI_BTN),
                KeyboardButton(text=ATTENDED_ACTIVITY),
            ]
        ],
        resize_keyboard=True
    )


def parse_name(name: str) -> bool:
    try:
        return True if len(name.split(" ")) >= 2 else False
    except Exception as e:
        get_logger().error("middlewares/utils.py: parse_name: Name parsing error", exc_info=e)
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
            get_logger().error("middlewares/utils.py: remove_error_message", exc_info=e)


def parse_activities(visits: List[VisitResult]) -> dict:
    sorted_activities = {
        TargetType.COMPANY: [],
        TargetType.ACTIVITY: []
    }

    for visit in visits:
        if visit.targetType == TargetType.ACTIVITY:
            sorted_activities[TargetType.ACTIVITY].append(visit.target)
        else:
            sorted_activities[TargetType.COMPANY].append(visit.target)

    return sorted_activities


def get_emoji_for_activity(activity_type: str):
    if activity_type == "COMPANY":
        return "⭐️"
    elif activity_type == "WORKSHOP":
        return "📖"
    elif activity_type == "CONTEST":
        return "🏆"
    elif activity_type == "ACTIVITY":
        return "🏆"
    else:
        return "📖"


def is_https_url(url: str) -> bool:
    pattern = r'^https://'
    return bool(re.match(pattern, url, re.IGNORECASE))


async def send_company_info(message: Message, company: Company):
    text = COMPANY_VISIT.format(company=company.name) + "\n"
    if company.description is not None:
        text += company.description

    if company.siteUrl is not None and company.siteUrl != "" and is_https_url(company.siteUrl):
        btn = InlineKeyboardButton(url=company.siteUrl, text=TO_SITE)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn]])
        await message.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(
            text=text,
            parse_mode=ParseMode.HTML
        )

