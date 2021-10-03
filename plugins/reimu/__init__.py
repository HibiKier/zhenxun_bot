from nonebot import on_command
from nonebot.adapters.cqhttp.permission import PRIVATE
from .data_source import from_reimu_get_info
from services.log import logger
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent
from nonebot.typing import T_State
from utils.utils import is_number, get_message_text, UserBlockLimiter, scheduler
from models.count_user import UserCount
from configs.config import COUNT_PER_DAY_REIMU, NICKNAME

__zx_plugin_name__ = "上车"
__plugin_usage__ = """
usage：
    * 请各位使用后不要转发 *
    * 大部分解压密码是⑨ *
    / 并不推荐小色批使用此功能[主要是不够色，目的不够明确] /
    指令：
        上车 ?[page] [目的地]
        示例：上车 萝莉
        示例：上车 5 萝莉: 该目的地第5页停车场
    ps: 请尽量提供具体的目的地名称
""".strip()
__plugin_des__ = "都坐稳了，老司机焊死了车门！[仅限私聊]"
__plugin_cmd__ = ["上车 ?[page] [目的地]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["上车"],
}


_ulmt = UserBlockLimiter()

reimu = on_command("上车", permission=PRIVATE, block=True, priority=1)


@reimu.args_parser
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if get_message_text(event.json()) in ["取消", "算了"]:
        await reimu.finish("已取消操作..", at_sender=True)
    if not get_message_text(event.json()):
        await reimu.reject("没时间等了！快说你要去哪里？", at_sender=True)
    state["keyword"] = get_message_text(event.json())
    state["page"] = 1


@reimu.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if str(event.get_message()) in ["帮助"]:
        await reimu.finish(__plugin_usage__)
    if await UserCount.check_count(event.user_id, "reimu", COUNT_PER_DAY_REIMU):
        await reimu.finish("今天已经没车了，请明天再来...", at_sender=True)
    if _ulmt.check(event.user_id):
        await reimu.finish("您还没下车呢，请稍等...", at_sender=True)
    _ulmt.set_true(event.user_id)
    msg = get_message_text(event.json())
    args = msg.split(" ")
    if msg in ["!", "！", "?", "？", ",", "，", ".", "。"]:
        await reimu.finish(__plugin_usage__)
    if msg:
        if len(args) > 1 and is_number(args[0]):
            state["keyword"] = args[1]
            state["page"] = args[0]
        else:
            state["keyword"] = msg
            state["page"] = 1


@reimu.got("keyword", "你的目的地是哪？")
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    try:
        keyword = state["keyword"]
        page = state["page"]
        await UserCount.add_count(event.user_id, "reimu")
        await reimu.send(
            f"已经帮你关好车门了，请等待发车（不加{NICKNAME}好友的话是欣赏不到旅途的风景的）", at_sender=True
        )
        reimu_report = await from_reimu_get_info(keyword, page)
        if reimu_report:
            await reimu.send(reimu_report)
        else:
            logger.error("Not found reimuInfo")
            await reimu.send("没找着")
        _ulmt.set_false(event.user_id)
    except:
        _ulmt.set_false(event.user_id)


@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    await UserCount.reset_count()
