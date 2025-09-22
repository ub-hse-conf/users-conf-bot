import urllib

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
    TASK_GET_ERROR, CONTENT_TYPE_UNSUPPORTED, TASK_GENERAL_REQUIRE, CONTENT_SENT, TASK_REJECTED, \
    AFTER_MODERATION_APPROVED, AFTER_MODERATION_REJECTED, TASK_REJECTED_ALERT_TO_ADMIN, TASK_APPROVE_ALERT_TO_ADMIN, \
    WRONG_SEND_BE_REAL, TASK_ALREADY_SENT, TIME_IS_OVER_MY_SLOW_FRIEND
from src.constants.transcription import type_of_program_dict
from src.middlewares.utils import get_courses_keyboard, get_programs_keyboard, parse_name, send_error_message, \
    is_error_message, remove_error_message, get_registration_result_keyboard, parse_email, get_main_reply_keyboard, \
    send_company_info, get_task_info, get_cancel_keyboard, detect_content_type, show_preview_and_ask_confirmation, \
    get_file_id, send_to_commission, update_commission_message
from src.models import CreateUserRequest, ErrorType, TaskStatus, TaskType

router = Router()


class TaskStates(StatesGroup):
    waiting_answer = State()
    waiting_confirm = State()

# Callback level


@router.message(TaskStates.waiting_answer)
async def validate_answer(message: Message, state: FSMContext, user_client: UserClient, bot: Bot):
    user_data = await state.get_data()
    task_id = user_data['task_id']
    task = await user_client.get_user_task_by_id(tg_id=message.chat.id, task_id=task_id)

    content_type = detect_content_type(message)

    if content_type == "unknown":
        await message.answer(
            text=CONTENT_TYPE_UNSUPPORTED,
            reply_markup=get_cancel_keyboard(task_id)
        )
        return

    await state.set_state(TaskStates.waiting_confirm)
    file_id = get_file_id(message, content_type)
    text_content = message.text if content_type == "text" else None

    await state.update_data(
        content_type=content_type,
        file_id=file_id,
        text_content=text_content
    )

    data = await state.get_data()
    info_message_id = data.get("info_message_id")
    if info_message_id:
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=info_message_id,
            )
        except Exception as e:
            get_logger().error("State 'name' exception", exc_info=e)
    await message.delete()

    message_info = await show_preview_and_ask_confirmation(
        message=message,
        content_type=content_type,
        text_content=text_content,
        task=task,
        file_id=file_id
    )

    await state.update_data(preview_message_id=message_info.message_id)


@router.callback_query(F.data.startswith("be_real_start:"))
@router.callback_query(F.data.startswith("task:"))
async def be_real_start(callback: CallbackQuery, state: FSMContext, user_client: UserClient) -> None:

    if callback.data.startswith("be_real_start:"):
        task_id = int(callback.data.replace("be_real_start:", ""))
    else:
        task_id = int(callback.data.replace("task:", ""))

    task = await user_client.get_user_task_by_id(tg_id=callback.message.chat.id, task_id=task_id)
    task_info = await user_client.get_task_info(task_id)

    if task_info.type == TaskType.TEMP and task_info.status != TaskStatus.IN_PROCESS:
        await callback.answer(
            text=TIME_IS_OVER_MY_SLOW_FRIEND
        )
        await callback.message.delete()
        await state.clear()
        return

    if not task:
        await callback.answer(
            text=TASK_GET_ERROR,
            show_alert=True
        )
        return

    if "опрос" in task.description:
        text = get_task_info(task)
        await callback.message.answer(
            text=text,
            parse_mode=ParseMode.HTML
        )
        return

    await state.update_data(
        task_id=task.id,
        task_description=task.description,
    )

    await state.set_state(TaskStates.waiting_answer)


    text = get_task_info(task)
    await callback.message.delete()
    info_message = await callback.message.answer(
        text=text,
        reply_markup=get_cancel_keyboard(task.id),
        parse_mode=ParseMode.HTML
    )

    await state.update_data(info_message_id=info_message.message_id)


@router.callback_query(F.data.startswith("cancel_send:"))
@router.callback_query(F.data.startswith("cancel_task"))
async def be_real_cancel(callback: CallbackQuery, state: FSMContext, user_client: UserClient) -> None:
    callback_data = callback.data
    if ":" in callback_data:
        task_id = callback_data.split(":")[1]
    else:
        user_data = await state.get_data()
        task_id = user_data.get('task_id', 'неизвестно')

    await state.clear()
    await callback.message.delete()
    await callback.answer(TASK_REJECTED)


@router.callback_query(F.data.startswith("confirm_send:"))
async def handle_confirm_send(
        callback: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        user_client: UserClient
):
    data = await state.get_data()
    try:
        content_type = data['content_type']
    except Exception:
        await callback.answer(TASK_ALREADY_SENT)
        await callback.message.delete()
        return

    file_id = data['file_id']
    text_content = data['text_content']


    parts = callback.data.split(":")
    task_id = int(parts[1])

    task = await user_client.get_user_task_by_id(
        tg_id=callback.message.chat.id,
        task_id=task_id
    )

    user_account = await user_client.get_user_data(tg_id=callback.message.chat.id)

    task_info = await user_client.get_task_info(task_id)
    if task_info.type == TaskType.TEMP and task_info.status == TaskStatus.IN_PROCESS:
        await send_to_commission(
            file_id=file_id,
            content_type=content_type,
            text_content=text_content,
            task=task,
            user_account=user_account,
            user=callback.from_user,
            bot=bot
        )
    elif task_info.type == TaskType.PERMANENT:
        await send_to_commission(
            file_id=file_id,
            content_type=content_type,
            text_content=text_content,
            task=task,
            user_account=user_account,
            user=callback.from_user,
            bot=bot
        )
    else:
        await callback.message.answer(TIME_IS_OVER_MY_SLOW_FRIEND)
        await callback.message.delete()
        await state.clear()
        return

    await callback.message.answer(CONTENT_SENT)
    await callback.message.delete()

    await state.clear()
    await callback.answer(CONTENT_SENT)


@router.callback_query(F.data.startswith("change_content:"))
async def handle_change_content(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    await callback.message.delete()

    await state.set_state(TaskStates.waiting_answer)
    await callback.answer("🔄 Можно отправить новый контент")

    info_message = await callback.message.answer(
        text=TASK_GENERAL_REQUIRE,
        reply_markup=get_cancel_keyboard(task_id),
        parse_mode=ParseMode.HTML
    )

    await state.update_data(info_message_id=info_message.message_id)


@router.callback_query(F.data.startswith("approve_task:"))
async def handle_approve_task(
        callback: CallbackQuery,
        user_client: UserClient,
        bot: Bot):
    task_id = int(callback.data.split(":")[1])
    user_id = int(callback.data.split(":")[2])
    task = await user_client.get_user_task_by_id(tg_id=user_id, task_id=task_id)

    if callback.message.caption:
        new_caption = await update_commission_message(
            callback.message,
            "approved",
            callback.from_user,
            task_id
        )
        await callback.message.edit_caption(
            caption=new_caption,
            parse_mode="HTML",
            reply_markup=None
        )
    else:
        new_text = await update_commission_message(
            callback.message,
            "approved",
            callback.from_user,
            task_id
        )
        await callback.message.edit_text(
            text=new_text,
            parse_mode="HTML",
            reply_markup=None
        )


    result = await user_client.complete_task(task_id=task_id, tg_id=user_id)
    if isinstance(result, dict):
        if result:
            if result.error_type == ErrorType.COMPLETEDUSERTASK_ALREADY_EXISTS:
                await callback.message.answer(
                    text=WRONG_SEND_BE_REAL
                )

    await callback.answer(TASK_APPROVE_ALERT_TO_ADMIN)
    await bot.send_message(
        chat_id=user_id,
        text=AFTER_MODERATION_APPROVED.format(
            task_name=task.name
        )
    )


@router.callback_query(F.data.startswith("reject_task:"))
async def handle_reject_task(
        callback: CallbackQuery,
        user_client: UserClient,
        bot: Bot):
    task_id = int(callback.data.split(":")[1])
    user_id = int(callback.data.split(":")[2])
    task = await user_client.get_user_task_by_id(tg_id=user_id, task_id=task_id)

    if callback.message.caption:
        # Это медиа-сообщение с подписью
        new_caption = await update_commission_message(
            callback.message,
            "rejected",
            callback.from_user,
            task_id
        )
        await callback.message.edit_caption(
            caption=new_caption,
            parse_mode="HTML",
            reply_markup=None
        )
    else:
        # Это текстовое сообщение
        new_text = await update_commission_message(
            callback.message,
            "rejected",
            callback.from_user,
            task_id
        )
        await callback.message.edit_text(
            text=new_text,
            parse_mode="HTML",
            reply_markup=None
        )

    await callback.answer(TASK_REJECTED_ALERT_TO_ADMIN)

    await bot.send_message(
        chat_id=user_id,
        text=AFTER_MODERATION_REJECTED.format(
            task_name=task.name
        )
    )
