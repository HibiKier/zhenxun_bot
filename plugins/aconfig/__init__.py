import random
from nonebot import on_keyword
import os
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from utils.utils import FreqLimiter
from configs.config import NICKNAME


__plugin_name__ = "基本设置 [Hidden]"
__plugin_usage__ = "用法： 无"


_flmt = FreqLimiter(300)


config_playgame = on_keyword({"打游戏"}, permission=GROUP, priority=1, block=True)


@config_playgame.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not _flmt.check(event.group_id):
        return
    _flmt.start_cd(event.group_id)
    await config_playgame.finish(
        image(random.choice(os.listdir(IMAGE_PATH + "dayouxi/")), "dayouxi")
    )


self_introduction = on_command(
    "自我介绍", aliases={"介绍", "你是谁", "你叫什么"}, rule=to_me(), priority=5, block=True
)


@self_introduction.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if NICKNAME.find('真寻') != -1:
        result = (
            "我叫绪山真寻\n"
            "你们可以叫我真寻，小真寻，哪怕你们叫我小寻子我也能接受！\n"
            "年龄的话我还是个**岁初中生(至少现在是)\n"
            "身高保密！！！(也就比美波里(姐姐..(妹妹))矮一点)\n"
            "我生日是在3月6号, 能记住的话我会很高兴的\n现在是自宅警备系的现役JC\n"
            "最好的朋友是椛！\n" + image("zhenxun")
        )
        await self_introduction.finish(result)


my_wife = on_keyword({"老婆"}, rule=to_me(), priority=5, block=True)


@my_wife.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await my_wife.finish(image("laopo.jpg", "other"))

