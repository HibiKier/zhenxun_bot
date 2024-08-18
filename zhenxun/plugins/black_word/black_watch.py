from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

from .utils import black_word_manager

__plugin_meta__ = PluginMetadata(
    name="敏感词文本监听",
    description="敏感词文本监听",
    usage="".strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="其他",
        plugin_type=PluginType.DEPENDANT,
    ).dict(),
)

base_config = Config.get("black_word")


# 黑名单词汇检测
@run_preprocessor
async def _(
    bot: Bot, message: UniMsg, matcher: Matcher, event: Event, session: EventSession
):
    gid = session.id3 or session.id2
    if session.id1:
        if (
            event.is_tome()
            and matcher.plugin_name == "black_word"
            and not await BanConsole.is_ban(session.id1, gid)
        ):
            msg = message.extract_plain_text()
            if session.id1 in bot.config.superusers:
                return logger.debug(
                    f"超级用户跳过黑名单词汇检查 Message: {msg}", target=session.id1
                )
            if gid:
                """屏蔽群权限-1的群"""
                group, _ = await GroupConsole.get_or_create(
                    group_id=gid, channel_id__isnull=True
                )
                if group.level < 0:
                    return
                if await BanConsole.is_ban(None, gid):
                    """屏蔽群被ban的群"""
                    return
            if await black_word_manager.check(bot, session, msg) and base_config.get(
                "CONTAIN_BLACK_STOP_PROPAGATION"
            ):
                matcher.stop_propagation()
