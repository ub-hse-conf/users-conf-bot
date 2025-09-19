__all__ = [
    "register_routes",
    "register_commands_info"
]

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from src.routers import start, qr, menu, help


def register_routes(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(qr.router)
    dp.include_router(menu.router)
    dp.include_router(help.router)


async def register_commands_info(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Регистрация или изменение данных о себе'),
            BotCommand(command='help', description='Получить список команд'),
            BotCommand(command='menu', description='Получить меню с кнопками'),
            BotCommand(command='qr', description='Получить свой qr-код'),
        ],
        scope=BotCommandScopeDefault()
    )
