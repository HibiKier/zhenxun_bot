from nonebot import on_command
from .data_source import get_yiqing_data, get_city_and_province_list
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import get_message_text
from configs.config import NICKNAME


__zx_plugin_name__ = "疫情查询"
__plugin_usage__ = """
usage：
    全国疫情查询
    指令：
        疫情 中国
        疫情 [省份/城市]
    * 当省份与城市重名时，可在后添加 "市" 或 "省" *
    示例：疫情 吉林   <- [省]
    示例：疫情 吉林市  <- [市]
""".strip()
__plugin_des__ = "实时疫情数据查询"
__plugin_cmd__ = ["疫情 [省份/城市]", "疫情 中国"]
__plugin_type__ = ('一些工具',)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查询疫情", "疫情", "疫情查询"],
}


yiqing = on_command("疫情", aliases={"查询疫情", "疫情查询"}, priority=5, block=True)


@yiqing.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    city_and_province_list = get_city_and_province_list()
    if msg:
        if msg in city_and_province_list or msg[:-1] in city_and_province_list:
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
        else:
            await yiqing.send(f"{NICKNAME}没有查到{msg}的疫情查询...")
