from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_uninfo import Uninfo
from tortoise.exceptions import IntegrityError

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.user_console import UserConsole
from zhenxun.services.log import logger
from zhenxun.services.cache import Cache
from zhenxun.utils.enum import (
    CacheType,
    GoldHandle,
    PluginType,
)
from zhenxun.utils.exception import InsufficientGold
from zhenxun.utils.platform import PlatformUtils

from .auth.auth_admin import auth_admin
from .auth.auth_bot import auth_bot
from .auth.auth_cost import auth_cost
from .auth.auth_group import auth_group
from .auth.auth_limit import LimitManage, auth_limit
from .auth.auth_plugin import auth_plugin
from .auth.exception import IsSuperuserException


async def auth(
    matcher: Matcher,
    event: Event,
    bot: Bot,
    session: Uninfo,
    message: UniMsg,
):
    """权限检查

    参数:
        matcher: matcher
        event: Event
        bot: bot
        session: Uninfo
        message: UniMsg
    """
    user_id = session.user.id
    group_id = None
    channel_id = None
    if session.group:
        if session.group.parent:
            group_id = session.group.parent.id
            channel_id = session.group.id
        else:
            group_id = session.group.id
    is_ignore = False
    cost_gold = 0
    try:
        from nonebot.adapters.onebot.v11 import PokeNotifyEvent

        if matcher.type == "notice" and not isinstance(event, PokeNotifyEvent):
            """过滤除poke外的notice"""
            return
    except ImportError:
        pass
    user_cache = Cache[UserConsole](CacheType.USERS)
    if matcher.plugin and (module := matcher.plugin.name):
        try:
            user = await user_cache.get(session.user.id)
        except IntegrityError as e:
            logger.debug(
                "重复创建用户，已跳过该次权限检查...",
                "AuthChecker",
                session=session,
                e=e,
            )
            return
        plugin = await Cache[PluginInfo](CacheType.PLUGINS).get(module)
        if user and plugin:
            if plugin.plugin_type == PluginType.HIDDEN:
                logger.debug(
                    f"插件: {plugin.name}:{plugin.module} "
                    "为HIDDEN，已跳过权限检查..."
                )
                return
            try:
                cost_gold = await auth_cost(user, plugin, session)
                if session.user.id in bot.config.superusers:
                    if plugin.plugin_type == PluginType.SUPERUSER:
                        raise IsSuperuserException()
                    if not plugin.limit_superuser:
                        cost_gold = 0
                        raise IsSuperuserException()
                await auth_bot(plugin, bot.self_id)
                await auth_group(plugin, session, message)
                await auth_admin(plugin, session)
                await auth_plugin(plugin, session, event)
                await auth_limit(plugin, session)
            except IsSuperuserException:
                logger.debug(
                    "超级用户或被ban跳过权限检测...", "AuthChecker", session=session
                )
            except IgnoredException:
                is_ignore = True
                LimitManage.unblock(matcher.plugin.name, user_id, group_id, channel_id)
            except AssertionError as e:
                is_ignore = True
                logger.debug("消息无法发送", session=session, e=e)
    if cost_gold and user_id:
        """花费金币"""
        try:
            await UserConsole.reduce_gold(
                user_id,
                cost_gold,
                GoldHandle.PLUGIN,
                matcher.plugin.name if matcher.plugin else "",
                PlatformUtils.get_platform(session),
            )
        except InsufficientGold:
            if u := await UserConsole.get_user(user_id):
                u.gold = 0
                await u.save(update_fields=["gold"])
        # 更新缓存
        await user_cache.update(user_id)
        logger.debug(f"调用功能花费金币: {cost_gold}", "AuthChecker", session=session)
    if is_ignore:
        raise IgnoredException("权限检测 ignore")
