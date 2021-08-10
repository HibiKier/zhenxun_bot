from nonebot import on_command
from .data_source import get_yiqing_data
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import get_message_text

__plugin_name__ = "疫情查询"
__plugin_usage__ = "查询疫情帮助:\n\t对我说 查询疫情 省份/城市，我会回复疫情的实时数据\n\t示例: 查询疫情 温州"


yiqing = on_command("疫情", aliases={"查询疫情", "疫情查询"}, priority=5, block=True)


@yiqing.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    result = await get_yiqing_data(msg)
    if result:
        await yiqing.send(result)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 查询疫情: {msg}"
        )
    else:
        await yiqing.send("查询失败!!!!", at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 查询疫情失败"
        )
