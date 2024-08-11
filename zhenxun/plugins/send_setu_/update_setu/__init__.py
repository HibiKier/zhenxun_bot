from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import BaseBlock, PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from .data_source import update_setu_img

__plugin_meta__ = PluginMetadata(
    name="更新色图",
    description="更新数据库内存在的色图",
    usage="""
    更新数据库内存在的色图
    指令：
        更新色图
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
        limits=[BaseBlock(result="色图正在更新...")],
    ).dict(),
)

_matcher = on_alconna(
    Alconna("更新色图"), rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    if Config.get_config("send_setu", "DOWNLOAD_SETU"):
        await MessageUtils.build_message("开始更新色图...").send(reply_to=True)
        result = await update_setu_img(True)
        if result:
            await MessageUtils.build_message(result).send()
        logger.info("更新色图", arparma.header_result, session=session)
    else:
        await MessageUtils.build_message("更新色图配置未开启...").send()


# 更新色图
@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=30,
)
async def _():
    if Config.get_config("send_setu", "DOWNLOAD_SETU"):
        result = await update_setu_img()
        if result:
            logger.info(result, "自动更新色图")
