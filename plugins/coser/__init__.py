from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from utils.message_builder import image
from services.log import logger
from utils.manager import withdraw_message_manager
from configs.config import Config

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
__plugin_configs__ = {
    "WITHDRAW_COS_MESSAGE": {
        "value": (0, 1),
        "help": "自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (0, 1),
    },
}

coser = on_regex("^(cos|COS|coser|括丝)$", priority=5, block=True)


url = "https://api.iyk0.com/cos"


@coser.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        msg_id = await coser.send(image(url))
        withdraw_message_manager.withdraw_message(
            event,
            msg_id["message_id"],
            Config.get_config("coser", "WITHDRAW_COS_MESSAGE"),
        )
    except Exception as e:
        await coser.send("你cos给我看！")
        logger.error(f"coser 发送了未知错误 {type(e)}：{e}")
