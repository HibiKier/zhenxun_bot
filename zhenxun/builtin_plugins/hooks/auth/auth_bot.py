from nonebot.exception import IgnoredException

from zhenxun.models.bot_console import BotConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.cache_utils import Cache
from zhenxun.utils.common_utils import CommonUtils
from zhenxun.utils.enum import CacheType


async def auth_bot(plugin: PluginInfo, bot_id: str):
    """bot层面的权限检查

    参数:
        plugin: PluginInfo
        bot_id: bot id

    异常:
        IgnoredException: 忽略插件
        IgnoredException: 忽略插件
    """
    if cache := Cache[BotConsole](CacheType.BOT):
        bot = await cache.get(bot_id)
        if not bot or not bot.status:
            logger.debug("Bot不存在或休眠中阻断权限检测...", "AuthChecker")
            raise IgnoredException("BotConsole休眠权限检测 ignore")
        if CommonUtils.format(plugin.module) in bot.block_plugins:
            logger.debug(
                f"Bot插件 {plugin.name}({plugin.module}) 权限检查结果为关闭...",
                "AuthChecker",
            )
            raise IgnoredException("BotConsole插件权限检测 ignore")
