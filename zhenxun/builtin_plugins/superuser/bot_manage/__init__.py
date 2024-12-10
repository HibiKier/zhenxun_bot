from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData
from zhenxun.utils.enum import PluginType

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
