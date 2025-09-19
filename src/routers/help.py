from aiogram import Router, Bot
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from structlog import get_logger
from io import BytesIO

from src.api import UserClient
from src.constants.texts import HELLO_TEXT, FIO_ERROR_TEXT, PROGRAM_CHANGE_TEXT, COURSE_CHANGE_TEXT, EMAIL_CHANGE_TEXT, \
    EMAIL_ERROR_TEXT, RESULT_TEXT, COMMAND_TEXT, COMPANY_VISIT, BAD_COMPANY_VISIT, QR_CODE_TEXT
from src.constants.transcription import type_of_program_dict
from src.middlewares.utils import get_courses_keyboard, get_programs_keyboard, parse_name, send_error_message, \
    is_error_message, remove_error_message, get_registration_result_keyboard, parse_email, get_main_reply_keyboard
from src.models import CreateUserRequest

router = Router()


class Form(StatesGroup):
    name = State()
    course = State()
    program = State()
    email = State()


# Command level


@router.message(Command("help"))
async def cmd_qr(message: Message, state: FSMContext, user_client: UserClient) -> None:
    bot_message = await message.answer(
        text=COMMAND_TEXT,
        reply_markup=ReplyKeyboardRemove()
    )
