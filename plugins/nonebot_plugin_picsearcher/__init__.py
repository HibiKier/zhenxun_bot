# -*- coding: utf-8 -*-
import traceback
from typing import Dict

from aiohttp.client_exceptions import ClientError
from nonebot.plugin import on_command, on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from services.log import logger
from utils.utils import get_message_text, get_message_imgs
from configs.config import MAX_FIND_IMG_COUNT
from nonebot.rule import to_me

from .ex import get_des as get_des_ex
from .iqdb import get_des as get_des_iqdb
from .saucenao import get_des as get_des_sau
from .ascii2d import get_des as get_des_asc
from .trace import get_des as get_des_trace
from .yandex import get_des as get_des_yandex


__zx_plugin_name__ = "识图"
__plugin_usage__ = """
usage：
    识别图片 [二次元图片]
    指令：
        识图 [图片]
""".strip()
__plugin_des__ = "以图搜图，看破本源"
__plugin_cmd__ = ["识图"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "synodriver"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["识图"],
}


async def get_des(url: str, mode: str, user_id: int):
    """
    :param url: 图片链接
    :param mode: 图源
    :param user_id: 用户 id
    """
    if mode == "iqdb":
        async for msg in get_des_iqdb(url):
            yield msg
    elif mode == "ex":
        async for msg in get_des_ex(url):
            yield msg
    elif mode == "trace":
        async for msg in get_des_trace(url):
            yield msg
    elif mode == "yandex":
        async for msg in get_des_yandex(url):
            yield msg
    elif mode.startswith("asc"):
        async for msg in get_des_asc(url, user_id):
            yield msg
    else:
        async for msg in get_des_sau(url, user_id):
            yield msg


setu = on_command("识图", aliases={"search"}, block=True, priority=5)


@setu.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    if imgs:
        state["setu"] = imgs[0]
    if msg:
        state["mod"] = msg


# ex/nao/trace/iqdb/ascii2d
# @setu.got("mod", prompt="从哪里查找呢? ex/nao/trace/iqdb/ascii2d")
# async def get_func(bot: Bot, event: MessageEvent, state: dict):
#     pass


@setu.args_parser
async def get_setu(bot: Bot, event: MessageEvent, state: T_State):
    imgs = get_message_imgs(event.json())
    msg = get_message_text(event.json())
    if not imgs:
        await setu.reject()
    if msg:
        state["mod"] = msg
    state["setu"] = imgs[0]


@setu.got("setu", prompt="图呢？")
async def get_setu(bot: Bot, event: MessageEvent, state: T_State):
    """
    发现没有的时候要发问
    :return:
    """
    url: str = state["setu"]
    mod: str = state["mod"] if state.get("mod") else "nao"  # 模式
    try:
        await bot.send(event=event, message="正在处理图片")
        idx = 1
        async for msg in get_des(url, mod, event.user_id):
            if msg:
                await bot.send(event=event, message=msg)
                if idx == MAX_FIND_IMG_COUNT:
                    break
                idx += 1
        if id == 1:
            await bot.send(event=event, message='没找着.')
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 识图:{url}"
        )
        # image_data: List[Tuple] = await get_pic_from_url(url)
        # await setu.finish("hso")
    except IndexError:
        # await bot.send(event, traceback.format_exc())
        await setu.finish("参数错误")
    except ClientError:
        await setu.finish("连接失败")


pic_map: Dict[str, str] = {}  # 保存这个群的其阿金一张色图 {"123456":http://xxx"}


async def check_pic(bot: Bot, event: MessageEvent, state: T_State) -> bool:
    if isinstance(event, MessageEvent):
        for msg in event.message:
            if msg.type == "image":
                url: str = msg.data["url"]
                state["url"] = url
                return True
        return False


notice_pic = on_message(check_pic, block=False, priority=1)


@notice_pic.handle()
async def handle_pic(bot: Bot, event: GroupMessageEvent, state: T_State):
    try:
        group_id: str = str(event.group_id)
        pic_map.update({group_id: state["url"]})
    except AttributeError:
        pass


previous = on_command("上一张图是什么", aliases={"上一张", "这是什么"}, rule=to_me(), block=True)


@previous.handle()
async def handle_previous(bot: Bot, event: GroupMessageEvent, state: T_State):
    await bot.send(event=event, message="processing...")
    try:
        url: str = pic_map[str(event.group_id)]
        idx = 1
        async for msg in get_des(url, "nao", event.user_id):
            await bot.send(event=event, message=msg)
            if idx == MAX_FIND_IMG_COUNT:
                break
            idx += 1
    except IndexError:
        await previous.finish("参数错误")
    except ClientError:
        await previous.finish("连接错误")
    except KeyError:
        await previous.finish("没有图啊QAQ")
