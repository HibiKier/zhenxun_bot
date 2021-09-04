from nonebot import on_command, on_keyword, on_regex
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from utils.utils import get_message_text, is_number
import os
import random
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message, GroupMessageEvent
from utils.utils import FreqLimiter, cn2py
from models.group_remind import GroupRemind
from asyncio.exceptions import TimeoutError
from configs.config import IMAGE_DIR_LIST
import aiofiles
import aiohttp
import re

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = "壁纸/萝莉/美图/在线搜图"
__plugin_usage__ = (
    "用法： \n" '\t1.发送"壁纸/萝莉/美图", 回复图片，后添加id获得指定图片 示例：萝莉 123\n' "\t2.在线搜图 示例：1张米浴的图"
)

_flmt = FreqLimiter(1)

if "色图" in IMAGE_DIR_LIST:
    IMAGE_DIR_LIST.remove("色图")

cmd = set(IMAGE_DIR_LIST)

# print(cmd)

send_img = on_command("img", aliases=cmd, priority=5, block=True)
pa = on_keyword({"丢人爬", "爪巴"}, priority=5, block=True)
pa_reg = on_regex("^爬$", priority=5, block=True)

search_url = "https://api.fantasyzone.cc/tu/search.php"


@send_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_id = get_message_text(event.json())
    path = cn2py(state["_prefix"]["raw_command"]) + "/"
    if state["_prefix"]["raw_command"] in IMAGE_DIR_LIST:
        if not os.path.exists(f"{IMAGE_PATH}/{path}/"):
            os.mkdir(f"{IMAGE_PATH}/{path}/")
    length = len(os.listdir(IMAGE_PATH + path)) - 1
    if length < 1:
        await send_img.finish("该图库中没有图片噢")
        logger.warning(f"图库 {path} 为空，调用取消！")
        return
    index = img_id if img_id else str(random.randint(0, length))
    if not is_number(index):
        await send_img.finish("id错误！")
    if int(index) > length or int(index) < 0:
        await send_img.finish(f"超过当前上下限！({length - 1})")
    result = image(f"{index}.jpg", path)
    if result:
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送{path}:"
            + result
        )
        await send_img.finish(f"id：{index}" + result)
    else:
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送 {path} 失败"
        )
        await send_img.finish(f"不想给你看Ov|")


@pa.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if isinstance(event, GroupMessageEvent) and not await GroupRemind.get_status(
        event.group_id, "pa"
    ):
        return
    msg = get_message_text(event.json())
    if not msg or str(event.get_message()[:2]) in ["开启", "关闭"]:
        return
    if _flmt.check(event.user_id):
        _flmt.start_cd(event.user_id)
        await pa.finish(image(random.choice(os.listdir(IMAGE_PATH + "pa")), "pa"))


@pa_reg.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if isinstance(event, GroupMessageEvent) and not await GroupRemind.get_status(
        event.group_id, "pa"
    ):
        return
    if _flmt.check(event.user_id):
        _flmt.start_cd(event.user_id)
        await pa.finish(image(random.choice(os.listdir(IMAGE_PATH + "pa")), "pa"))


num_key = {
    "一": 1,
    "二": 2,
    "两": 2,
    "双": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

