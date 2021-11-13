from nonebot import on_command, on_keyword, on_regex
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from utils.utils import get_message_text, is_number
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from utils.utils import FreqLimiter, cn2py
from configs.config import Config
from utils.manager import group_manager, withdraw_message_manager
import random
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__zx_plugin_name__ = "发送本地图库图片"
__plugin_usage__ = f"""
usage：
    发送指定图库下的随机或指定id图片
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
    "cmd": ["发送图片"] + Config.get_config("image_management", "IMAGE_DIR_LIST"),
}
__plugin_task__ = {"pa": "丢人爬"}
__plugin_resources__ = {
    "pa": IMAGE_PATH
}

_flmt = FreqLimiter(1)

cmd = set(Config.get_config("image_management", "IMAGE_DIR_LIST"))

# print(cmd)

send_img = on_command("img", aliases=cmd, priority=5, block=True)
pa = on_keyword({"丢人爬", "爪巴"}, priority=5, block=True)
pa_reg = on_regex("^爬$", priority=5, block=True)

search_url = "https://api.fantasyzone.cc/tu/search.php"


@send_img.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_id = get_message_text(event.json())
    path = cn2py(state["_prefix"]["raw_command"]) + "/"
    if state["_prefix"]["raw_command"] in Config.get_config(
        "image_management", "IMAGE_DIR_LIST"
    ):
        if not os.path.exists(f"{IMAGE_PATH}/{path}/"):
            os.mkdir(f"{IMAGE_PATH}/{path}/")
    length = len(os.listdir(IMAGE_PATH + path))
    if length == 0:
        logger.warning(f"图库 {path} 为空，调用取消！")
        await send_img.finish("该图库中没有图片噢")
    index = img_id if img_id else str(random.randint(0, length))
    if not is_number(index):
        return
    if int(index) > length - 1 or int(index) < 0:
        await send_img.finish(f"超过当前上下限！({length - 1})")
    result = image(f"{index}.jpg", path)
    if result:
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送{path}:"
            + result
        )
        msg_id = await send_img.send(f"id：{index}" + result)
        withdraw_message_manager.withdraw_message(
            event,
            msg_id,
            Config.get_config("image_management", "WITHDRAW_IMAGE_MESSAGE"),
        )
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
        isinstance(event, GroupMessageEvent)
        and not await group_manager.check_group_task_status(event.group_id, "pa")
        or get_message_text(event.json()).startswith("开启")
        or get_message_text(event.json()).startswith("关闭")
    ):
        return
    if _flmt.check(event.user_id):
        _flmt.start_cd(event.user_id)
        await pa.finish(image(random.choice(os.listdir(IMAGE_PATH + "pa")), "pa"))
