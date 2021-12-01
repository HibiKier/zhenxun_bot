from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, Event
from utils.utils import get_message_text
from nonebot.typing import T_State
from .model import WordBank


async def check(bot: Bot, event: Event, state: T_State) -> bool:
    if isinstance(event, GroupMessageEvent):
        return bool(
            await WordBank.check(event.group_id, get_message_text(event.json()), event.is_tome())
        )
    return False
