import os
import time

from nonebot.rule import to_me
from nonebot.utils import run_sync
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_alconna import Alconna, on_alconna

from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.utils.utils import ResourceDirManager

__plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="指定bot对象的功能/被动开关和状态",
    usage="""
    清理临时数据
    """.strip(),
    extra=PluginExtraData(
        author="",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)
