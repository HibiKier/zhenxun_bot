from typing import List

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.rule import to_me

from configs.config import NICKNAME, Config
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser
from services.log import logger
from utils.utils import get_message_img, get_message_text

from .data_source import get_chat_result, hello, no_result

__zx_plugin_name__ = "AI"
__plugin_usage__ = f"""
usage：
    与{NICKNAME}普普通通的对话吧！
"""
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "cmd": ["Ai", "ai", "AI", "aI"],
}
__plugin_configs__ = {
    "TL_KEY": {"value": [], "help": "图灵Key", "type": List[str]},
    "ALAPI_AI_CHECK": {
        "value": False,
        "help": "是否检测青云客骂娘回复",
        "default_value": False,
        "type": bool,
    },
    "TEXT_FILTER": {
        "value": ["鸡", "口交"],
        "help": "文本过滤器，将敏感词更改为*",
        "default_value": [],
        "type": List[str],
    },
}
Config.add_plugin_config(
    "alapi", "ALAPI_TOKEN", None, help_="在 https://admin.alapi.cn/user/login 登录后获取token"
)

ai = on_message(rule=to_me(), priority=998)


@ai.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = get_message_text(event.json())
    img = get_message_img(event.json())
    if "CQ:xml" in str(event.get_message()):
        return
    # 打招呼
    if (not msg and not img) or msg in [
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
    img = img[0] if img else ""
    if isinstance(event, GroupMessageEvent):
        nickname = await GroupInfoUser.get_user_nickname(event.user_id, event.group_id)
    else:
        nickname = await FriendUser.get_user_nickname(event.user_id)
    if not nickname:
        if isinstance(event, GroupMessageEvent):
            nickname = event.sender.card or event.sender.nickname
        else:
            nickname = event.sender.nickname
    result = await get_chat_result(msg, img, event.user_id, nickname)
    logger.info(
        f"USER {event.user_id} GROUP {event.group_id if isinstance(event, GroupMessageEvent) else ''} "
        f"问题：{msg} ---- 回答：{result}"
    )
    if result:
        result = str(result)
        for t in Config.get_config("ai", "TEXT_FILTER"):
            result = result.replace(t, "*")
        await ai.finish(Message(result))
    else:
        await ai.finish(no_result())
