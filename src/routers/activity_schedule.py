from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from src.constants.texts import SCHEDULE_BTN

router = Router()


@router.message(F.text == SCHEDULE_BTN)
@router.message(Command("schedule"))
async def cmd_map(message: Message) -> None:
    schedule = FSInputFile("static/images/schedule.png")
    await message.answer_photo(
        photo=schedule
    )
