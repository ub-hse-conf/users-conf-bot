__all__ = [
    "register_middlewares",
]

from aiogram import Dispatcher

from src.middlewares.block_all_before_start_conference_middleware import BlockAllBeforeStartConferenceMiddleware
from src.middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from src.middlewares.tracing_middleware import TracingMiddleware

def register_middlewares(dp: Dispatcher):
    dp.update.middleware.register(TracingMiddleware())
    dp.update.middleware.register(BlockAllBeforeStartConferenceMiddleware())
    dp.update.middleware.register(ExceptionHandlerMiddleware())