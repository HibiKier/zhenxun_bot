import os
import random
from typing import List

from nonebot import on_message, on_regex
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg

from configs.config import Config
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.depends import GetConfig
from utils.manager import withdraw_message_manager
from utils.message_builder import image
from utils.utils import FreqLimiter, cn2py, get_message_text, is_number

from .anti import pix_random_change_file
from .rule import rule

__zx_plugin_name__ = "本地图库"
__plugin_usage__ = f"""
usage：
    发送指定图库下的随机或指定id图片genshin_memo
    指令：
        {Config.get_config("image_management", "IMAGE_DIR_LIST")} ?[id]
        示例：美图 
        示例: 萝莉 2
""".strip()
__plugin_des__ = "让看看我的私藏，指[图片]"
__plugin_cmd__ = Config.get_config("image_management", "IMAGE_DIR_LIST")
__plugin_type__ = ("来点好康的",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["发送图片"] + (Config.get_config("image_management", "IMAGE_DIR_LIST") or []),
}
__plugin_resources__ = {"pa": IMAGE_PATH / "pa"}

Config.add_plugin_config(
    "_task", "DEFAULT_PA", True, help_="被动 爬 进群默认开关状态", default_value=True, type=int
)

_flmt = FreqLimiter(1)


send_img = on_message(priority=5, rule=rule, block=True)
pa_reg = on_regex("^(爬|丢人爬|爪巴)$", priority=5, block=True)


_path = IMAGE_PATH / "image_management"


@send_img.handle()
async def _(
    event: MessageEvent,
    image_dir_list: List[str] = GetConfig("image_management", "IMAGE_DIR_LIST", []),
):
    msg = get_message_text(event.message).split()
    gallery = msg[0]
    if gallery not in image_dir_list:
        return
    img_id = None
    if len(msg) > 1:
        img_id = msg[1]
    path = _path / cn2py(gallery)
    if gallery in image_dir_list:
        if not path.exists() and (path.parent.parent / cn2py(gallery)).exists():
            path = IMAGE_PATH / cn2py(gallery)
        else:
            path.mkdir(parents=True, exist_ok=True)
    length = len(os.listdir(path))
    if not length:
        logger.warning(f"图库 {cn2py(gallery)} 为空，调用取消！")
        await send_img.finish("该图库中没有图片噢...")
    index = img_id if img_id else str(random.randint(0, length - 1))
    if not is_number(index):
        return
    if int(index) > length - 1 or int(index) < 0:
        await send_img.finish(f"超过当前图库的上下限了哦！({length - 1})")
    result = image(pix_random_change_file(path / f"{index}.jpg"))
    if result:
        logger.info(
            f"发送{cn2py(gallery)}:" + str(path / f"{index}.jpg"),
            "发送图片",
            event.user_id,
            getattr(event, "group_id", None),
        )
        msg_id = await send_img.send(
            f"id：{index}" + result
            if Config.get_config("image_management", "SHOW_ID")
            else "" + result
        )
        withdraw_message_manager.withdraw_message(
            event,
            msg_id,
            Config.get_config("image_management", "WITHDRAW_IMAGE_MESSAGE"),
        )
    else:
        logger.info(
            f"发送 {cn2py(gallery)} 不存在",
            "发送图片",
            event.user_id,
            getattr(event, "group_id", None),
        )
        await send_img.finish(f"不想给你看Ov|")


@pa_reg.handle()
async def _(event: MessageEvent):
    if _flmt.check(event.user_id):
        _flmt.start_cd(event.user_id)
        path = IMAGE_PATH / "pa"
        if not path.exists() or not os.listdir(IMAGE_PATH / "pa"):
            await pa_reg.finish("该图库中没有图片噢...")
        await pa_reg.finish(
            image(IMAGE_PATH / "pa" / random.choice(os.listdir(IMAGE_PATH / "pa")))
        )
