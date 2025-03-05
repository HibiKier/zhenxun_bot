from nonebot.adapters import Bot
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot_plugin_alconna import At
from nonebot_plugin_uninfo import Uninfo
from tortoise.exceptions import MultipleObjectsReturned

from zhenxun.configs.config import Config
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.cache import Cache
from zhenxun.services.log import logger
from zhenxun.utils.enum import CacheType, PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import FreqLimiter

Config.add_plugin_config(
    "hook",
    "BAN_RESULT",
    "才不会给你发消息.",
    help="对被ban用户发送的消息",
)

_flmt = FreqLimiter(300)


async def is_ban(user_id: str | None, group_id: str | None):
    cache = Cache[list[BanConsole]](CacheType.BAN)
    result = await cache.get(user_id, group_id) or await cache.get(user_id)
    return result and result[0].ban_time > 0


# 检查是否被ban
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, session: Uninfo):
    if plugin := matcher.plugin:
        if metadata := plugin.metadata:
            extra = metadata.extra
            if extra.get("plugin_type") in [PluginType.HIDDEN]:
                return
    user_id = session.user.id
    group_id = session.group.id if session.group else None
    cache = Cache[list[BanConsole]](CacheType.BAN)
    if user_id in bot.config.superusers:
        return
    if group_id:
        try:
            if await is_ban(None, group_id):
                logger.debug("群组处于黑名单中...", "BanChecker")
                raise IgnoredException("群组处于黑名单中...")
        except MultipleObjectsReturned:
            logger.warning(
                "群组黑名单数据重复，过滤该次hook并移除多余数据...", "BanChecker"
            )
            ids = await BanConsole.filter(user_id="", group_id=group_id).values_list(
                "id", flat=True
            )
            await BanConsole.filter(id__in=ids[:-1]).delete()
            await cache.reload()
        group_cache = Cache[GroupConsole](CacheType.GROUPS)
        if g := await group_cache.get(group_id):
            if g.level < 0:
                logger.debug("群黑名单, 群权限-1...", "BanChecker")
                raise IgnoredException("群黑名单, 群权限-1..")
    if user_id:
        ban_result = Config.get_config("hook", "BAN_RESULT")
        if await is_ban(user_id, group_id):
            time = await BanConsole.check_ban_time(user_id, group_id)
            if time == -1:
                time_str = "∞"
            else:
                time = abs(int(time))
                if time < 60:
                    time_str = f"{time!s} 秒"
                else:
                    minute = int(time / 60)
                    if minute > 60:
                        hours = minute // 60
                        minute %= 60
                        time_str = f"{hours} 小时 {minute}分钟"
                    else:
                        time_str = f"{minute} 分钟"
            db_plugin = await Cache[PluginInfo](CacheType.PLUGINS).get(
                matcher.plugin_name
            )
            if (
                db_plugin
                # and not db_plugin.ignore_prompt
                and time != -1
                and ban_result
                and _flmt.check(user_id)
            ):
                _flmt.start_cd(user_id)
                logger.debug(f"ban检测发送插件: {matcher.plugin_name}")
                await MessageUtils.build_message(
                    [
                        At(flag="user", target=user_id),
                        f"{ban_result}\n在..在 {time_str} 后才会理你喔",
                    ]
                ).send()
            logger.debug("用户处于黑名单中...", "BanChecker")
            raise IgnoredException("用户处于黑名单中...")
