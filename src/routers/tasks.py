from aiogram import Router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from src.api import UserClient
from src.constants.texts import TASK_LIST, ALL_TASKS_DONE, USER_TASKS_IN_PROGRESS, BE_REAL_ATTENTION
from src.middlewares.utils import get_task_keyboard
from src.models import UserTaskStatus
from src.models.task import UserTaskType

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
        text = USER_TASKS_IN_PROGRESS.format(count=len(available_tasks))
        is_be_real = False
        for task in available_tasks:
            if task.task_type == UserTaskType.BE_REAL:
                is_be_real = True

        if is_be_real:
            text += f"\n\n{BE_REAL_ATTENTION} "
        await message.answer(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
