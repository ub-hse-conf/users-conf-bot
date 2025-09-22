import urllib
from asyncio import Task
from datetime import datetime
from typing import List
import pymorphy2

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update, User as AIOUser
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import Message
import re

from structlog import get_logger

from src.config import BE_REAL_GROUP_ID, ADDITIONAL_TASKS_GROUP_ID
from src.constants.texts import REGISTER_FAIL_BTN, REGISTER_OK_BTN, SCHEDULE_BTN, ACTIVITY_MAP_BTN, \
    NU_KAK_TAM_S_DENGAMI_BTN, SEND_QR, ATTENDED_ACTIVITY, COMPANY_VISIT, TO_SITE, TASK_LIST, activity, lecture, contest, \
    workshop, company, TASK_GENERAL_REQUIRE, CANCEL_BTN, SEND_CONFIRM_BTN, CHANGE_ANSWER, PREVIEW_TEXT, COMISSION_TEXT, \
    MODERATOR_TEXT, MODERATION_CONCLUSION_TEXT, PASS_CODE
from src.constants.transcription import type_of_program_dict
from src.models import VisitResult, TargetType, UserTask, User, UserTaskStatus
from src.models.company import Company
from src.models.task import UserTaskType


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
            ],
            [
                KeyboardButton(text=TASK_LIST),
                KeyboardButton(text=PASS_CODE),
                KeyboardButton(text=ATTENDED_ACTIVITY),
            ],
            [
                KeyboardButton(text=SCHEDULE_BTN),
                KeyboardButton(text=ACTIVITY_MAP_BTN),
                KeyboardButton(text=NU_KAK_TAM_S_DENGAMI_BTN),
            ],
        ],
        resize_keyboard=True
    )


def get_task_keyboard(task_list: list[UserTask]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for task in task_list:
        if task.task_type == UserTaskType.BE_REAL:
            builder.add(
                InlineKeyboardButton(
                    text="BE REAL!" + task.name,
                    callback_data=f"task:{task.id}"
                )
            )
        else:
            builder.add(
                InlineKeyboardButton(
                    text=task.name,
                    callback_data=f"task:{task.id}"
                )
            )


    builder.adjust(1)
    return builder.as_markup()


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


def get_task_info(task: UserTask) -> str:
    text = f"{task.name}\n\n{task.description}\n\n"
    text += TASK_GENERAL_REQUIRE
    return text


def get_cancel_keyboard(task_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=CANCEL_BTN,
            callback_data=f"cancel_task:{task_id}" if task_id else "cancel_task"
        ))
    return builder.as_markup(resize_keyboard=True)


def get_confirmation_keyboard(task_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=CHANGE_ANSWER,
            callback_data=f"change_content:{task_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=CANCEL_BTN,
            callback_data=f"cancel_send:{task_id}"
        ),
        InlineKeyboardButton(
            text=SEND_CONFIRM_BTN,
            callback_data=f"confirm_send:{task_id}"
        )
    )
    return builder.as_markup()


async def show_preview_and_ask_confirmation(message: Message,
                                            content_type: str,
                                            text_content: str,
                                            file_id: str,
                                            task: UserTask):

    keyboard = get_confirmation_keyboard(task.id)
    message_id: Message

    # Отправляем предпросмотр в зависимости от типа контента
    if content_type == "photo":
        message_id = await message.answer_photo(
            photo=file_id,
            caption=PREVIEW_TEXT.format(task_name=task.name, task_description=task.description),
            reply_markup=keyboard
        )

    elif content_type == "text":
        full_text = f"{PREVIEW_TEXT.format(task_name=task.name, task_description=task.description)}\n\n{text_content}"
        message_id = await message.answer(text=full_text, reply_markup=keyboard)

    elif content_type == "video":
        message_id = await message.answer_video(
            video=file_id,
            caption=PREVIEW_TEXT.format(task_name=task.name, task_description=task.description),
            reply_markup=keyboard
        )

    elif content_type == "video_note":
        text_msg = await message.answer(
            text=PREVIEW_TEXT.format(task_name=task.name, task_description=task.description),
            reply_markup=keyboard)
        message_id = await message.answer_video_note(video_note=file_id)

    elif content_type == "document":
        message_id = await message.answer_document(
            document=file_id,
            caption=PREVIEW_TEXT.format(task_name=task.name, task_description=task.description),
            reply_markup=keyboard
        )

    elif content_type == "audio":
        message_id = await message.answer_audio(
            audio=file_id,
            caption=PREVIEW_TEXT.format(task_name=task.name, task_description=task.description),
            reply_markup=keyboard
        )

    elif content_type == "voice":
        text_msg = await message.answer(
            text=PREVIEW_TEXT.format(task_name=task.name, task_description=task.description),
            reply_markup=keyboard)

        message_id = await message.answer_voice(voice=file_id)
    return message_id


def get_content_type_name(content_type: str) -> str:
    names = {
        "photo": "📸 Фотография",
        "text": "📝 Текст",
        "video": "🎥 Видео",
        "video_note": "⭕ Кружочек",
        "document": "📎 Документ",
        "audio": "🎵 Аудио",
        "voice": "🎤 Голосовое сообщение"
    }
    return names.get(content_type, "Неизвестно")


def detect_content_type(message: Message) -> str:
    if message.photo:
        return "photo"
    elif message.video:
        return "video"
    elif message.video_note:
        return "video_note"
    elif message.text:
        return "text"
    elif message.document:
        return "document"
    elif message.audio:
        return "audio"
    elif message.voice:
        return "voice"
    else:
        return "unknown"


def get_file_id(message: Message, content_type: str) -> str:
    if content_type == "photo":
        return message.photo[-1].file_id
    elif content_type == "video":
        return message.video.file_id
    elif content_type == "video_note":
        return message.video_note.file_id
    elif content_type == "document":
        return message.document.file_id
    elif content_type == "audio":
        return message.audio.file_id
    elif content_type == "voice":
        return message.voice.file_id
    return ""


def get_emoji_for_activity(activity_type: str):
    if activity_type == "COMPANY":
        return company
    elif activity_type == "WORKSHOP":
        return workshop
    elif activity_type == "CONTEST":
        return contest
    elif activity_type == "ACTIVITY":
        return activity
    else:
        return lecture


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


async def send_answer_to_be_real_group(message: Message):
    pass


async def send_answer_to_add_task_group(message: Message):
    pass


async def send_to_commission(file_id: str,
                             content_type: str,
                             text_content: str,
                             task: UserTask,
                             user_account: User,
                             user: AIOUser,
                             bot: Bot) -> Message:

    chat_id = BE_REAL_GROUP_ID if task.task_type == UserTaskType.BE_REAL else ADDITIONAL_TASKS_GROUP_ID

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="❌ Отклонить",
            callback_data=f"reject_task:{task.id}:{user.id}"
        ),
        InlineKeyboardButton(
            text="✅ Одобрить",
            callback_data=f"approve_task:{task.id}:{user.id}"
        )
    )

    caption = create_commission_caption(
        task=task,
        user_account=user_account,
        user=user,
        text_content=text_content
    )

    # Отправляем в зависимости от типа контента
    if content_type == "photo":
        return await bot.send_photo(
            chat_id=chat_id,
            photo=file_id,
            caption=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )

    elif content_type == "text":
        return await bot.send_message(
            chat_id=chat_id,
            text=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )

    elif content_type == "video":
        return await bot.send_video(
            chat_id=chat_id,
            video=file_id,
            caption=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )

    elif content_type == "video_note":
        text_msg = await bot.send_message(
            chat_id=chat_id,
            text=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )
        await bot.send_video_note(
            chat_id=chat_id,
            video_note=file_id
        )
        return text_msg

    elif content_type == "document":
        return await bot.send_document(
            chat_id=chat_id,
            document=file_id,
            caption=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )

    elif content_type == "audio":
        return await bot.send_audio(
            chat_id=chat_id,
            audio=file_id,
            caption=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )

    elif content_type == "voice":
        text_msg = await bot.send_message(
            chat_id=chat_id,
            text=caption,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )
        await bot.send_voice(
            chat_id=chat_id,
            voice=file_id,
            parse_mode=ParseMode.HTML
        )
        return text_msg


def create_commission_caption(
        text_content: str,
        task: UserTask,
        user_account: User,
        user: AIOUser
) -> str:

    caption = COMISSION_TEXT.format(
        task_name=task.name,
        task_description=task.description,
        username=user_account.fullName,
        link=f"{user.username if user.username else user.first_name}",
        date=f"{datetime.now().strftime('%d.%m.%Y %H:%M')}",
    )

    if text_content:
        caption += f"\n\n💬 Текст пользователя:\n\n <i><b>{text_content}</b></i>"

    return caption


async def update_commission_message(
        message: Message,
        decision: str,
        moderator: AIOUser,
        task_id: int) -> str:
    """Обновляет текст сообщения в комиссии с информацией о решении"""

    # Сохраняем оригинальный текст без кнопок
    original_text = message.text or message.caption or ""

    # Убираем HTML/Markdown разметку из оригинального текста если нужно
    clean_text = remove_markup(original_text)

    decision_texts = {
        "approved": "✅ ОДОБРЕНО",
        "rejected": "❌ ОТКЛОНЕНО"
    }

    moderator_info = MODERATOR_TEXT.format(
        moderator=moderator.full_name,
        username=moderator.username if moderator.username else moderator.first_name
    )

    new_text = MODERATION_CONCLUSION_TEXT.format(
        clean_text=clean_text,
        decision=decision_texts[decision],
        moderator_info=moderator_info,
        date=datetime.now().strftime('%d.%m.%Y %H:%M')
    )

    return new_text


def remove_markup(text: str) -> str:
    """Убирает HTML/Markdown разметку из текста"""
    # Простая очистка от основных тегов
    import re
    # Убираем HTML теги
    text = re.sub(r'<[^>]+>', '', text)
    # Убираем Markdown разметку
    text = re.sub(r'[*`~]', '', text)
    return text


def get_cancel_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=CANCEL_BTN,
        callback_data="cancel_text_input"
    ))
    return builder.as_markup()


def plural(n, forms):
    """
    forms: [форма_1, форма_2, форма_5]
    Например: ["задача", "задачи", "задач"]
    """
    n = abs(n) % 100
    if 11 <= n <= 19:
        return forms[2]

    n = n % 10
    if n == 1:
        return forms[0]
    elif 2 <= n <= 4:
        return forms[1]
    else:
        return forms[2]