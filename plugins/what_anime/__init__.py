from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, Bot
from .data_source import get_anime
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import Arg
from utils.utils import get_message_img
from services.log import logger


__zx_plugin_name__ = "识番"
__plugin_usage__ = """
usage：
    api.trace.moe 以图识番
    指令：
        识番 [图片]
""".strip()
__plugin_des__ = "以图识番"
__plugin_cmd__ = ["识番 [图片]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["识番"],
}


what_anime = on_command("识番", priority=5, block=True)


@what_anime.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_url = get_message_img(event.json())
    if img_url:
        state["img_url"] = img_url[0]


@what_anime.got("img_url", prompt="虚空识番？来图来图GKD")
async def _(bot: Bot, event: MessageEvent, state: T_State, img_url: Message = Arg("img_url")):
    img_url = get_message_img(img_url)
    if not img_url:
        await what_anime.reject_arg("img_url", "发送的必须是图片！")
    img_url = img_url[0]
    await what_anime.send("开始识别.....")
    anime_data_report = await get_anime(img_url)
    if anime_data_report:
        await what_anime.send(anime_data_report, at_sender=True)
        logger.info(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
            f" 识番 {img_url} --> {anime_data_report}"
        )
    else:
        logger.info(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 识番 {img_url} 未找到"
        )
        await what_anime.send(f"没有寻找到该番剧，果咩..", at_sender=True)
