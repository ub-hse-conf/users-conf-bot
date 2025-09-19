from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from src.constants.texts import EXCEPTION_MESSAGE, UNREGISTERED_USER_EXCEPTION
from src.exception import ServerErrorException
from structlog import get_logger

from src.middlewares.utils import get_user_id_from_update, send_message
from src.models import ErrorType


class ExceptionHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Update
        try:
            return await handler(event, data)
        except Exception as e:
            get_logger().exception("Error when handling update", exc_info=e)
            if isinstance(e, ServerErrorException):
                e: ServerErrorException
                if e.error.error_type == ErrorType.USER_NOT_FOUND:
                    user_id = await get_user_id_from_update(event)
                    await send_message(user_id, event, UNREGISTERED_USER_EXCEPTION)
                    return

            chat_id = await get_user_id_from_update(event)
            try:
                await event.bot.send_message(chat_id=chat_id, text=EXCEPTION_MESSAGE.format(event.update_id))
            except Exception as e:
                get_logger().exception("Error when sending exception message", exc_info=e)
