import asyncio
import uuid

from aiogram import Dispatcher

from src import custom_logging, api, routers, middlewares
from src.api import UserClient, endpoint
from src.bot import CustomBot
from src.config import BOT_TOKEN, BASE_URL, USERNAME_API, PASSWORD_API
from src.storage import create_bot_storage
from src.version import get_version


async def main():
    instance_id = str(uuid.uuid4())
    version = get_version()

    custom_logging.init_logging(instance_id, version)

    user_client = UserClient(base_url=BASE_URL, username=USERNAME_API, password=PASSWORD_API)

    storage = create_bot_storage()

    dp = Dispatcher(user_client=user_client, storage=storage)
    bot = CustomBot.create(BOT_TOKEN, storage)
    await routers.register_commands_info(bot)

    app = api.create_app_instance(bot)
    endpoint.register_endpoints(app)

    middlewares.register_middlewares(dp)
    routers.register_routes(dp)

    async with bot:
        await asyncio.gather(
            bot.start(dp),
            api.start_web(app, dp, bot)
        )
