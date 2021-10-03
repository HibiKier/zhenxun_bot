from .qiu_translation import qiu_qiu_word_translation, qiu_qiu_phrase_translation
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from nonebot import on_command
from utils.utils import get_message_text
from services.log import logger

__zx_plugin_name__ = "丘丘语翻译"
__plugin_usage__ = """
usage：
    异世界旅游小助手，仅支持丘丘语翻译至中文
    指令：
        丘丘语翻译/丘丘一下 [文本]
""".strip()
__plugin_des__ = "其实我听得懂丘丘人讲话"
__plugin_cmd__ = ["丘丘语翻译/丘丘一下 [文本]"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["丘丘语翻译", "丘丘一下"],
}

qiuqiu = on_command("丘丘语翻译", aliases={"丘丘一下", "丘丘翻译"}, priority=5, block=True)

suffix = "\n※ 只能从丘丘语翻译为中文，不能反向翻译\n" "※ 注意空格，不要加入任何标点符号\n" "※ 翻译数据来源于 米游社论坛"


@qiuqiu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    txt = get_message_text(event.json()).lower()
    if txt == "":
        return
    mes = qiu_qiu_phrase_translation(txt)
    if not mes:
        mes = qiu_qiu_word_translation(txt)
    mes += suffix
    # print(mes)
    await qiuqiu.send(mes, at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送丘丘翻译:" + txt
    )
