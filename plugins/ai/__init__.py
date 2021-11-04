from nonebot import on_message
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
)
from nonebot.rule import to_me
from nonebot.typing import T_State

from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser
from services.log import logger
from utils.utils import get_message_text, get_message_imgs
from .data_source import get_chat_result, hello, no_result
from configs.config import NICKNAME, Config

__zx_plugin_name__ = "AI"
__plugin_usage__ = f"""
usage：
    与{NICKNAME}普普通通的对话吧！
"""
__plugin_version__ = 0.1
__plugin_author__ = 'HibiKier'
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["Ai", "ai", "AI", "aI"],
}
__plugin_configs__ = {
    "TL_KEY": {
        "value": [],
        "help": "图灵Key"
    },
    "ALAPI_AI_CHECK": {
        "value": False,
        "help": "是否检测青云客骂娘回复",
        "default_value": False
    }
}
Config.add_plugin_config(
    "alapi",
    "ALAPI_TOKEN",
    None,
    help_="在https://admin.alapi.cn/user/login登录后获取token"
)

ai = on_message(rule=to_me(), priority=8)


@ai.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    if "CQ:xml" in str(event.get_message()):
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
    if isinstance(event, GroupMessageEvent):
        nickname = await GroupInfoUser.get_group_member_nickname(
            event.user_id, event.group_id
        )
    else:
        nickname = await FriendUser.get_friend_nickname(event.user_id)
    if not nickname:
        if isinstance(event, GroupMessageEvent):
            nickname = event.sender.card if event.sender.card else event.sender.nickname
        else:
            nickname = event.sender.nickname
    result = await get_chat_result(msg, img, event.user_id, nickname)
    logger.info(
        f"USER {event.user_id} GROUP {event.group_id if isinstance(event, GroupMessageEvent) else ''} "
        f"问题：{msg} ---- 回答：{result}"
    )
    if result:
        await ai.finish(Message(result))
    else:
        await ai.finish(no_result())
