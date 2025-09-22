from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from structlog import get_logger

from src.api import UserClient
from src.middlewares.utils import get_main_reply_keyboard

router = Router()

_melowetty_id = 646596194

@router.message(Command("start_conference"))
async def start_conference(message: Message, user_client: UserClient):
    if message.chat.id == _melowetty_id:
        get_logger().info("Handled start conference")
        token, users = await user_client.get_pageable_user_ids(0)
        get_logger().info(f"Got {len(users)} users for processing with next token {token}")
        await process_users(message.bot, users)
        while token != 0:
            token, users = await user_client.get_pageable_user_ids(token)
            get_logger().info(f"Got {len(users)} users for processing with next token {token}")
            await process_users(message.bot, users)

        get_logger().info(f"Finish start conference")



async def process_users(bot, users):
    for user in users:
        if user != _melowetty_id:
            get_logger().info(f"Skip user {user}")
            continue

        get_logger().info(f"Process user {user}")
        await bot.send_message(user, "*Доброе утро! ☀️*\n\n"
                               "До конференции остался один час, очень ждём тебя! А уже сейчас ты можешь изучить, что будет на конференции 😉",
                         reply_markup=get_main_reply_keyboard())