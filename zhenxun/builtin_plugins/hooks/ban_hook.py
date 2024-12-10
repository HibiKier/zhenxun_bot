from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.typing import T_State
from nonebot_plugin_alconna import At
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import FreqLimiter

Config.add_plugin_config(
    "hook",
    "BAN_RESULT",
    "才不会给你发消息.",
    help="对被ban用户发送的消息",
)

_flmt = FreqLimiter(300)


# 检查是否被ban
@run_preprocessor
async def _(
    matcher: Matcher, bot: Bot, event: Event, state: T_State, session: EventSession
):
    if plugin := matcher.plugin:
        if metadata := plugin.metadata:
            extra = metadata.extra
            if extra.get("plugin_type") in [PluginType.HIDDEN]:
                return
    user_id = session.id1
    group_id = session.id3 or session.id2
    if group_id:
        if user_id in bot.config.superusers:
            return
        if await BanConsole.is_ban(None, group_id):
            logger.debug("群组处于黑名单中...", "ban_hook")
            raise IgnoredException("群组处于黑名单中...")
        if g := await GroupConsole.get_group(group_id):
            if g.level < 0:
                logger.debug("群黑名单, 群权限-1...", "ban_hook")
                raise IgnoredException("群黑名单, 群权限-1..")
    if user_id:
        ban_result = Config.get_config("hook", "BAN_RESULT")
        if user_id in bot.config.superusers:
            return
        if await BanConsole.is_ban(user_id, group_id):
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
            if time != -1 and ban_result and _flmt.check(user_id):
                _flmt.start_cd(user_id)
                await MessageUtils.build_message(
                    [
                        At(flag="user", target=user_id),
                        f"{ban_result}\n在..在 {time_str} 后才会理你喔",
                    ]
                ).send()
            logger.debug("用户处于黑名单中...", "ban_hook")
            raise IgnoredException("用户处于黑名单中...")
