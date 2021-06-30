from utils.utils import scheduler
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from .data_source import update_setu_img
from configs.config import DOWNLOAD_SETU


__plugin_name__ = "更新色图 [Hidden]"

__plugin_usage__ = '无'


update_setu = on_command("更新色图", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@update_setu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if DOWNLOAD_SETU:
        await update_setu.send("开始更新色图...", at_sender=True)
        await update_setu.finish(await update_setu_img(), at_sender=True)
    else:
        await update_setu.finish('更新色图配置未开启')


# 更新色图
@scheduler.scheduled_job(
    'cron',
    # year=None,
    # month=None,
    # day=None,
    # week=None,
    # day_of_week="mon,tue,wed,thu,fri",
    hour=4,
    minute=30,
    # second=None,
    # start_date=None,
    # end_date=None,
    # timezone=None,
)
async def _():
    if DOWNLOAD_SETU:
        await update_setu_img()
