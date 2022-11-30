from configs.config import Config
from models.chat_history import ChatHistory
from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from utils.depends import PlaintText

from ._rule import rule

__zx_plugin_name__ = "消息存储 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


Config.add_plugin_config(
    "chat_history", "FLAG", True, help_="是否开启消息自从存储", name="消息存储", default_value=True
)


chat_history = on_message(rule=rule, priority=1, block=False)


@chat_history.handle()
async def _(event: MessageEvent, msg: str = PlaintText()):
    if isinstance(event, GroupMessageEvent):
        await ChatHistory.add_chat_msg(
            event.user_id, event.group_id, str(event.get_message()), msg
        )
    else:
        await ChatHistory.add_chat_msg(event.user_id, None, str(event.get_message()), msg)


# @test.handle()
# async def _(event: MessageEvent):
#     print(await ChatHistory.get_user_msg(event.user_id, "private"))
#     print(await ChatHistory.get_user_msg_count(event.user_id, "private"))
#     print(await ChatHistory.get_user_msg(event.user_id, "group"))
#     print(await ChatHistory.get_user_msg_count(event.user_id, "group"))
#     print(await ChatHistory.get_group_msg(event.group_id))
#     print(await ChatHistory.get_group_msg_count(event.group_id))
