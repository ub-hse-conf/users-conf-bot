from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

from src.constants.texts import HELP_MESSAGE


router = Router()


class Form(StatesGroup):
    name = State()
    course = State()
    program = State()
    email = State()


@router.message(Command("help"))
async def cmd_qr(message: Message) -> None:
    await message.answer(
        text=HELP_MESSAGE,
        parse_mode=ParseMode.HTML
    )
