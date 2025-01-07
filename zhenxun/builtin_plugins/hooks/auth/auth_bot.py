from nonebot.exception import IgnoredException

from zhenxun.models.bot_console import BotConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.cache_utils import Cache
from zhenxun.utils.enum import CacheType


async def get_bot_status(bot_id: str):
    a = await Cache.get(CacheType.BOT, bot_id)
    cache_data = await Cache.get_cache(CacheType.BOT)
    if cache_data and cache_data.getter:
        b = await cache_data.getter.get(cache_data.data)
    if bot := await Cache.get(CacheType.BOT, bot_id):
        return bot


async def auth_bot(plugin: PluginInfo, bot_id: str):
    """机器人权限

    参数:
        plugin: PluginInfo
        bot_id: bot_id
    """
    if not await BotConsole.get_bot_status(bot_id):
        logger.debug("Bot休眠中阻断权限检测...", "AuthChecker")
        raise IgnoredException("BotConsole休眠权限检测 ignore")
    if await BotConsole.is_block_plugin(bot_id, plugin.module):
        logger.debug(
            f"Bot插件 {plugin.name}({plugin.module}) 权限检查结果为关闭...",
            "AuthChecker",
        )
        raise IgnoredException("BotConsole插件权限检测 ignore")
