from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.api import UserClient
from src.constants.texts import VOTE_SENT, VOTE_ERROR
from src.models import CreateVoteRequest, ErrorType

router = Router()


@router.callback_query(F.data.startswith("event|"))
async def ted(callback: CallbackQuery, user_client: UserClient) -> None:
    answers = list()
    buttons = callback.message.reply_markup.inline_keyboard
    for button in buttons:
        answers.append(button[0].text)

    params = callback.data.split("|")
    activity_id = int(params[1])
    index = int(params[2])

    result = await user_client.add_user_answer(
        activity_id=activity_id,
        request=CreateVoteRequest(
            userTgId=callback.message.chat.id,
            answer=answers[index]
        ))

    if not result:
        await callback.message.answer(
            text=VOTE_ERROR
        )

    else:
        await callback.answer(VOTE_SENT)

    await callback.message.delete()
