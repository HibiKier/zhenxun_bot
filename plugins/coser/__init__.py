import time
from typing import Any, Tuple

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.params import RegexGroup

from configs.config import Config
from configs.path_config import TEMP_PATH
from services.log import logger
from utils.http_utils import AsyncHttpx
from utils.manager import withdraw_message_manager
from utils.message_builder import image

__zx_plugin_name__ = "coser"
__plugin_usage__ = """
usage：
    三次元也不戳，嘿嘿嘿
    指令：
        ?N连cos/coser
        示例：cos
        示例：5连cos （单次请求张数小于9）
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
        "type": Tuple[int, int],
    },
}

coser = on_regex(r"^(\d)?连?(cos|COS|coser|括丝)$", priority=5, block=True)

# 纯cos，较慢:https://picture.yinux.workers.dev
# 比较杂，有福利姬，较快:https://api.jrsgslb.cn/cos/url.php?return=img
url = "https://picture.yinux.workers.dev"


@coser.handle()
async def _(event: MessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    num = reg_group[0] or 1
    for _ in range(int(num)):
        path = TEMP_PATH / f"cos_cc{int(time.time())}.jpeg"
        try:
            await AsyncHttpx.download_file(url, path)
            msg_id = await coser.send(image(path))
            withdraw_message_manager.withdraw_message(
                event,
                msg_id["message_id"],
                Config.get_config("coser", "WITHDRAW_COS_MESSAGE"),
            )
        except Exception as e:
            await coser.send("你cos给我看！")
            logger.error(f"coser 发送了未知错误 {type(e)}：{e}")
