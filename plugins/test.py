from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from nonebot import on_command, on_keyword
from nonebot.plugin import MatcherGroup
from nonebot.adapters.cqhttp.event import GroupRequestEvent
import nonebot
from models.open_cases_user import OpenCasesUser
from tzlocal import get_localzone
from datetime import datetime, timezone, timedelta
from util.utils import get_bot, get_message_imgs, get_local_proxy
from util.init_result import *
from nonebot.adapters.cqhttp.message import MessageSegment
import requests
import aiohttp
from models.bag_user import UserBag
from nonebot.adapters.cqhttp.message import Message
import asyncio
from models.group_member_info import GroupInfoUser

# erm = on_command('异世相遇，尽享美味', aliases={'异世相遇 尽享美味', '异世相遇,尽享美味'}, priority=5, block=True)

matcher = on_keyword({"test"})


@matcher.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    for i in range(1001, len(os.listdir(IMAGE_PATH + 'setu/'))):
        await matcher.send(f"id：{i}" + image(f'{i}.jpg', 'setu'))
        await asyncio.sleep(0.5)


# @erm.handle()
# async def first_receive(bot: Bot, event: Event, state: T_State):
#     print(record('erm'))
#     await matcher.send(record('erm'))
