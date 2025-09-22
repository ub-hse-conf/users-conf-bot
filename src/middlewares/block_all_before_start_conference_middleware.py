from aiogram import BaseMiddleware
from aiogram.types import Message
from structlog import get_logger

_while_list = [
    774471737,
    823397841,
    743056572,
    351259027,
    646596194
]

class ExcludedCommandsFilter:
    def __init__(self, excluded_commands: list):
        self.excluded_commands = excluded_commands

    async def __call__(self, message: Message) -> bool:
        if not message.text or not message.text.startswith('/'):
            return True

        command = message.text.split()[0][1:].split('@')[0]
        return command not in self.excluded_commands

class BlockAllBeforeStartConferenceMiddleware(BaseMiddleware):
    def __init__(self):
        self.excluded_commands = ['start']

    async def __call__(self, handler, event, data):
        if event.message is None:
            return await handler(event, data)

        message = event.message
        filter_check = ExcludedCommandsFilter(self.excluded_commands)
        should_check = await filter_check(message)

        if not should_check:
            return await handler(event, data)

        id = message.from_user.id

        if id not in _while_list:
            get_logger().info("Access for user not granted before conference start")
            await message.answer("Конференция еще не началась, ждем тебя завтра заряженным на конференции 😎")
            return

        get_logger().info("Access granted for user in white list")
        return await handler(event, data)
