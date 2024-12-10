from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor, run_preprocessor
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession

from ._auth_checker import LimitManage, checker


# # 权限检测
@run_preprocessor
async def _(
    matcher: Matcher, event: Event, bot: Bot, session: EventSession, message: UniMsg
):
    await checker.auth(
        matcher,
        event,
        bot,
        session,
        message,
    )


# 解除命令block阻塞
@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Exception | None,
    bot: Bot,
    event: Event,
    session: EventSession,
):
    user_id = session.id1
    group_id = session.id3
    channel_id = session.id2
    if not group_id:
        group_id = channel_id
        channel_id = None
    if user_id and matcher.plugin:
        module = matcher.plugin.name
        LimitManage.unblock(module, user_id, group_id, channel_id)
