from utils.manager import resources_manager
from utils.utils import get_matchers
from services.log import logger
from pathlib import Path
import nonebot


def init_plugins_resources():
    """
    资源文件路径的移动
    """
    _tmp = []
    for matcher in get_matchers():
        if matcher.plugin_name not in _tmp:
            _tmp.append(matcher.plugin_name)
            _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
            try:
                _module = _plugin.module
            except AttributeError:
                logger.warning(f"插件 {matcher.plugin_name} 加载失败...，资源控制未加载...")
            else:
                try:
                    resources = _module.__getattribute__("__plugin_resources__")
                except AttributeError:
                    pass
                else:
                    path = Path(_module.__getattribute__("__file__")).parent
                    for resource in resources.keys():
                        resources_manager.add_resource(matcher.plugin_name, path / resource, resources[resource])
    resources_manager.save()
    resources_manager.start_move()












