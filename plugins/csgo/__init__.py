from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from utils.utils import get_message_text, is_number
from .data_source import get_csgola_data, get_5e_data
from services.log import logger


__zx_plugin_name__ = "cs国服/平台信息查找"
__plugin_usage__ = """
usage：
    快速查询csgo战绩和数据
    指令：
        cs国服查询 [steam主页个人id]
        5e查询 [5e战绩个人名称]
        示例：cs国服查询 23848238483
        示例：5e查询 poster
"""
__plugin_des__ = "什么？你也是rush B玩家？"
__plugin_cmd__ = ["cs国服查询 [steam主页个人id]", "5e查询 [5e战绩个人名称]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["csgo战绩查询", "cs国服查询", "5e查询"],
}

csgola = on_command("cs国服查询", priority=5, block=True)

csgo5e = on_command("5e查询", priority=5, block=True)


@csgola.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if "http" in msg:
        msg = msg[:-1] if msg[-1] == "/" else msg
        msg = msg.split("/")[-1]
    if not is_number(msg):
        await csgola.finish("Id必须为数字！", at_sender=True)
    await csgola.send("开始查找...")
    img, code = await get_csgola_data(int(msg))
    if code == 200:
        await csgola.send(img, at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 查询csgo国服战绩：{msg}"
        )
    else:
        await csgola.send(img, at_sender=True)


@csgo5e.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    await csgola.send("开始查找...")
    img, code = await get_5e_data(msg)
    if code == 200:
        await csgo5e.send(img, at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 查询csgo国服战绩：{msg}"
        )
    else:
        await csgo5e.send(img, at_sender=True)
