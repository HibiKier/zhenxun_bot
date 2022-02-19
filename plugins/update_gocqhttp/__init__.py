from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from .data_source import download_gocq_lasted, upload_gocq_lasted
from services.log import logger
from utils.utils import scheduler, get_bot
from nonebot.permission import SUPERUSER
from configs.config import Config
from pathlib import Path
import os


__zx_plugin_name__ = "更新gocq [Superuser]"
__plugin_usage__ = """
usage：
    下载最新版gocq并上传至群文件
    指令：
        更新gocq
""".strip()
__plugin_cmd__ = ["更新gocq"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_configs__ = {
    "UPDATE_GOCQ_GROUP": {
        "value": [],
        "help": "需要为哪些群更新最新版gocq吗？（上传最新版gocq）示例：[434995955, 239483248]",
        "default_value": [],
    }
}

path = str((Path() / "resources" / "gocqhttp_file").absolute()) + "/"

lasted_gocqhttp = on_command("更新gocq", permission=SUPERUSER, priority=5, block=True)


@lasted_gocqhttp.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    # try:
    if event.group_id in Config.get_config("update_gocqhttp", "UPDATE_GOCQ_GROUP"):
        await lasted_gocqhttp.send("检测中...")
        info = await download_gocq_lasted(path)
        if info == "gocqhttp没有更新！":
            await lasted_gocqhttp.finish("gocqhttp没有更新！")
        try:
            for file in os.listdir(path):
                await upload_gocq_lasted(path, file, event.group_id)
                logger.info(f"更新了cqhttp...{file}")
            await lasted_gocqhttp.send(f"gocqhttp更新了，已上传成功！\n更新内容：\n{info}")
        except Exception as e:
            logger.error(f"更新gocq错误 e：{e}")


# 更新gocq
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    if Config.get_config("update_gocqhttp", "UPDATE_GOCQ_GROUP"):
        bot = get_bot()
        try:
            info = await download_gocq_lasted(path)
            if info == "gocqhttp没有更新！":
                logger.info("gocqhttp没有更新！")
                return
            for group in Config.get_config("update_gocqhttp", "UPDATE_GOCQ_GROUP"):
                for file in os.listdir(path):
                    await upload_gocq_lasted(path, file, group)
                await bot.send_group_msg(
                    group_id=group, message=f"gocqhttp更新了，已上传成功！\n更新内容：\n{info}"
                )
        except Exception as e:
            logger.error(f"自动更新gocq出错 e:{e}")
