import random
from types import ModuleType
from typing import Any

from configs.config import Config
from services import logger
from utils.manager import (plugin_data_manager, plugins2block_manager,
                           plugins2cd_manager, plugins2count_manager,
                           plugins2settings_manager, plugins_manager)
from utils.manager.models import (Plugin, PluginBlock, PluginCd, PluginCount,
                                  PluginData, PluginSetting, PluginType)
from utils.utils import get_matchers


def get_attr(module: ModuleType, name: str, default: Any = None) -> Any:
    """
    说明:
        获取属性
    参数:
        :param module: module
        :param name: name
        :param default: default
    """
    return getattr(module, name) if hasattr(module, name) else default


def init_plugin_info():

    for matcher in [x for x in get_matchers(True) if x.plugin]:
        try:
            plugin = matcher.plugin
            metadata = plugin.metadata
            extra = metadata.extra if metadata else {}
            if hasattr(plugin, "module"):
                module = plugin.module
                plugin_model = matcher.plugin_name
                plugin_name = (
                    metadata.name
                    if metadata and metadata.name
                    else get_attr(module, "__zx_plugin_name__", matcher.plugin_name)
                )
                if not plugin_name:
                    logger.warning(f"配置文件 模块：{plugin_model} 获取 plugin_name 失败...")
                    continue
                if "[Admin]" in plugin_name:
                    plugin_type = PluginType.ADMIN
                    plugin_name = plugin_name.replace("[Admin]", "").strip()
                elif "[Hidden]" in plugin_name:
                    plugin_type = PluginType.HIDDEN
                    plugin_name = plugin_name.replace("[Hidden]", "").strip()
                elif "[Superuser]" in plugin_name:
                    plugin_type = PluginType.SUPERUSER
                    plugin_name = plugin_name.replace("[Superuser]", "").strip()
                else:
                    plugin_type = PluginType.NORMAL
                plugin_usage = (
                    metadata.usage
                    if metadata and metadata.usage
                    else get_attr(module, "__plugin_usage__")
                )
                plugin_des = (
                    metadata.description
                    if metadata and metadata.description
                    else get_attr(module, "__plugin_des__")
                )
                menu_type = get_attr(module, "__plugin_type__") or ("normal",)
                plugin_setting = get_attr(module, "__plugin_settings__")
                if plugin_setting:
                    plugin_setting = PluginSetting(**plugin_setting)
                    plugin_setting.plugin_type = menu_type
                plugin_superuser_usage = get_attr(module, "__plugin_super_usage__")
                plugin_task = get_attr(module, "__plugin_task__")
                plugin_version = extra.get("__plugin_version__") or get_attr(
                    module, "__plugin_version__"
                )
                plugin_author = extra.get("__plugin_author__") or get_attr(
                    module, "__plugin_author__"
                )
                plugin_cd = get_attr(module, "__plugin_cd_limit__")
                if plugin_cd:
                    plugin_cd = PluginCd(**plugin_cd)
                plugin_block = get_attr(module, "__plugin_block_limit__")
                if plugin_block:
                    plugin_block = PluginBlock(**plugin_block)
                plugin_count = get_attr(module, "__plugin_count_limit__")
                if plugin_count:
                    plugin_count = PluginCount(**plugin_count)
                plugin_resources = get_attr(module, "__plugin_resources__")
                plugin_configs = get_attr(module, "__plugin_configs__")
                if settings := plugins2settings_manager.get(plugin_model):
                    plugin_setting = settings
                if plugin_cd_limit := plugins2cd_manager.get(plugin_model):
                    plugin_cd = plugin_cd_limit
                if plugin_block_limit := plugins2block_manager.get(plugin_model):
                    plugin_block = plugin_block_limit
                if plugin_count_limit := plugins2count_manager.get(plugin_model):
                    plugin_count = plugin_count_limit
                if plugin_cfg := Config.get(plugin_model):
                    plugin_configs = plugin_cfg
                plugin_status = plugins_manager.get(plugin_model)
                if not plugin_status:
                    plugin_status = Plugin(plugin_name=plugin_model)
                plugin_status.author = plugin_author
                plugin_status.version = plugin_version
                plugin_data = PluginData(
                    model=plugin_model,
                    name=plugin_name.strip(),
                    plugin_type=plugin_type,
                    usage=plugin_usage,
                    superuser_usage=plugin_superuser_usage,
                    des=plugin_des,
                    task=plugin_task,
                    menu_type=menu_type,
                    plugin_setting=plugin_setting,
                    plugin_cd=plugin_cd,
                    plugin_block=plugin_block,
                    plugin_count=plugin_count,
                    plugin_resources=plugin_resources,
                    plugin_configs=plugin_configs,
                    plugin_status=plugin_status,
                )
                plugin_data_manager.add_plugin_info(plugin_data)
        except Exception as e:
            logger.error(f"构造插件数据失败 {matcher.plugin_name} - {type(e)}：{e}")
