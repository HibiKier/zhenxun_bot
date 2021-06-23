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

matcher = on_keyword({"test"})
#
#
# @matcher.handle()
# async def _(bot: Bot, event: MessageEvent, state: T_State):
#     await matcher.send(json(
#         {"app": "com.tencent.gxhServiceIntelligentTip", "desc": "", "view": "gxhServiceIntelligentTip",
#          "ver": "", "prompt": "[QQ红包]", "appID": "", "sourceName": "", "actionData": "", "actionData_A": "",
#          "sourceUrl": "", "meta": {"gxhServiceIntelligentTip": {
#             "bgImg": "http:\/\/ptlogin2.qq.com\/ho_cross_domain?tourl=https:\/\/gxh.vip.qq.com\/\/qqshow"
#                      "\/admindata\/comdata\/vipActTpl_mobile_zbltyxn\/dddb247a4a9c6d34757c160f9e0b6669.gif",
#             "appid": "gxhServiceIntelligentTip", "reportParams": 'null', "action": ""}},
#          "config": {"forward": 1, "height": 240, "type": "normal", "autoSize": 0, "width": 180}, "text": "",
#          "sourceAd": ""}
#     ))


# @erm.handle()
# async def first_receive(bot: Bot, event: Event, state: T_State):
#     print(record('erm'))
#     await matcher.send(record('erm'))


@matcher.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message())
    if len(msg) > 5:
        return
    await matcher.reject()

