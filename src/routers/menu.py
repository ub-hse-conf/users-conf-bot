from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.constants.texts import COMMAND_LIST_TEXT
from src.middlewares.utils import get_main_reply_keyboard

router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(
        text=COMMAND_LIST_TEXT,
        reply_markup=get_main_reply_keyboard()
    )
