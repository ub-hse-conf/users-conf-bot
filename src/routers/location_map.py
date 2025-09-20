from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, FSInputFile

from src.constants.texts import ACTIVITY_MAP_BTN

router = Router()


@router.message(F.text == ACTIVITY_MAP_BTN)
@router.message(Command("map"))
async def cmd_map(message: Message) -> None:
    second_floor = FSInputFile("static/images/2_floor_schema.png")
    third_floor = FSInputFile("static/images/3_floor_schema.png")
    third_floor_cabinet = FSInputFile("static/images/3_floor_schema_312.png")
    await message.answer_photo(
        second_floor,
        caption="Схема 2 этажа"
    )
    await message.answer_photo(
        third_floor,
        caption="Схема 3 этажа"
    )
    await message.answer_photo(
        third_floor_cabinet,
        caption="Схема 3 этажа, 312 кабинет"
    )

