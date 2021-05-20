from .data_source import get_qqbot_chat_result, hello, no_result
from services.log import logger
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, PrivateMessageEvent
from util.utils import get_message_text, get_message_imgs
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser

__plugin_name__ = 'AI'


ai = on_message(rule=to_me(), priority=8)


@ai.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    if str(event.get_message()).find('CQ:xml') != -1:
        return
    # 打招呼
    if not msg and not imgs:
        await ai.finish(hello())
    img = imgs[0] if imgs else ''
    nickname = await FriendUser.get_friend_nickname(event.user_id)
    if not nickname:
        nickname = await FriendUser.get_user_name(event.user_id)
        if not nickname:
            nickname = "你"
    result = await get_qqbot_chat_result(msg, img, event.user_id, nickname)
    logger.info(f"USER {event.user_id} 问题：{msg}\n回答：{result}")
    if result:
        await ai.finish(result)
    else:
        await ai.finish(no_result())


@ai.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    # if await GroupRemind.get_status(event.group_id, 'ai'):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    # 打招呼
    if not msg and not imgs:
        await ai.finish(hello())
    img = imgs[0] if imgs else ''
    nickname = await GroupInfoUser.get_group_member_nickname(event.user_id, event.group_id)
    if not nickname:
        try:
            nickname = (await GroupInfoUser.select_member_info(event.user_id, event.group_id)).user_name
        except AttributeError:
            nickname = "你"
    result = await get_qqbot_chat_result(msg, img, event.user_id, nickname)
    logger.info(f"问题：{msg}\n回答：{result}")
    if result:
        await ai.finish(result)
    else:
        await ai.finish(no_result())

