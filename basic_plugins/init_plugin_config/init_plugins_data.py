
from ruamel.yaml import YAML
from utils.manager import plugins_manager, plugin_data_manager
from utils.utils import get_matchers
from services.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json


_yaml = YAML(typ="safe")


def init_plugins_data():
    """
    初始化插件数据信息
    """
    for matcher in get_matchers(True):
        _plugin = matcher.plugin
        if not _plugin:
            continue
        try:
            _module = _plugin.module
        except AttributeError:
            if matcher.plugin_name not in plugins_manager.keys():
                plugins_manager.add_plugin_data(
                    matcher.plugin_name, matcher.plugin_name, error=True
                )
            else:
                plugins_manager[matcher.plugin_name].error = True
        else:
            if plugin_data := plugin_data_manager.get(matcher.plugin_name):
                try:
                    plugin_version = plugin_data.plugin_status.version
                    plugin_name = plugin_data.name
                    plugin_author = plugin_data.plugin_status.author
                    if matcher.plugin_name in plugins_manager.keys():
                        plugins_manager[matcher.plugin_name].error = False
                    if matcher.plugin_name not in plugins_manager.keys():
                        plugins_manager.add_plugin_data(
                            matcher.plugin_name,
                            plugin_name=plugin_name,
                            author=plugin_author,
                            version=plugin_version,
                        )
                    elif isinstance(plugin_version, str) or plugins_manager[matcher.plugin_name].version is None or (
                        plugin_version is not None
                        and plugin_version > float(plugins_manager[matcher.plugin_name].version)
                    ):
                        plugins_manager[matcher.plugin_name].plugin_name = plugin_name
                        plugins_manager[matcher.plugin_name].author = plugin_author
                        plugins_manager[matcher.plugin_name].version = plugin_version
                except Exception as e:
                    logger.error(f"插件数据 {matcher.plugin_name} 加载发生错误 {type(e)}：{e}")
    plugins_manager.save()
