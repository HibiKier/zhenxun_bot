import re
from typing import List, Optional

import cattrs
from fastapi import APIRouter, Query

from configs.config import Config
from services.log import logger
from utils.manager import plugin_data_manager, plugins2settings_manager, plugins_manager
from utils.manager.models import PluginData, PluginSetting, PluginType

from ....base_model import Result
from ....utils import authentication
from .model import (
    PluginConfig,
    PluginCount,
    PluginDetail,
    PluginInfo,
    PluginSwitch,
    UpdatePlugin,
)

router = APIRouter(prefix="/plugin")


@router.get("/get_plugin_list", dependencies=[authentication()], deprecated="获取插件列表")
def _(
    plugin_type: List[PluginType] = Query(None), menu_type: Optional[str] = None
) -> Result:
    """
    获取插件列表
    :param plugin_type: 类型 normal, superuser, hidden, admin
    :param menu_type: 菜单类型
    """
    try:
        plugin_list: List[PluginInfo] = [] 
        for module in plugin_data_manager.keys():
            plugin_data: Optional[PluginData] = plugin_data_manager[module]
            if plugin_data and plugin_data.plugin_type in plugin_type:
                setting = plugin_data.plugin_setting or PluginSetting()
                plugin = plugin_data.plugin_status
                menu_type_ = getattr(setting, "plugin_type", ["无"])[0]
                if menu_type and menu_type != menu_type_:
                    continue
                plugin_info = PluginInfo(
                    module=module,
                    plugin_name=plugin_data.name,
                    default_status=getattr(setting, "default_status", False),
                    limit_superuser=getattr(setting, "limit_superuser", False),
                    cost_gold=getattr(setting, "cost_gold", 0),
                    menu_type=menu_type_,
                    version=(plugin.version or 0) if plugin else 0,
                    level=getattr(setting, "level", 5),
                    status=plugin.status if plugin else False,
                    author=plugin.author if plugin else None
                )
                plugin_info.version = (plugin.version or 0) if plugin else 0
                plugin_list.append(plugin_info)
    except Exception as e:
        logger.error("调用API错误", "/get_plugins", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(plugin_list, "拿到了新鲜出炉的数据!")

@router.get("/get_plugin_count", dependencies=[authentication()], deprecated="获取插件数量")
def _() -> Result:
    plugin_count = PluginCount()
    for module in plugin_data_manager.keys():
        plugin_data: Optional[PluginData] = plugin_data_manager[module]
        if plugin_data and plugin_data.plugin_type == PluginType.NORMAL:
            plugin_count.normal += 1
        elif plugin_data and plugin_data.plugin_type == PluginType.ADMIN:
            plugin_count.admin += 1
        elif plugin_data and plugin_data.plugin_type == PluginType.SUPERUSER:
            plugin_count.superuser += 1
        else:
            plugin_count.other += 1
    return Result.ok(plugin_count)

@router.post("/update_plugin", dependencies=[authentication()], description="更新插件参数")
def _(plugin: UpdatePlugin) -> Result:
    """
    修改插件信息
    :param plugin: 插件内容
    """
    try:
        module = plugin.module
        if p2s := plugins2settings_manager.get(module):
            p2s.default_status = plugin.default_status
            p2s.limit_superuser = plugin.limit_superuser
            p2s.cost_gold = plugin.cost_gold
            # p2s.cmd = plugin.cmd.split(",") if plugin.cmd else []
            p2s.level = plugin.level
            menu_lin = None
            if len(p2s.plugin_type) > 1:
                menu_lin = p2s.menu_type[1]
            if menu_lin is not None:
                p2s.plugin_type = (plugin.menu_type, menu_lin)
            else:
                p2s.plugin_type = (plugin.menu_type,)
        if pm := plugins_manager.get(module):
            if plugin.block_type:
                pm.block_type = plugin.block_type
                pm.status = False
            else:
                pm.block_type = None
                pm.status = True
        plugins2settings_manager.save()
        plugins_manager.save()
        # 配置项
        if plugin.configs and (configs := Config.get(module)):
            for key in plugin.configs:
                if c := configs.configs.get(key):
                    value = plugin.configs[key]
                    # if isinstance(c.value, (list, tuple)) or isinstance(
                    #     c.default_value, (list, tuple)
                    # ):
                    #     value = value.split(",")
                    if c.type and value is not None:
                        value = cattrs.structure(value, c.type)
                    Config.set_config(module, key, value)
        plugin_data_manager.reload()
    except Exception as e:
        logger.error("调用API错误", "/update_plugins", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(info="已经帮你写好啦!")


@router.post("/change_switch", dependencies=[authentication()], description="开关插件")
def _(param: PluginSwitch) -> Result:
    if pm := plugins_manager.get(param.module):
        pm.block_type = None if param.status else 'all'
        pm.status = param.status
        plugins_manager.save()
        return Result.ok(info="成功改变了开关状态!")
    return Result.warning_("未获取该插件的配置!")


@router.get("/get_plugin_menu_type", dependencies=[authentication()], description="获取插件类型")
def _() -> Result:
    menu_type_list = []
    for module in plugin_data_manager.keys():
        plugin_data: Optional[PluginData] = plugin_data_manager[module]
        if plugin_data:
            setting = plugin_data.plugin_setting or PluginSetting()
            menu_type = getattr(setting, "plugin_type", ["无"])[0]
            if menu_type not in menu_type_list:
                menu_type_list.append(menu_type)
    return Result.ok(menu_type_list)


@router.get("/get_plugin", dependencies=[authentication()], description="获取插件详情")
def _(module: str) -> Result:
    if plugin_data := plugin_data_manager.get(module):
        setting = plugin_data.plugin_setting or PluginSetting()
        plugin = plugin_data.plugin_status
        config_list = []
        if config := Config.get(module):
            for cfg in config.configs:
                type_str = ""
                type_inner = None
                x = str(config.configs[cfg].type)
                r = re.search(r"<class '(.*)'>",str(config.configs[cfg].type))
                if r:
                    type_str = r.group(1)
                else:
                    r = re.search(r"typing\.(.*)\[(.*)\]",str(config.configs[cfg].type))
                    if r:
                        type_str = r.group(1)
                        if type_str:
                            type_str = type_str.lower()
                        type_inner = r.group(2)
                        if type_inner:
                            type_inner = [x.strip() for x in type_inner.split(",")]
                config_list.append(PluginConfig(
                    module=module,
                    key=cfg,
                    value=config.configs[cfg].value,
                    help=config.configs[cfg].help,
                    default_value=config.configs[cfg].default_value,
                    type=type_str,
                    type_inner=type_inner
                ))
        plugin_info = PluginDetail(
            module=module,
            plugin_name=plugin_data.name,
            default_status=getattr(setting, "default_status", False),
            limit_superuser=getattr(setting, "limit_superuser", False),
            cost_gold=getattr(setting, "cost_gold", 0),
            menu_type=getattr(setting, "plugin_type", ["无"])[0],
            version=(plugin.version or 0) if plugin else 0,
            level=getattr(setting, "level", 5),
            status=plugin.status if plugin else False,
            author=plugin.author if plugin else None,
            config_list=config_list,
            block_type=getattr(plugin, "block_type", None)
        )
        return Result.ok(plugin_info)
    return Result.warning_("未获取到插件详情...")