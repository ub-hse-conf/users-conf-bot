from aiogram import Router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from src.api import UserClient
from src.constants.texts import TASK_LIST, ALL_TASKS_DONE, USER_TASKS_IN_PROGRESS
from src.middlewares.utils import get_task_keyboard
from src.models import UserTaskStatus

router = Router()


@router.message(F.text == TASK_LIST)
@router.message(Command("tasks"))
async def cmd_tasks(message: Message, user_client: UserClient) -> None:
    task_list = await user_client.get_user_tasks(message.chat.id)
    available_tasks = list(filter(lambda task: task.status != UserTaskStatus.DONE, task_list))
    if len(available_tasks) == 0:
        await message.answer(
            text=ALL_TASKS_DONE,
            parse_mode=ParseMode.HTML
        )
    else:
        keyboard = get_task_keyboard(available_tasks)
        await message.answer(
            text=USER_TASKS_IN_PROGRESS.format(count=len(available_tasks)),
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
