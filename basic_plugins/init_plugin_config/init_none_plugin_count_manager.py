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
    modules = [x.plugin_name for x in get_matchers()]
    plugins_manager_list = list(plugins_manager.keys())
    for module in plugins_manager_list:
        if module not in modules or none_plugin_count_manager.check(module):
            try:
                plugin_name = plugins_manager.get(module)["plugin_name"]
            except (AttributeError, KeyError):
                plugin_name = ""
            if none_plugin_count_manager.check(module):
                try:
                    plugins2settings_manager.delete(module)
                    plugins2settings_manager.save()
                    plugins2count_manager.delete(module)
                    plugins2count_manager.save()
                    plugins2cd_manager.delete(module)
                    plugins2cd_manager.save()
                    plugins2block_manager.delete(module)
                    plugins2block_manager.save()
                    plugins_manager.delete(module)
                    plugins_manager.save()
                    # resources_manager.remove_resource(module)
                    none_plugin_count_manager.delete(module)
                    logger.info(f"{module}:{plugin_name} 插件疑似已删除，清除对应插件数据...")
                except Exception as e:
                    logger.exception(
                        f"{module}:{plugin_name} 插件疑似已删除，清除对应插件数据失败...{type(e)}：{e}")
            else:
                none_plugin_count_manager.add_count(module)
                logger.info(
                    f"{module}:{plugin_name} 插件疑似已删除，加载{none_plugin_count_manager._max_count}次失败后将清除对应插件数据，当前次数：{none_plugin_count_manager._data[module]}")
        else:
            none_plugin_count_manager.reset(module)
    none_plugin_count_manager.save()
