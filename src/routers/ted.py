from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery

from src.api import UserClient
from src.constants.texts import VOTE_SENT
from src.models import CreateVoteRequest

router = Router()


@router.callback_query(F.data.startswith("event|"))
async def ted(callback: CallbackQuery, user_client: UserClient) -> None:
    answers = list()
    buttons = callback.message.reply_markup.inline_keyboard
    for button in buttons:
        answers.append(button[0].text)

    params = callback.data.split("|")
    activity_id = int(params[0])
    index = int(params[1])

    await user_client.add_user_answer(
        activity_id=activity_id,
        request=CreateVoteRequest(
            userTgId=callback.message.from_user.id,
            answer=answers[index]
        ))

    await callback.answer(VOTE_SENT)
