#!/usr/bin/python3
# coding: utf-8
import re
import random
from difflib import SequenceMatcher
from nonebot.adapters.onebot.v11 import Message
from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.adapters.onebot.v11.message import MessageSegment
from .data import atri_text
from .data import V_PATH
from nonebot.params import CommandArg, ArgStr

__zx_plugin_name__ = "高性能萝卜子"
__plugin_usage__ = """
usage：
    Atri真可爱(发送一条关键词随机Atri语言
    指令：
        Atri/atri/亚托莉 [关键词]
""".strip()
__plugin_des__ = "高性能萝卜子"
__plugin_type__ = ("来点语音吧~",)
__plugin_cmd__ = [
    "Atri",
    "atri",
    "亚托莉",
]
__plugin_version__ = 0.1
__plugin_author__ = "AkashiCoin"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [
        "Atri",
        "atri",
        "亚托莉",
    ],
}
__plugin_block_limit__ = {"rst": "Atri正在讲话哦，请稍后..."}


atri = on_command("Atri", aliases={"atri", "亚托莉"}, priority=5, block=True)


@atri.handle()
async def _h(state: T_State, arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip()
    if args:
        state["words"] = args


@atri.got("words", prompt="想对萝卜子说什么话呢?")
async def _g(state: T_State, words: str = ArgStr("words")):
    words = str(state["words"])
    diff: dict[str, float] = {}
    for text in atri_text:
        r1 = SequenceMatcher(None, words, text["s"]).ratio()
        r2 = SequenceMatcher(None, words, text["s_f"]).ratio()
        r3 = SequenceMatcher(None, words, text["s_k"]).ratio()
        diff.update({text["o"]: r1 * r2 + r3})  # 完全瞎想的计算方式，没啥特殊的意义
    diff_sorted = dict(sorted(diff.items(), key=lambda item: item[1], reverse=True))
    voice = random.choice(
        [
            list(diff_sorted.keys())[0],
            list(diff_sorted.keys())[1],
            list(diff_sorted.keys())[2],
        ]
    )
    text = re.findall("(.*).mp3", voice)[0]
    await atri.send(MessageSegment.record(f"file:///{V_PATH}{voice}"))
    await atri.finish(text)
