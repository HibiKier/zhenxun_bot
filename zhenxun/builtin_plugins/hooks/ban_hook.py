from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.typing import T_State
from nonebot_plugin_saa import Mention, MessageFactory, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.models.ban_console import BanConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
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
            if extra.get("plugin_type") == PluginType.HIDDEN:
                return
    user_id = session.id1
    group_id = session.id3 or session.id2
    if user_id:
        ban_result = Config.get_config("hook", "BAN_RESULT")
        if user_id in bot.config.superusers:
            return
        if await BanConsole.is_ban(user_id) or await BanConsole.is_ban(
            user_id, group_id
        ):
            time = await BanConsole.check_ban_time(user_id)
            if time == -1:
                time_str = "∞"
            else:
                time = abs(int(time))
                if time < 60:
                    time_str = str(time) + " 秒"
                else:
                    time_str = str(int(time / 60)) + " 分钟"
            if ban_result and _flmt.check(user_id):
                _flmt.start_cd(user_id)
                await MessageFactory(
                    [
                        Mention(user_id),
                        Text(f"{ban_result}\n在..在 {time_str} 后才会理你喔"),
                    ]
                ).send()
            raise IgnoredException("用户处于黑名单中")
