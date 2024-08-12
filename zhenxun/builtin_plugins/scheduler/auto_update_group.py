import nonebot
from nonebot_plugin_apscheduler import scheduler

from zhenxun.services.log import logger
from zhenxun.utils.platform import PlatformUtils


# 自动更新群组信息
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    bots = nonebot.get_bots()
    for bot in bots.values():
        try:
            await PlatformUtils.update_group(bot)
        except Exception as e:
            logger.error(f"Bot: {bot.self_id} 自动更新群组信息", "自动更新群组", e=e)
    logger.info("自动更新群组成员信息成功...")


# 自动更新好友信息
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    bots = nonebot.get_bots()
    for bot in bots.values():
        try:
            await PlatformUtils.update_friend(bot)
        except Exception as e:
            logger.error(
                f"Bot: {bot.self_id} 自动更新好友信息错误", "自动更新好友", e=e
            )
    logger.info("自动更新好友信息成功...")
