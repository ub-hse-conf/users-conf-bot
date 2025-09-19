import asyncio

import structlog
from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import Application, AppRunner, TCPSite

from src.api.client import UserClient
from src.config import WEBHOOK_PATH, WORKING_MODE
from src.models import WorkingMode

__all__ = [
    "UserClient",
]

logger = structlog.get_logger(__name__)


async def start_web(app: Application, dp: Dispatcher, bot):
    if WORKING_MODE == WorkingMode.WEBHOOK:
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot
        )

        webhook_requests_handler.register(app, path=WEBHOOK_PATH)

        setup_application(app, dp, bot=bot)
        logger.info("Bot has added webhook to webserver")

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, '0.0.0.0', 8081)
    await site.start()
    logger.info("Web server successfully started at port 8081")
    await asyncio.Future()


def create_app_instance(bot) -> Application:
    app = Application()
    app['bot'] = bot

    return app