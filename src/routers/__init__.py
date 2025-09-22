__all__ = [
    "register_routes",
    "register_commands_info"
]

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from src.routers import (start,
                         qr,
                         menu,
                         help,
                         attended_activity,
                         status, tasks,
                         location_map,
                         activity_schedule,
                         bereal,
                         ted,
                         workshop_word, conference_start_mailing)


def register_routes(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(qr.router)
    dp.include_router(menu.router)
    dp.include_router(help.router)
    dp.include_router(attended_activity.router)
    dp.include_router(status.router)
    dp.include_router(tasks.router)
    dp.include_router(location_map.router)
    dp.include_router(activity_schedule.router)
    dp.include_router(bereal.router)
    dp.include_router(ted.router)
    dp.include_router(workshop_word.router)
    dp.include_router(conference_start_mailing.router)


async def register_commands_info(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command='help', description='Помощь с конференцией'),
            BotCommand(command='menu', description='Получить меню с кнопками'),
            BotCommand(command='qr', description='Получить свой qr-код'),
            BotCommand(command='activities', description='Мои активности'),
            BotCommand(command='gifts', description='Как получить подарки'),
            BotCommand(command='tasks', description='Мои задания'),
            BotCommand(command='schedule', description='Расписание активностей'),
            BotCommand(command='map', description='Карта активностей'),
        ],
        scope=BotCommandScopeDefault()
    )
