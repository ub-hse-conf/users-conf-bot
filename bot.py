import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from routers import register_routes, register_commands_info

load_dotenv()

TOKEN = getenv("BOT_TOKEN")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=TOKEN)
    await register_commands_info(bot)
    register_routes(dp)
    await dp.start_polling(bot)

