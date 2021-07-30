from .qiu_translation import qiu_qiu_word_translation, qiu_qiu_phrase_translation
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from nonebot import on_command
from utils.utils import get_message_text
from services.log import logger

__plugin_name__ = "丘丘语翻译"

__plugin_usage__ = "用法：丘丘翻译 [消息]"

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
