from nonebot.exception import IgnoredException
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_uninfo import Uninfo

from zhenxun.models.group_console import GroupConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.cache_utils import Cache
from zhenxun.utils.enum import CacheType


async def auth_group(plugin: PluginInfo, session: Uninfo, message: UniMsg):
    """群黑名单检测 群总开关检测

    参数:
        plugin: PluginInfo
        session: EventSession
        message: UniMsg
    """
    if not session.group:
        return
    if session.group.parent:
        group_id = session.group.parent.id
    else:
        group_id = session.group.id
    text = message.extract_plain_text()
    group = await Cache[GroupConsole](CacheType.GROUPS).get(group_id)
    if not group:
        """群不存在"""
        logger.debug(
            "群组信息不存在...",
            "AuthChecker",
            session=session,
        )
        raise IgnoredException("群不存在")
    if group.level < 0:
        """群权限小于0"""
        logger.debug(
            "群黑名单, 群权限-1...",
            "AuthChecker",
            session=session,
        )
        raise IgnoredException("群黑名单")
    if not group.status:
        """群休眠"""
        if text.strip() != "醒来":
            logger.debug("群休眠状态...", "AuthChecker", session=session)
            raise IgnoredException("群休眠状态")
    if plugin.level > group.level:
        """插件等级大于群等级"""
        logger.debug(
            f"{plugin.name}({plugin.module}) 群等级限制.."
            f"该功能需要的群等级: {plugin.level}..",
            "AuthChecker",
            session=session,
        )
        raise IgnoredException(f"{plugin.name}({plugin.module}) 群等级限制...")
