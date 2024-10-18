from nonebot.adapters import Bot
from nonebot_plugin_uninfo import Uninfo
from nonebot.plugin import PluginMetadata
from playwright.async_api import TimeoutError
from nonebot_plugin_alconna import At, Args, Match, Alconna, Arparma, on_alconna

from zhenxun.services.log import logger
from zhenxun.utils.depends import UserName
from zhenxun.utils.message import MessageUtils
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.group_member_info import GroupInfoUser

from .my_info import get_user_info

__plugin_meta__ = PluginMetadata(
    name="查看信息",
    description="查看个人信息",
    usage="""
    查看个人/群组信息
    指令：
        我的信息 ?[at]
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1").dict(),
)


_matcher = on_alconna(Alconna("我的信息", Args["at_user?", At]), priority=5, block=True)


@_matcher.handle()
async def _(
    bot: Bot,
    session: Uninfo,
    arparma: Arparma,
    at_user: Match[At],
    nickname: str = UserName(),
):
    user_id = session.user.id
    if at_user.available and session.group:
        user_id = at_user.result.target
        if user := await GroupInfoUser.get_or_none(
            user_id=user_id, group_id=session.group.id
        ):
            nickname = user.user_name
        else:
            nickname = user_id
    try:
        result = await get_user_info(
            session, bot, user_id, session.group.id if session.group else None, nickname
        )
        await MessageUtils.build_message(result).send(at_sender=True)
        logger.info("获取用户信息", arparma.header_result, session=session)
    except TimeoutError as e:
        logger.error("获取用户信息超时", arparma.header_result, session=session, e=e)
        await MessageUtils.build_message("获取用户信息超时...").finish(reply_to=True)
    except Exception as e:
        logger.error("获取用户信息失败", arparma.header_result, session=session, e=e)
        await MessageUtils.build_message("获取用户信息失败...").finish(reply_to=True)
