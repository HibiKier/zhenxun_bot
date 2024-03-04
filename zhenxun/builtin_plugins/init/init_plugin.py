import nonebot
from nonebot import get_loaded_plugins
from nonebot.drivers import Driver
from nonebot.plugin import Plugin
from ruamel.yaml import YAML

from zhenxun.configs.utils import PluginExtraData, PluginSetting
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.plugin_limit import PluginLimit
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

_yaml = YAML(pure=True)
_yaml.allow_unicode = True
_yaml.indent = 2

driver: Driver = nonebot.get_driver()


async def _handle_setting(
    plugin: Plugin,
    plugin_list: list[PluginInfo],
    limit_list: list[PluginLimit],
    task_list: list[TaskInfo],
):
    """处理插件设置

    参数:
        plugin: Plugin
        plugin_list: 插件列表
        limit_list: 插件限制列表
    """
    metadata = plugin.metadata
    if metadata:
        extra = metadata.extra
        extra_data = PluginExtraData(**extra)
        logger.debug(f"{metadata.name}:{plugin.name} -> {extra}", "初始化插件数据")
        setting = extra_data.setting or PluginSetting()
        if metadata.type == "library":
            extra_data.plugin_type = PluginType.HIDDEN
            extra_data.menu_type = ""
        plugin_list.append(
            PluginInfo(
                module=plugin.name,
                module_path=plugin.module_name,
                name=metadata.name,
                author=extra_data.author,
                version=extra_data.version,
                level=setting.level,
                default_status=setting.default_status,
                limit_superuser=setting.limit_superuser,
                menu_type=extra_data.menu_type,
                cost_gold=setting.cost_gold,
                plugin_type=extra_data.plugin_type,
                admin_level=extra_data.admin_level,
            )
        )
        if extra_data.limits:
            for limit in extra_data.limits:
                limit_list.append(
                    PluginLimit(
                        module=plugin.name,
                        module_path=plugin.module_name,
                        limit_type=limit._type,
                        watch_type=limit.watch_type,
                        status=limit.status,
                        check_type=limit.check_type,
                        result=limit.result,
                        cd=getattr(limit, "cd", None),
                        max_count=getattr(limit, "max_count", None),
                    )
                )
        if extra_data.tasks:
            for task in extra_data.tasks:
                task_list.append(
                    TaskInfo(
                        module=task.module,
                        name=task.name,
                        status=task.status,
                        run_time=task.run_time,
                    )
                )


@driver.on_startup
async def _():
    """
    初始化插件数据配置
    """
    plugin_list: list[PluginInfo] = []
    limit_list: list[PluginLimit] = []
    task_list: list[TaskInfo] = []
    module2id = {}
    if module_list := await PluginInfo.all().values("id", "module_path"):
        module2id = {m["module_path"]: m["id"] for m in module_list}
    for plugin in get_loaded_plugins():
        if plugin.metadata:
            await _handle_setting(plugin, plugin_list, limit_list, task_list)
    create_list = []
    update_list = []
    for plugin in plugin_list:
        if plugin.module_path not in module2id:
            create_list.append(plugin)
        else:
            plugin.id = module2id[plugin.module_path]
            update_list.append(plugin)
    if create_list:
        await PluginInfo.bulk_create(create_list, 10)
    if update_list:
        await PluginInfo.bulk_update(
            update_list,
            ["name", "author", "version", "admin_level"],
            10,
        )
    if limit_list:
        limit_create = []
        plugins = []
        if module_path_list := [limit.module_path for limit in limit_list]:
            plugins = await PluginInfo.filter(module_path__in=module_path_list).all()
        if plugins:
            for limit in limit_list:
                if l := [p for p in plugins if p.module_path == limit.module_path]:
                    plugin = l[0]
                    limit_type_list = [
                        _limit.limit_type for _limit in await plugin.plugin_limit.all()  # type: ignore
                    ]
                    if limit.limit_type not in limit_type_list:
                        limit.plugin = plugin
                        limit_create.append(limit)
        if limit_create:
            await PluginLimit.bulk_create(limit_create, 10)
    if task_list:
        module_dict = {
            t[1]: t[0] for t in await TaskInfo.all().values_list("id", "module")
        }
        create_list = []
        update_list = []
        for task in task_list:
            if task.module not in module_dict:
                create_list.append(task)
            else:
                task.id = module_dict[task.module]
                update_list.append(task)
        if create_list:
            await TaskInfo.bulk_create(create_list, 10)
        if update_list:
            await TaskInfo.bulk_update(
                update_list,
                ["run_time", "status", "name"],
                10,
            )
