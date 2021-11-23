from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from utils.message_builder import image
from services.log import logger

__zx_plugin_name__ = "coser"
__plugin_usage__ = """
usage：
    三次元也不戳，嘿嘿嘿
    指令：
        cos/coser
""".strip()
__plugin_des__ = "三次元也不戳，嘿嘿嘿"
__plugin_cmd__ = ["cos/coser"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["cos", "coser", "括丝", "COS", "Cos", "cOS", "coS"],
}

coser = on_command(
    "cos", aliases={"coser", "括丝", "COS", "Cos", "cOS", "coS"}, priority=5, block=True
)


url = "http://iw233.cn/API/cos.php"


@coser.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        await coser.send(image(url))
    except Exception as e:
        await coser.send("你cos给我看！")
        logger.error(f"coser 发送了未知错误 {type(e)}：{e}")
