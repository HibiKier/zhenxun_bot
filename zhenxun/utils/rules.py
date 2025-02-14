from nonebot.adapters import Bot, Event
from nonebot.internal.rule import Rule
from nonebot.permission import SUPERUSER
from nonebot_plugin_session import EventSession
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.config import Config
from zhenxun.models.level_user import LevelUser
from zhenxun.utils.platform import PlatformUtils


def admin_check(a: int | str, key: str | None = None) -> Rule:
    """
    管理员权限等级检查

    参数:
        a: 权限等级或 配置项 module
        key: 配置项 key.

    返回:
        Rule: Rule
    """

    async def _rule(bot: Bot, event: Event, session: Uninfo) -> bool:
        if await SUPERUSER(bot, event):
            return True
        if PlatformUtils.is_qbot(session):
            """官bot接口，放弃所有权限检查"""
            return False
        if session.group:
            level = a
            if isinstance(a, str) and key:
                level = Config.get_config(a, key)
            if level is not None:
                return bool(
                    await LevelUser.check_level(
                        session.user.id, session.group.id, int(level)
                    )
                )
        return False

    return Rule(_rule)


def ensure_group(session: Uninfo) -> bool:
    """
    是否在群聊中

    参数:
        session: Uninfo

    返回:
        bool: bool
    """
    return bool(session.group)


def ensure_private(session: EventSession) -> bool:
    """
    是否在私聊中

    参数:
        session: session

    返回:
        bool: bool
    """
    return not session.id3 and not session.id2


def notice_rule(event_type: type | list[type]) -> Rule:
    """
    Notice限制

    参数:
        event_type: Event类型

    返回:
        Rule: Rule
    """

    async def _rule(event: Event) -> bool:
        if isinstance(event_type, list):
            for et in event_type:
                if isinstance(event, et):
                    return True
        else:
            return isinstance(event, event_type)
        return False

    return Rule(_rule)
