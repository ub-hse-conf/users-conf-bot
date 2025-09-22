from aiogram import F
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from src.api import UserClient
from src.constants.texts import PASS_CODE, CANCEL_BTN, PASS_CODE_WORD, WORD_SENT, PASS_CORRECT_WORD, \
    WRONG_SEND, WRONG_SEND_NO_VISIT
from src.middlewares.utils import get_cancel_inline_keyboard
from src.models import ErrorType
from src.models.keyword import Keyword

router = Router()


class TextInputStates(StatesGroup):
    waiting_for_text = State()


@router.message(F.text == PASS_CODE)
@router.message(Command("pass_code"))
async def workshop_word(message: Message, state: FSMContext) -> None:
    await state.set_state(TextInputStates.waiting_for_text)

    info_message = await message.answer(
        text=PASS_CODE_WORD,
        reply_markup=get_cancel_inline_keyboard()
    )

    await state.update_data(info_message_id=info_message.message_id)


@router.message(TextInputStates.waiting_for_text, F.text)
async def handle_text_input(message: Message, state: FSMContext, user_client: UserClient, bot: Bot) -> None:
    user_text = message.text.strip()

    await message.delete()
    data = await state.get_data()
    if data["info_message_id"]:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=data["info_message_id"],
        )

    result = await user_client.add_keyword(Keyword(
        tgId=message.chat.id,
        keyWord=user_text
    ))

    if result:
        if result.error_type == ErrorType.VISIT_NOT_FOUND:
            await message.answer(
                text=WRONG_SEND_NO_VISIT
            )

        elif result.error_type == ErrorType.VISIT_ALREADY_EXISTS:
            await message.answer(
                text=WRONG_SEND_NO_VISIT
            )

        else:
            await message.answer(
                text=WRONG_SEND
            )

    else:
        await message.answer(
            text=WORD_SENT
        )

    await state.clear()


@router.message(TextInputStates.waiting_for_text)
async def handle_non_text_input(message: Message):

    await message.answer(
        text=PASS_CORRECT_WORD,
        reply_markup=get_cancel_inline_keyboard()
    )


@router.callback_query(F.data == "cancel_text_input")
async def handle_cancel_text_input(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer(CANCEL_BTN)
