from aiogram import Router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile


from src.api import UserClient
from src.constants.texts import QR_CODE_TEXT, ATTENDED_ACTIVITY, NO_VISITS
from src.middlewares.utils import parse_activities, get_emoji_for_activity
from src.models import TargetType

router = Router()

# Command level


@router.message(F.text == ATTENDED_ACTIVITY)
@router.message(Command("activities"))
async def cmd_attended_activity(message: Message, user_client: UserClient) -> None:
    user_activity_list = await user_client.get_user_visits(tg_id=message.chat.id)
    all_activities = await user_client.get_all_activities()
    sorted_activity = parse_activities(user_activity_list)
    message_text = ""
    activities = sorted_activity[TargetType.ACTIVITY]
    companies = sorted_activity[TargetType.COMPANY]
    if len(activities) > 0:
        message_text += f"<b>Посещенные активности:</b> [{len(user_activity_list)}/{len(all_activities)}]\n\n"
        for activity in activities:
            emoji = get_emoji_for_activity("ACTIVITY")
            message_text += f"{emoji} {activity.name}\n"
        message_text += "\n"

    if len(companies) > 0:
        message_text += "<b>Посещенные компании:</b>\n\n"
        for company in companies:
            emoji = get_emoji_for_activity("COMPANY")
            message_text += f"{emoji} {company.name}\n"
        message_text += "\n"

    if message_text == "":
        message_text = NO_VISITS

    await message.answer(
        text=message_text,
        parse_mode=ParseMode.HTML
    )
