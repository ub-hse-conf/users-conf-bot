import asyncio
import uuid
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

import custom_logging
from api.client import UserClient
from routers import register_routes, register_commands_info

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
BASE_URL = getenv("BASE_URL")
LOGIN_API = getenv("LOGIN_API")
PASSWORD_API = getenv("PASSWORD_API")


async def main():
    instance_id = str(uuid.uuid4())
    custom_logging.init_logging(instance_id)
    user_client = UserClient(base_url=BASE_URL, username=LOGIN_API, password=PASSWORD_API)

    dp = Dispatcher()
    bot = Bot(token=TOKEN)
    await register_commands_info(bot)
    register_routes(dp)
    await dp.start_polling(bot)

