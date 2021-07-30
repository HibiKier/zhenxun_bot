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

IMAGE_DIR_LIST.remove("色图")
cmd = set(IMAGE_DIR_LIST)

# print(cmd)

send_img = on_command("img", aliases=cmd, priority=5, block=True)
pa = on_keyword({"爬", "爪巴"}, priority=1, block=True)
search_img = on_regex(".*[份|发|张|个|次|点]图.*?", priority=6, block=True)

search_url = "https://api.fantasyzone.cc/tu/search.php"


@send_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_id = get_message_text(event.json())
    path = cn2py(state["_prefix"]["raw_command"]) + "/"
    if path in IMAGE_DIR_LIST:
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
    if isinstance(event, GroupMessageEvent):
        if await GroupRemind.get_status(event.group_id, "pa"):
            msg = get_message_text(event.json())
            if not msg or str(event.get_message()[:2]) in ["开启", "关闭"]:
                return
        if not _flmt.check(event.user_id):
            return
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


@search_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    r = re.search("[来要]?(.*)[份发张个次点]图(.*)", msg)
    num = r.group(1)
    if num in num_key.keys():
        num = num_key[num]
    elif is_number(num):
        num = int(num)
    else:
        return
    keyword = r.group(2)
    params = {"search": keyword, "r18": 0}
    async with aiohttp.ClientSession() as session:
        exists_id = []
        for _ in range(num):
            for _ in range(10):
                try:
                    async with session.get(
                        search_url, timeout=5, params=params
                    ) as response:
                        data = json.loads(await response.text())
                except TimeoutError:
                    pass
                else:
                    if data["id"] == "null":
                        await send_img.finish(f"没有搜索到 {keyword} 的图片...", at_sender=True)
                    if data["id"] in exists_id:
                        continue
                    title = data["title"]
                    author = data["userName"]
                    pid = data["id"]
                    img_url = data["url"]
                    exists_id.append(pid)
                    for _ in range(5):
                        try:
                            await download_pic(img_url, event.user_id, session)
                        except TimeoutError:
                            pass
                        else:
                            break
                    else:
                        await search_img.finish("图片下载失败...", at_sender=True)
                    await search_img.send(
                        Message(
                            f"title：{title}\n"
                            f"pid：{pid}\n"
                            f"author：{author}\n"
                            f'{image(f"send_img_{event.user_id}.png", "temp")}'
                        )
                    )
                    break
            else:
                await search_img.send("图片下载惜败了....", at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送搜索了 {num} 张 {keyword} 的图片"
    )


async def download_pic(img_url: str, user_id: int, session):
    async with session.get(img_url, timeout=2) as res:
        async with aiofiles.open(
            f"{IMAGE_PATH}/temp/send_img_{user_id}.png", "wb"
        ) as f:
            await f.write(await res.read())
