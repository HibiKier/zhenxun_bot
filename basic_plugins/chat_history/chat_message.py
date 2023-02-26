from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent

from configs.config import Config
from models.chat_history import ChatHistory
from services.log import logger
from utils.depends import PlaintText
from utils.utils import scheduler

from ._rule import rule

__zx_plugin_name__ = "消息存储 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


Config.add_plugin_config(
    "chat_history",
    "FLAG",
    True,
    help_="是否开启消息自从存储",
    name="消息存储",
    default_value=True,
    type=bool,
)


chat_history = on_message(rule=rule, priority=1, block=False)


TEMP_LIST = []


@chat_history.handle()
async def _(event: MessageEvent, msg: str = PlaintText()):
    group_id = None
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    TEMP_LIST.append(
        {
            "user_qq": event.user_id,
            "group_id": group_id,
            "text": str(event.get_message()),
            "plain_text": msg,
        }
    )


@scheduler.scheduled_job(
    "interval",
    minutes=1,
)
async def _():
    try:
        message_list = TEMP_LIST.copy()
        TEMP_LIST.clear()
        if message_list:
            model_list = [ChatHistory(**x) for x in message_list]
            await ChatHistory.bulk_create(model_list)
        logger.debug(f"批量添加聊天记录 {len(message_list)} 条", "定时任务")
    except Exception as e:
        logger.error(f"定时批量添加聊天记录", "定时任务", e=e)


# @test.handle()
# async def _(event: MessageEvent):
#     print(await ChatHistory.get_user_msg(event.user_id, "private"))
#     print(await ChatHistory.get_user_msg_count(event.user_id, "private"))
#     print(await ChatHistory.get_user_msg(event.user_id, "group"))
#     print(await ChatHistory.get_user_msg_count(event.user_id, "group"))
#     print(await ChatHistory.get_group_msg(event.group_id))
#     print(await ChatHistory.get_group_msg_count(event.group_id))
