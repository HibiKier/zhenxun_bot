from .data_source import get_anime
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from utils.utils import get_message_imgs
from services.log import logger
from utils.utils import UserExistLimiter


__plugin_name__ = "识番"
__plugin_usage__ = r"""
以图识番
识番 [图片]
""".strip()

_ulmt = UserExistLimiter()

what_anime = on_command("识番", priority=5, block=True)


@what_anime.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["取消", "算了"]:
        await what_anime.finish("已取消操作..", at_sender=True)
    img_url = get_message_imgs(event.json())
    if not img_url:
        await what_anime.reject(prompt="图呢图呢图呢图呢GKD", at_sender=True)
    state["img_url"] = img_url


@what_anime.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["帮助"]:
        await what_anime.finish(__plugin_usage__)
    if _ulmt.check(event.user_id):
        await what_anime.finish("您有识番任务正在进行，请稍等...", at_sender=True)
    img_url = get_message_imgs(event.json())
    if img_url:
        state["img_url"] = img_url


@what_anime.got("img_url", prompt="虚空识番？来图来图GKD")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_url = state["img_url"][0]
    _ulmt.set_True(event.user_id)
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
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 识番 {img_url} 未找到！！"
        )
        await what_anime.send(f"没有寻找到该番剧，果咩..", at_sender=True)
    _ulmt.set_False(event.user_id)
