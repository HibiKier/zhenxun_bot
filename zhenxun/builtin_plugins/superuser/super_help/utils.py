import nonebot

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.enum import PluginType
from zhenxun.utils.exception import EmptyError

from .config import PluginData


async def get_plugins() -> list[PluginData]:
    """获取插件数据"""
    plugin_list = await PluginInfo.filter(
        plugin_type__in=[PluginType.SUPERUSER, PluginType.SUPER_AND_ADMIN]
    ).all()
    data_list = []
    for plugin in plugin_list:
        if _plugin := nonebot.get_plugin_by_module_name(plugin.module_path):
            if _plugin.metadata:
                data_list.append(PluginData(plugin=plugin, metadata=_plugin.metadata))
    if not data_list:
        raise EmptyError()
    return data_list
