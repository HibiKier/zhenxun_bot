from utils.manager import (
    none_plugin_count_manager,
    plugins2count_manager,
    plugins2cd_manager,
    plugins2settings_manager,
    plugins2block_manager,
    plugins_manager,
    resources_manager
)
from services.log import logger
from utils.utils import get_matchers

try:
    import ujson as json
except ModuleNotFoundError:
    import json


def init_none_plugin_count_manager():
    """
    清除已删除插件数据
    """
    modules = [x.module for x in get_matchers()]
    for module in none_plugin_count_manager.keys():
        if module not in modules:
            none_plugin_count_manager.add_count(module)
        else:
            none_plugin_count_manager.reset(module)
        if none_plugin_count_manager.check(module):
            try:
                plugin_name = plugins_manager.get(module)["plugin_name"]
            except (AttributeError, KeyError):
                plugin_name = ""
            try:
                plugins2settings_manager.delete(module)
                plugins2count_manager.delete(module)
                plugins2cd_manager.delete(module)
                plugins2block_manager.delete(module)
                plugins_manager.delete(module)
                resources_manager.remove_resource(module)
                logger.info(f"{module}:{plugin_name} 插件疑似已删除，清除对应插件数据...")
            except Exception as e:
                logger.error(
                    f"{module}:{plugin_name} 插件疑似已删除，清除对应插件数据失败...{type(e)}：{e}"
                )
