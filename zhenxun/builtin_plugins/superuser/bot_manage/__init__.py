from pathlib import Path

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
async def _(bot: Bot):
    """初始化Bot管理

    参数:
        bot: Bot
    """
    plugin_list = await PluginInfo.get_plugins(
        plugin_type__in=[PluginType.NORMAL, PluginType.DEPENDANT, PluginType.ADMIN]
    )
    available_tasks: list[str] = await TaskInfo.filter(status=True).values_list(
        "module", flat=True
    )  # type: ignore
    available_plugins = [p.module for p in plugin_list]
    # for _, bot in nonebot.get_bots().items():
    platform = PlatformUtils.get_platform(bot)
    bot_data, is_create = await BotConsole.get_or_create(
        bot_id=bot.self_id, platform=platform
    )
    if not is_create:
        block_plugins = await bot_data.get_plugins(bot.self_id, False)
        block_plugins = BotConsole._convert_module_format(block_plugins)
        for module in available_plugins.copy():
            if module in block_plugins:
                available_plugins.remove(module)
        block_tasks = await bot_data.get_tasks(bot.self_id, False)
        block_tasks = BotConsole._convert_module_format(block_tasks)
        for module in available_tasks.copy():
            if module in block_plugins:
                available_tasks.remove(module)
    bot_data.available_plugins = BotConsole._convert_module_format(available_plugins)
    bot_data.available_tasks = BotConsole._convert_module_format(available_tasks)
    await bot_data.save(update_fields=["available_plugins", "available_tasks"])
    logger.info("初始化Bot管理完成...")
