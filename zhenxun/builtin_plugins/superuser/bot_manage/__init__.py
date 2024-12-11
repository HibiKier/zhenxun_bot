from pathlib import Path
from typing import cast

import nonebot
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.bot_console import BotConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.platform import PlatformUtils

driver = nonebot.get_driver()

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str(Path(__file__).parent.resolve()))

__plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="指定bot对象的功能/被动开关和状态",
    usage="""
    """.strip(),
    extra=PluginExtraData(
        author="",
        version="0.1",
        plugin_type=PluginType.PARENT,
    ).dict(),
)


@driver.on_bot_connect
async def init_bot_console(bot: Bot):
    """初始化Bot管理

    参数:
        bot: Bot
    """

    async def _filter_blocked_items(
        items_list: list[str], block_list: list[str]
    ) -> list[str]:
        """过滤被block的项目

        参数:
            items_list: 需要过滤的项目列表
            block_list: block列表

        返回:
            list: 过滤后且经过格式化的项目列表
        """
        return [item for item in items_list if item not in block_list]

    plugin_list = [
        plugin.module
        for plugin in await PluginInfo.get_plugins(
            plugin_type__in=[PluginType.NORMAL, PluginType.DEPENDANT, PluginType.ADMIN]
        )
    ]
    task_list = cast(
        list[str], await TaskInfo.filter(status=True).values_list("module", flat=True)
    )
    platform = PlatformUtils.get_platform(bot)
    bot_data, created = await BotConsole.get_or_create(
        bot_id=bot.self_id, platform=platform
    )

    if not created:
        task_list = await _filter_blocked_items(
            task_list, await bot_data.get_tasks(bot.self_id, False)
        )
        plugin_list = await _filter_blocked_items(
            plugin_list, await bot_data.get_plugins(bot.self_id, False)
        )

    bot_data.available_plugins = BotConsole.convert_module_format(plugin_list)
    bot_data.available_tasks = BotConsole.convert_module_format(task_list)
    await bot_data.save(update_fields=["available_plugins", "available_tasks"])
    logger.info("初始化Bot管理完成...")
