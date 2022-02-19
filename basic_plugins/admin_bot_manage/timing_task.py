from utils.utils import scheduler, get_bot
from ._data_source import update_member_info
from services.log import logger
from models.group_info import GroupInfo
from asyncpg.exceptions import ConnectionDoesNotExistError, UndefinedColumnError


__zx_plugin_name__ = '管理方面定时任务 [Hidden]'
__plugin_usage__ = '无'
__plugin_des__ = '成员信息和管理权限的定时更新'
__plugin_version__ = 0.1
__plugin_author__ = 'HibiKier'


# 自动更新群员信息
@scheduler.scheduled_job(
    "cron",
    hour=2,
    minute=1,
)
async def _():
    bot = get_bot()
    if bot:
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        for g in gl:
            try:
                await update_member_info(g)
                logger.info(f"更新群组 g:{g} 成功")
            except Exception as e:
                logger.error(f"更新群组错误 g:{g} e:{e}")


# 快速更新群员信息以及管理员权限
@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    try:
        bot = get_bot()
        if bot:
            gl = await bot.get_group_list()
            gl = [g["group_id"] for g in gl]
            all_group = [x.group_id for x in await GroupInfo.get_all_group()]
            for g in gl:
                if g not in all_group:
                    await update_member_info(g, False)
                    logger.info(f"快速更新群信息以及权限：{g}")
    except (IndexError, ConnectionDoesNotExistError, UndefinedColumnError):
        pass
