from typing import Any

from structlog import get_logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import WORKING_MODE, WEBHOOK_URL, WEBHOOK_PATH
from src.models import WorkingMode
from src.storage import BaseStorage


class CustomBot(Bot):
    logger: Any

    @staticmethod
    def create(token: str, storage: BaseStorage) -> Bot:
        return CustomBot(
            token=token,
            storage=storage,
            default=DefaultBotProperties(parse_mode="Markdown"),
        )

    def __init__(
            self,
            token,
            *args,
            **kwargs,
    ):
        super().__init__(token, *args, **kwargs)
        self.logger = get_logger(__name__)

    async def start(self, dp: Dispatcher):
        if WORKING_MODE == WorkingMode.LONG_POLLING:
            self.logger.info("Bot has started pulling")
            await dp.start_polling(self)
        else:
            if not WEBHOOK_URL:
                raise RuntimeError("WEBHOOK_URL must be set")

            webhook_info = await self.get_webhook_info()

            if webhook_info.url != WEBHOOK_URL + WEBHOOK_PATH:
                await self.delete_webhook()

                await self.set_webhook(
                    url=WEBHOOK_URL + WEBHOOK_PATH,
                    drop_pending_updates=False
                )
                self.logger.info("Webhook URL changed to %s", WEBHOOK_URL + WEBHOOK_PATH)

            self.logger.info("Webhook linked to bot")