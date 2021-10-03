from utils.utils import get_bot, scheduler
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from services.log import logger
from configs.path_config import IMAGE_PATH
from .data_source import get_alc_image
from utils.manager import group_manager
from pathlib import Path

__zx_plugin_name__ = "原神老黄历"
__plugin_usage__ = """
usage：
    有时候也该迷信一回！特别是运气方面
    指令：
        原神黄历
""".strip()
__plugin_des__ = "有时候也该迷信一回！特别是运气方面"
__plugin_cmd__ = ["原神黄历"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神黄历", "原神老黄历"],
}
__plugin_task__ = {"genshin_alc": "原神黄历提醒"}

almanac = on_command("原神黄历", priority=5, block=True)


ALC_PATH = Path(IMAGE_PATH) / "genshin" / "alc"
ALC_PATH.mkdir(parents=True, exist_ok=True)


@almanac.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    alc_img = await get_alc_image(ALC_PATH)
    mes = alc_img + "\n ※ 黄历数据来源于 genshin.pub"
    await almanac.send(mes)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送查看原神黄历"
    )


@scheduler.scheduled_job(
    "cron",
    hour=10,
    minute=25,
)
async def _():
    # 每日提醒
    bot = get_bot()
    if bot:
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        alc_img = await get_alc_image(ALC_PATH)
        mes = alc_img + "\n ※ 黄历数据来源于 genshin.pub"
        for gid in gl:
            if await group_manager.check_group_task_status(gid, "genshin_alc"):
                await bot.send_group_msg(group_id=int(gid), message=mes)
