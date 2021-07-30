from .alc import get_almanac_base64_str, load_data
import os
from utils.utils import get_bot, scheduler
from nonebot import on_command
from models.level_user import LevelUser
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from utils.message_builder import image
from services.log import logger
from models.group_remind import GroupRemind


FILE_PATH = os.path.dirname(__file__)

almanac = on_command("原神黄历", priority=5, block=True)
reload = on_command("重载原神黄历数据", priority=5, block=True)


@almanac.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    almanac_base64 = get_almanac_base64_str()
    mes = image(b64=almanac_base64) + "\n ※ 黄历数据来源于 genshin.pub"
    await almanac.send(mes)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送查看原神黄历"
    )


@reload.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if await LevelUser.check_level(event.user_id, event.group_id, 5):
        load_data()
        await reload.send("重载成功")


@scheduler.scheduled_job(
    "cron",
    hour=10,
    minute=25,
)
async def _():
    # 每日提醒
    bot = get_bot()
    gl = await bot.get_group_list(self_id=bot.self_id)
    gl = [g["group_id"] for g in gl]
    almanac_base64 = get_almanac_base64_str()
    mes = image(b64=almanac_base64) + "\n ※ 黄历数据来源于 genshin.pub"
    for gid in gl:
        if await GroupRemind.get_status(gid, "almanac"):
            await bot.send_group_msg(group_id=int(gid), message=mes)
