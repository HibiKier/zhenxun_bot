from nonebot.adapters import Bot, Event
from nonebot.internal.rule import Rule
from nonebot.permission import SUPERUSER
from nonebot_plugin_session import EventSession, SessionLevel

from zhenxun.configs.config import Config
from zhenxun.models.level_user import LevelUser


def admin_check(a: int | str, key: str | None = None) -> Rule:
    """
    管理员权限等级检查

    参数:
        a: 权限等级或 配置项 module
        key: 配置项 key.

    返回:
        Rule: Rule
    """

    async def _rule(bot: Bot, event: Event, session: EventSession) -> bool:
        if await SUPERUSER(bot, event):
            return True
        if session.id1 and session.id2:
            level = a
            if type(a) == str and key:
                level = Config.get_config(a, key)
            if level is not None:
                return bool(
                    await LevelUser.check_level(session.id1, session.id2, int(level))
                )
        return False

    return Rule(_rule)


def ensure_group(session: EventSession) -> bool:
    """
    是否在群聊中

    参数:
        session: session

    返回:
        bool: bool
    """
    return session.level in [SessionLevel.LEVEL2, SessionLevel.LEVEL3]
