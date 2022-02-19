from utils.utils import get_bot, scheduler
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from services.log import logger
from configs.path_config import IMAGE_PATH
from .data_source import get_alc_image
from utils.manager import group_manager
from configs.config import Config

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

Config.add_plugin_config(
    "_task",
    "DEFAULT_GENSHIN_ALC",
    True,
    help_="被动 原神黄历提醒 进群默认开关状态",
    default_value=True,
)

almanac = on_command("原神黄历", priority=5, block=True)


ALC_PATH = IMAGE_PATH / "genshin" / "alc"
ALC_PATH.mkdir(parents=True, exist_ok=True)


@almanac.handle()
async def _(event: MessageEvent,):
    alc_img = await get_alc_image(ALC_PATH)
    if alc_img:
        mes = alc_img + "\n ※ 黄历数据来源于 genshin.pub"
        await almanac.send(mes)
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 发送查看原神黄历"
        )
    else:
        await almanac.send("黄历图片下载失败...")


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
        if alc_img:
            mes = "[[_task|genshin_alc]]" + alc_img + "\n ※ 黄历数据来源于 genshin.pub"
            for gid in gl:
                if await group_manager.check_group_task_status(gid, "genshin_alc"):
                    await bot.send_group_msg(group_id=int(gid), message="" + mes)
