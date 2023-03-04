from typing import Any, Tuple

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import RegexGroup
from nonebot.typing import T_State

from services.log import logger
from utils.depends import CheckConfig

from .data_source import CheckParam, language, translate_msg

__zx_plugin_name__ = "翻译"
__plugin_usage__ = """
usage：
    出国旅游小助手
    Regex: 翻译(form:.*?)?(to:.*?)? (.+)
    一般只需要设置to:，form:按照百度自动检测
    指令：
        翻译语种: (查看form与to可用值)
        示例:
        翻译 你好: 将中文翻译为英文
        翻译 Hello: 将英文翻译为中文
        翻译to:el 你好: 将"你好"翻译为希腊语
        翻译to:希腊语 你好: 允许form和to使用中文
        翻译form:zhto:jp 你好: 指定原语种并将"你好"翻译为日文
""".strip()
__plugin_des__ = "出国旅游好助手"
__plugin_cmd__ = ["翻译"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["翻译"],
}
__plugin_configs__ = {
    "APPID": {
        "value": None,
        "help": "百度翻译APPID",
        "type": str,
    },
    "SECRET_KEY": {
        "value": None,
        "help": "百度翻译秘钥",
        "type": str,
    },
}

translate = on_regex("^翻译(form:.*?)?(to:.*?)? (.+)", priority=5, block=True)

translate_language = on_regex("^翻译语种$", priority=5, block=True)


@translate_language.handle()
async def _(event: MessageEvent):
    s = ""
    for key, value in language.items():
        s += f"{key}: {value}，"
    await translate_language.send(s[:-1])
    logger.info(f"查看翻译语种", "翻译语种", event.user_id, getattr(event, "group_id", None))


@translate.handle(
    parameterless=[
        CheckConfig(config="APPID"),
        CheckConfig(config="SECRET_KEY"),
        CheckParam(),
    ]
)
async def _(
    event: MessageEvent, state: T_State, reg_group: Tuple[Any, ...] = RegexGroup()
):
    _, _, msg = reg_group
    await translate.send(await translate_msg(msg, state["form"], state["to"]))
    logger.info(f"翻译: {msg}", "翻译", event.user_id, getattr(event, "group_id", None))
