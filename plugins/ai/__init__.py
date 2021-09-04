from .data_source import get_chat_result, hello, no_result
from services.log import logger
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    PrivateMessageEvent,
    Message,
    MessageEvent,
)
from utils.utils import get_message_text, get_message_imgs
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser

__plugin_name__ = "AI [Hidden]"


ai = on_message(rule=to_me(), priority=8)


@ai.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    if "CQ:xml" in msg:
        return
    # 打招呼
    if (not msg and not imgs) or msg in [
        "你好啊",
        "你好",
        "在吗",
        "在不在",
        "您好",
        "您好啊",
        "你好",
        "在",
    ]:
        await ai.finish(hello())
    img = imgs[0] if imgs else ""
    if isinstance(event, PrivateMessageEvent):
        nickname = await FriendUser.get_friend_nickname(event.user_id)
    else:
        nickname = await GroupInfoUser.get_group_member_nickname(
            event.user_id, event.group_id
        )
    if not nickname:
        if isinstance(event, PrivateMessageEvent):
            nickname = event.sender.nickname
        else:
            nickname = event.sender.card if event.sender.card else event.sender.nickname
    result = await get_chat_result(msg, img, event.user_id, nickname)
    logger.info(
        f"USER {event.user_id} GROUP {event.group_id if not isinstance(event, PrivateMessageEvent) else ''} "
        f"问题：{msg} ---- 回答：{result}"
    )
    if result:
        await ai.finish(Message(result))
    else:
        await ai.finish(no_result())
