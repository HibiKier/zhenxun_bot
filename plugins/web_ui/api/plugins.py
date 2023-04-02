from typing import Optional

import cattrs
from fastapi import APIRouter

from configs.config import Config
from services.log import logger
from utils.manager import plugin_data_manager, plugins2settings_manager, plugins_manager
from utils.manager.models import PluginData, PluginType

from ..config import *
from ..models.model import Plugin, PluginConfig, Result
from ..models.params import UpdateConfig, UpdatePlugin
from ..utils import authentication

router = APIRouter()


@router.get("/get_plugins", dependencies=[authentication()])
def _(
    plugin_type: PluginType,
) -> Result:
    """
    获取插件列表
    :param plugin_type: 类型 normal, superuser, hidden, admin
    """
    try:
        plugin_list = []
        for module in plugin_data_manager.keys():
            plugin_data: Optional[PluginData] = plugin_data_manager[module]
            if plugin_data and plugin_data.plugin_type == plugin_type:
                plugin_config = None
                if plugin_data.plugin_configs:
                    plugin_config = {}
                    for key in plugin_data.plugin_configs:
                        plugin_config[key] = PluginConfig(
                            key=key,
                            module=module,
                            has_type=bool(plugin_data.plugin_configs[key].type),
                            **plugin_data.plugin_configs[key].dict(),
                        )
                plugin_list.append(
                    Plugin(
                        model=module,
                        plugin_settings=plugin_data.plugin_setting,
                        plugin_manager=plugin_data.plugin_status,
                        plugin_config=plugin_config,
                        cd_limit=plugin_data.plugin_cd,
                        block_limit=plugin_data.plugin_block,
                        count_limit=plugin_data.plugin_count,
                    )
                )
    except Exception as e:
        logger.error("调用API错误", "/get_plugins", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(plugin_list, "拿到了新鲜出炉的数据!")


@router.post("/update_plugins", dependencies=[authentication()])
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
            p2s.cmd = plugin.cmd
            p2s.level = plugin.group_level
        if pd := plugin_data_manager.get(module):
            menu_lin = None
            if len(pd.menu_type) > 1:
                menu_lin = pd.menu_type[1]
            if menu_lin is not None:
                pd.menu_type = (plugin.menu_type, menu_lin)
            else:
                pd.menu_type = (plugin.menu_type,)
        if pm := plugins_manager.get(module):
            if plugin.block_type:
                pm.block_type = plugin.block_type
                pm.status = False
            else:
                pm.block_type = None
                pm.status = True
        plugins2settings_manager.save()
        plugins_manager.save()
    except Exception as e:
        logger.error("调用API错误", "/update_plugins", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(info="已经帮你写好啦!")


@router.post("/update_config", dependencies=[authentication()])
def _(config_list: List[UpdateConfig]) -> Result:
    try:
        for config in config_list:
            if cg := Config.get(config.module):
                if c := cg.configs.get(config.key):
                    if isinstance(c.value, (list, tuple)) or isinstance(
                        c.default_value, (list, tuple)
                    ):
                        value = config.value.split(",")
                    else:
                        value = config.value
                    if c.type and value is not None:
                        value = cattrs.structure(value, c.type)
                    Config.set_config(config.module, config.key, value)
    except Exception as e:
        logger.error("调用API错误", "/update_config", e=e)
        return Result.fail(f"{type(e)}: {e}")
    Config.save(save_simple_data=True)
    return Result.ok(info="写入配置项了哦!")
