import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

# from src.constants.messages import EXCEPTION_MESSAGE
# from src.middlewares.utils import get_user_id_from_update
# from src.models import Image


class ExceptionHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Update
        # user_id = await get_user_id_from_update(event)
        try:
            return await handler(event, data)
        except Exception as e:
            pass
            # chat_id = await get_user_id_from_update(event)
            # logging.error(f"Handling with error for user with id {user_id}", exc_info=e)
