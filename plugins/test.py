from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from nonebot import on_command, on_keyword, on_metaevent
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
from models.bag_user import BagUser
from nonebot.adapters.cqhttp.message import Message
import asyncio
from models.group_member_info import GroupInfoUser

# erm = on_command('异世相遇，尽享美味', aliases={'异世相遇 尽享美味', '异世相遇,尽享美味'}, priority=5, block=True)

# matcher = on_keyword({"test"})
#
#
# @matcher.handle()
# async def _(bot: Bot, event: MessageEvent, state: T_State):
#     songContent = [
#         {
#             "type": "music",
#             "data": {
#                 "type": "custom",
#                 "subtype": "kugou",
#                 "url": "https://webfs.yun.kugou.com/",
#                 "audio": "https://webfs.yun.kugou.com/202106231924/77ad13a9c9c091f74aa10098281433ab/G128/M02/02/00/wA0DAFplVJ6AIcIiADK1ZUYugV4043.mp3",
#                 "title": "音乐标题"
#             }
#         }
#     ]
#     await matcher.send(songContent)


# @erm.handle()
# async def first_receive(bot: Bot, event: Event, state: T_State):
#     print(record('erm'))
#     await matcher.send(record('erm'))




