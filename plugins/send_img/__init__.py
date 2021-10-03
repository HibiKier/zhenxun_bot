from nonebot import on_command, on_keyword, on_regex
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from utils.utils import get_message_text, is_number
import os
import random
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from utils.utils import FreqLimiter, cn2py
from configs.config import IMAGE_DIR_LIST
from utils.manager import group_manager

try:
    import ujson as json
except ModuleNotFoundError:
    import json

if "色图" in IMAGE_DIR_LIST:
    IMAGE_DIR_LIST.remove("色图")

__zx_plugin_name__ = "发送本地图库图片"
__plugin_usage__ = f"""
usage：
    发送指定图库下的随机或指定id图片
    指令：
        {IMAGE_DIR_LIST} ?[id]
        示例：美图 
        示例: 萝莉 2
""".strip()
__plugin_des__ = "让看看我的私藏，指[图片]"
__plugin_cmd__ = IMAGE_DIR_LIST
__plugin_type__ = ("来点好康的",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["发送图片"] + IMAGE_DIR_LIST,
}
__plugin_task__ = {"pa": "丢人爬"}

_flmt = FreqLimiter(1)

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
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送{path}:"
            + result
        )
        await send_img.finish(f"id：{index}" + result)
    else:
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送 {path} 失败"
        )
        await send_img.finish(f"不想给你看Ov|")


@pa.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if (
        isinstance(event, GroupMessageEvent)
        and not await group_manager.check_group_task_status(event.group_id, "pa")
        or get_message_text(event.json()).startswith("开启")
        or get_message_text(event.json()).startswith("关闭")
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
    if (
        (
            isinstance(event, GroupMessageEvent)
            and not await group_manager.check_group_task_status(event.group_id, "pa")
            or get_message_text(event.json()).startswith("开启")
            or get_message_text(event.json()).startswith("关闭")
        )
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
