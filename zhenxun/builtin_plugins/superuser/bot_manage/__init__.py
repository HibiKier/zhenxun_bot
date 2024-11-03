from pathlib import Path

import nonebot
from nonebot.plugin import PluginMetadata

from zhenxun.utils.enum import PluginType
from zhenxun.configs.utils import PluginExtraData

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str(Path(__file__).parent.resolve()))

__plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="指定bot对象的功能/被动开关和状态",
    usage="""
    """.strip(),
    extra=PluginExtraData(
        author="",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)
