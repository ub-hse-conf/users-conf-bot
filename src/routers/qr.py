from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile


from src.api import UserClient
from src.constants.texts import QR_CODE_TEXT, SEND_QR

router = Router()

# Command level


@router.message(F.text == SEND_QR)
@router.message(Command("qr"))
async def cmd_qr(message: Message, user_client: UserClient) -> None:
    image_bytes = await user_client.get_user_qr(message.chat.id)

    input_file = BufferedInputFile(
        image_bytes,
        filename=f"qr_code_{message.chat.id}.png"
    )

    bot_message = await message.answer_photo(
        photo=input_file,
        caption=QR_CODE_TEXT,
    )


@router.message(Command("get_id"))
async def get_chat_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID: {chat_id}")
