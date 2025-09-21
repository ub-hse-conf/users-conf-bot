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



# @router.callback_query(F.data.startswith("register_"))
# async def register_end(callback: CallbackQuery, state: FSMContext, user_client: UserClient) -> None:
#     register_result = callback.data.replace("register_", "")
#     await callback.message.delete()
#
#     if register_result == "True":
#         data = await state.get_data()
#         await user_client.create_user(request=CreateUserRequest(
#             course=data["course"],
#             fullName=data["name"],
#             email=data["email"],
#             program=data["program"],
#             tgId=callback.message.chat.id
#         ))
#         await callback.answer(
#             text=RESULT_TEXT.format(
#                 fio=data["name"],
#                 email=data["email"],
#                 course=data["course"],
#                 program=data["program"]
#             ),
#             show_alert=False
#         )
#         await state.clear()
#         await callback.message.answer(
#             text=COMMAND_LIST_TEXT,
#             reply_markup=get_main_reply_keyboard()
#         )
#
#     else:
#         await state.clear()
#         await cmd_start(callback.message, state)

