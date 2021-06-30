from nonebot.rule import to_me
from nonebot.typing import T_State
import base64
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from nonebot import on_command, on_keyword, on_metaevent
from nonebot.plugin import MatcherGroup
from nonebot.adapters.cqhttp.event import GroupRequestEvent
import nonebot
from models.open_cases_user import OpenCasesUser
from tzlocal import get_localzone
from datetime import datetime, timezone, timedelta
from utils.utils import get_bot, get_message_imgs, get_local_proxy
from utils.init_result import *
from nonebot.adapters.cqhttp.message import MessageSegment
import requests
import aiohttp
from models.bag_user import BagUser
from nonebot.adapters.cqhttp.message import Message
import asyncio
from models.group_member_info import GroupInfoUser
from matplotlib import font_manager
from matplotlib import pyplot as plt
import matplotlib as mpl
from utils.utils import scheduler
from utils.browser import get_browser
from playwright.async_api import async_playwright, Browser
from typing import Optional
import playwright
# erm = on_command('异世相遇，尽享美味', aliases={'异世相遇 尽享美味', '异世相遇,尽享美味'}, priority=5, block=True)


matcher = on_keyword({"test"})


@matcher.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    browser = await get_browser()
    url = 'https://genshin.pub/daily'
    # try:
    page = await browser.new_page()
    await page.goto(url)
    await page.set_viewport_size({"width": 2560, "height": 1080})
    await page.click("button")
    card = await page.query_selector(".GSContainer_inner_border_box__21_vs")
    clip = await card.bounding_box()
    await page.screenshot(path=f'xxxx.png', clip=clip)
    await page.close()
    # except Exception:
    if page:
        await page.close()
    # raise

# @erm.handle()
# async def first_receive(bot: Bot, event: Event, state: T_State):
#     print(record('erm'))
#     await matcher.send(record('erm'))



