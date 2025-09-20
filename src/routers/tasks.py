from aiogram import Router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from src.constants.texts import TASK_LIST

router = Router()


@router.message(F.text == TASK_LIST)
@router.message(Command("tasks"))
async def cmd_qr(message: Message) -> None:
    await message.answer(
        text="Тут будут активные задания",
        parse_mode=ParseMode.HTML
    )
