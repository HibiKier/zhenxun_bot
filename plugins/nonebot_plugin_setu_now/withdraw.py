import time
import datetime

from nonebot import require, get_driver
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot

from configs.config import Config

scheduler = require("nonebot_plugin_apscheduler").scheduler

WITHDRAW_TIME = Config.get_config("nonebot_plugin_setu_now", "SETU_WITHDRAW")


def add_withdraw_job(bot: Bot, message_id: int):
    if WITHDRAW_TIME:
        logger.debug("添加撤回任务")
        scheduler.add_job(
            withdraw_msg,
            "date",
            args=[bot, message_id],
            run_date=datetime.datetime.fromtimestamp(time.time() + WITHDRAW_TIME),  # type: ignore
        )


async def withdraw_msg(bot: Bot, message_id: int):
    await bot.delete_msg(message_id=message_id)
