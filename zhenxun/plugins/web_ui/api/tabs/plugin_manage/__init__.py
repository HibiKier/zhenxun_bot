import re

import cattrs
from fastapi import APIRouter, Query

from zhenxun.configs.config import Config
from zhenxun.models.plugin_info import PluginInfo as DbPluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.enum import BlockType, PluginType

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


@router.get(
    "/get_plugin_list", dependencies=[authentication()], deprecated="获取插件列表"  # type: ignore
)
async def _(
    plugin_type: list[PluginType] = Query(None), menu_type: str | None = None
) -> Result:
    try:
        plugin_list: list[PluginInfo] = []
        query = DbPluginInfo
        if plugin_type:
            query = query.filter(plugin_type__in=plugin_type, load_status=True)
        if menu_type:
            query = query.filter(menu_type=menu_type)
        plugins = await query.all()
        for plugin in plugins:
            plugin_info = PluginInfo(
                module=plugin.module,
                plugin_name=plugin.name,
                default_status=plugin.default_status,
                limit_superuser=plugin.limit_superuser,
                cost_gold=plugin.cost_gold,
                menu_type=plugin.menu_type,
                version=plugin.version or "0",
                level=plugin.level,
                status=plugin.status,
                author=plugin.author,
            )
            plugin_list.append(plugin_info)
    except Exception as e:
        logger.error("调用API错误", "/get_plugins", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(plugin_list, "拿到了新鲜出炉的数据!")


@router.get(
    "/get_plugin_count", dependencies=[authentication()], deprecated="获取插件数量"  # type: ignore
)
async def _() -> Result:
    plugin_count = PluginCount()
    plugin_count.normal = await DbPluginInfo.filter(
        plugin_type=PluginType.NORMAL, load_status=True
    ).count()
    plugin_count.admin = await DbPluginInfo.filter(
        plugin_type__in=[PluginType.ADMIN, PluginType.SUPER_AND_ADMIN], load_status=True
    ).count()
    plugin_count.superuser = await DbPluginInfo.filter(
        plugin_type__in=[PluginType.SUPERUSER, PluginType.SUPER_AND_ADMIN],
        load_status=True,
    ).count()
    plugin_count.other = await DbPluginInfo.filter(
        plugin_type__in=[PluginType.HIDDEN, PluginType.DEPENDANT], load_status=True
    ).count()
    return Result.ok(plugin_count)


@router.post(
    "/update_plugin", dependencies=[authentication()], description="更新插件参数"
)
async def _(plugin: UpdatePlugin) -> Result:
    try:
        db_plugin = await DbPluginInfo.get_or_none(
            module=plugin.module, load_status=True
        )
        if not db_plugin:
            return Result.fail("插件不存在...")
        db_plugin.default_status = plugin.default_status
        db_plugin.limit_superuser = plugin.limit_superuser
        db_plugin.cost_gold = plugin.cost_gold
        db_plugin.level = plugin.level
        db_plugin.menu_type = plugin.menu_type
        db_plugin.block_type = plugin.block_type
        if plugin.block_type == BlockType.ALL:
            db_plugin.status = False
        else:
            db_plugin.status = True
        await db_plugin.save()
        # 配置项
        if plugin.configs and (configs := Config.get(plugin.module)):
            for key in plugin.configs:
                if c := configs.configs.get(key):
                    value = plugin.configs[key]
                    if c.type and value is not None:
                        value = cattrs.structure(value, c.type)
                    Config.set_config(plugin.module, key, value)
    except Exception as e:
        logger.error("调用API错误", "/update_plugins", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(info="已经帮你写好啦!")


@router.post("/change_switch", dependencies=[authentication()], description="开关插件")
async def _(param: PluginSwitch) -> Result:
    db_plugin = await DbPluginInfo.get_or_none(module=param.module, load_status=True)
    if not db_plugin:
        return Result.fail("插件不存在...")
    if not param.status:
        db_plugin.block_type = BlockType.ALL
        db_plugin.status = False
    else:
        db_plugin.block_type = None
        db_plugin.status = True
    await db_plugin.save()
    return Result.ok(info="成功改变了开关状态!")


@router.get(
    "/get_plugin_menu_type", dependencies=[authentication()], description="获取插件类型"
)
async def _() -> Result:
    menu_type_list = []
    result = await DbPluginInfo.annotate().values_list("menu_type", flat=True)
    for r in result:
        if r not in menu_type_list and r:
            menu_type_list.append(r)
    return Result.ok(menu_type_list)


@router.get("/get_plugin", dependencies=[authentication()], description="获取插件详情")
async def _(module: str) -> Result:
    db_plugin = await DbPluginInfo.get_or_none(module=module, load_status=True)
    if not db_plugin:
        return Result.fail("插件不存在...")
    config_list = []
    if config := Config.get(module):
        for cfg in config.configs:
            type_str = ""
            type_inner = None
            x = str(config.configs[cfg].type)
            r = re.search(r"<class '(.*)'>", str(config.configs[cfg].type))
            if r:
                type_str = r.group(1)
            else:
                r = re.search(r"typing\.(.*)\[(.*)\]", str(config.configs[cfg].type))
                if r:
                    type_str = r.group(1)
                    if type_str:
                        type_str = type_str.lower()
                    type_inner = r.group(2)
                    if type_inner:
                        type_inner = [x.strip() for x in type_inner.split(",")]
            config_list.append(
                PluginConfig(
                    module=module,
                    key=cfg,
                    value=config.configs[cfg].value,
                    help=config.configs[cfg].help,
                    default_value=config.configs[cfg].default_value,
                    type=type_str,
                    type_inner=type_inner,  # type: ignore
                )
            )
    plugin_info = PluginDetail(
        module=module,
        plugin_name=db_plugin.name,
        default_status=db_plugin.default_status,
        limit_superuser=db_plugin.limit_superuser,
        cost_gold=db_plugin.cost_gold,
        menu_type=db_plugin.menu_type,
        version=db_plugin.version or "0",
        level=db_plugin.level,
        status=db_plugin.status,
        author=db_plugin.author,
        config_list=config_list,
        block_type=db_plugin.block_type,
    )
    return Result.ok(plugin_info)
