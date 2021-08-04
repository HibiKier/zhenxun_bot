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

exists_flag = False

update_setu = on_command("更新色图", rule=to_me(), permission=SUPERUSER, priority=1, block=True)


@update_setu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    global exists_flag
    if DOWNLOAD_SETU:
        if not exists_flag:
            exists_flag = True
            await update_setu.send("开始更新色图...", at_sender=True)
            await update_setu.send(await update_setu_img(), at_sender=True)
            exists_flag = False
        else:
            await update_setu.finish("色图正在更新....")
    else:
        await update_setu.finish('更新色图配置未开启')


# 更新色图
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=30,
)
async def _():
    global exists_flag
    if DOWNLOAD_SETU and not exists_flag:
        await update_setu_img()
