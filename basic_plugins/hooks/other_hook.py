from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.typing import T_State
from ._utils import status_message_manager
from utils.image_utils import text2image
from typing import Dict, Any
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    PrivateMessageEvent,
    GroupMessageEvent,
)
import re


# 为什么AI会自己和自己聊天
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: PrivateMessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if event.user_id == int(bot.self_id):
        raise IgnoredException("为什么AI会自己和自己聊天")


# 有命令就别说话了
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if matcher.type == "message" and matcher.plugin_name == "ai":
        if (
            isinstance(event, GroupMessageEvent)
            and not status_message_manager.check(event.group_id)
        ):
            status_message_manager.delete(event.group_id)
            raise IgnoredException("有命令就别说话了")
        elif (
            isinstance(event, PrivateMessageEvent)
            and not status_message_manager.check(event.user_id)
        ):
            status_message_manager.delete(event.user_id)
            raise IgnoredException("有命令就别说话了")

# @Bot.on_calling_api
# async def handle_api_call(bot: Bot, api: str, data: Dict[str, Any]):
#     if api in ["send_msg", "send_group_msg", "send_private_msg"]:
#         msg = str(data["message"])
#         if (r := re.search("\[\[To_Img\|?(.*?)]]", msg)) or (r := re.search("&#91;&#91;To_Img\|?(.*?)&#91;&#91;")):



