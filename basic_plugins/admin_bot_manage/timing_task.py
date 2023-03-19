from nonebot import get_bots

from services.log import logger
from utils.utils import scheduler

from ._data_source import update_member_info

__zx_plugin_name__ = "管理方面定时任务 [Hidden]"
__plugin_usage__ = "无"
__plugin_des__ = "成员信息和管理权限的定时更新"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


async def update():
    bot_list = get_bots()
    if bot_list:
        used_group = []
        for key in bot_list:
            bot = bot_list[key]
            gl = await bot.get_group_list()
            gl = [g["group_id"] for g in gl if g["group_id"] not in used_group]
            for g in gl:
                used_group.append(g)
                try:
                    await update_member_info(bot, g)  # type: ignore
                    logger.debug(f"更新群组成员信息成功", "自动更新群组成员信息", group_id=g)
                except Exception as e:
                    logger.error(f"更新群组成员信息错误", "自动更新群组成员信息", group_id=g, e=e)


# 自动更新群员信息
@scheduler.scheduled_job(
    "cron",
    hour=2,
    minute=1,
)
async def _():
    await update()


# 快速更新群员信息以及管理员权限
@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    await update()
