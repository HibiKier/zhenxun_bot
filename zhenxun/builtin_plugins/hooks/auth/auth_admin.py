from nonebot.exception import IgnoredException
from nonebot_plugin_alconna import At
from nonebot_plugin_uninfo import Uninfo

from zhenxun.models.level_user import LevelUser
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.cache import Cache
from zhenxun.services.log import logger
from zhenxun.utils.enum import CacheType
from zhenxun.utils.message import MessageUtils

from .utils import freq


async def auth_admin(plugin: PluginInfo, session: Uninfo):
    """管理员命令 个人权限

    参数:
        plugin: PluginInfo
        session: PluginInfo
    """
    group_id = None
    cache = Cache[list[LevelUser]](CacheType.LEVEL)
    user_level = await cache.get(session.user.id) or []
    if session.group:
        if session.group.parent:
            group_id = session.group.parent.id
        else:
            group_id = session.group.id

    if not plugin.admin_level:
        return
    if group_id:
        user_level += await cache.get(session.user.id, group_id) or []
        user = max(user_level, key=lambda x: x.user_level)
        if user.user_level < plugin.admin_level:
            try:
                if freq._flmt.check(session.user.id):
                    freq._flmt.start_cd(session.user.id)
                    await MessageUtils.build_message(
                        [
                            At(flag="user", target=session.user.id),
                            "你的权限不足喔，"
                            f"该功能需要的权限等级: {plugin.admin_level}",
                        ]
                    ).send(reply_to=True)
            except Exception as e:
                logger.error(
                    "auth_admin 发送消息失败",
                    "AuthChecker",
                    session=session,
                    e=e,
                )
            logger.debug(
                f"{plugin.name}({plugin.module}) 管理员权限不足...",
                "AuthChecker",
                session=session,
            )
            raise IgnoredException("管理员权限不足...")
    elif user_level:
        user = max(user_level, key=lambda x: x.user_level)
        if user.user_level < plugin.admin_level:
            try:
                await MessageUtils.build_message(
                    f"你的权限不足喔，该功能需要的权限等级: {plugin.admin_level}"
                ).send()
            except Exception as e:
                logger.error(
                    "auth_admin 发送消息失败", "AuthChecker", session=session, e=e
                )
        logger.debug(
            f"{plugin.name}({plugin.module}) 管理员权限不足...",
            "AuthChecker",
            session=session,
        )
        raise IgnoredException("权限不足")
