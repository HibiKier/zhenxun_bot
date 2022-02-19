from utils.utils import scheduler
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .data_source import update_setu_img
from configs.config import Config


__zx_plugin_name__ = "更新色图 [Superuser]"
__plugin_usage__ = """
usage：
    更新数据库内存在的色图
    指令：
        更新色图
""".strip()
__plugin_cmd__ = ["更新色图"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_block_limit__ = {
    "rst": "色图正在更新..."
}


update_setu = on_command(
    "更新色图", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@update_setu.handle()
async def _():
    if Config.get_config("send_setu", "DOWNLOAD_SETU"):
        await update_setu.send("开始更新色图...", at_sender=True)
        await update_setu_img(True)
    else:
        await update_setu.finish("更新色图配置未开启")


# 更新色图
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=30,
)
async def _():
    if Config.get_config("send_setu", "DOWNLOAD_SETU"):
        await update_setu_img()
