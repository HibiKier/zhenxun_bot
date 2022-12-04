from utils.manager import resources_manager, plugin_data_manager
from utils.utils import get_matchers
from services.log import logger
from pathlib import Path


def init_plugins_resources():
    """
    资源文件路径的移动
    """
    for matcher in get_matchers(True):
        if plugin_data := plugin_data_manager.get(matcher.plugin_name):
            try:
                _module = matcher.plugin.module
            except AttributeError:
                logger.warning(f"插件 {matcher.plugin_name} 加载失败...，资源控制未加载...")
            else:
                if resources := plugin_data.plugin_resources:
                    path = Path(_module.__getattribute__("__file__")).parent
                    for resource in resources.keys():
                        resources_manager.add_resource(
                            matcher.plugin_name, path / resource, resources[resource]
                        )
    resources_manager.save()
    resources_manager.start_move()
