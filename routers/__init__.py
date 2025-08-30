__all__ = [
    "register_routes",
    "register_commands_info"
]

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from routers import start


def register_routes(dp: Dispatcher):
    dp.include_router(start.router)

async def register_commands_info(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Регистрация или изменение данных о себе'),
        ],
        scope=BotCommandScopeDefault()
    )