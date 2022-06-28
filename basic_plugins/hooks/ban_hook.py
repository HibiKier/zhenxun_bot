from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    MessageEvent,
    ActionFailed,
    PokeNotifyEvent,
    GroupMessageEvent,
)
from configs.config import Config
from models.ban_user import BanUser
from utils.utils import is_number, static_flmt, FreqLimiter
from utils.message_builder import at
from ._utils import ignore_rst_module, other_limit_plugins


Config.add_plugin_config(
    "hook",
    "BAN_RESULT",
    "才不会给你发消息.",
    help_="对被ban用户发送的消息",
)

_flmt = FreqLimiter(300)


# 检查是否被ban
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    if (
        (isinstance(event, MessageEvent) or isinstance(event, PokeNotifyEvent))
        and matcher.priority not in [1, 999]
    ) or matcher.plugin_name in other_limit_plugins:
        try:
            if (
                await BanUser.is_super_ban(event.user_id)
                and str(event.user_id) not in bot.config.superusers
            ):
                raise IgnoredException("用户处于超级黑名单中")
        except AttributeError:
            pass
        if (
            await BanUser.is_ban(event.user_id)
            and str(event.user_id) not in bot.config.superusers
        ):
            time = await BanUser.check_ban_time(event.user_id)
            if is_number(time):
                time = abs(int(time))
                if time < 60:
                    time = str(time) + " 秒"
                else:
                    time = str(int(time / 60)) + " 分钟"
            else:
                time = str(time) + " 分钟"
            if isinstance(event, GroupMessageEvent):
                if not static_flmt.check(event.user_id):
                    raise IgnoredException("用户处于黑名单中")
                static_flmt.start_cd(event.user_id)
                if matcher.priority != 999:
                    try:
                        ban_result = Config.get_config("hook", "BAN_RESULT")
                        if (
                            ban_result
                            and _flmt.check(event.user_id)
                            and matcher.plugin_name not in ignore_rst_module
                        ):
                            _flmt.start_cd(event.user_id)
                            await bot.send_group_msg(
                                group_id=event.group_id,
                                message=at(event.user_id)
                                + ban_result
                                + f" 在..在 {time} 后才会理你喔",
                            )
                    except ActionFailed:
                        pass
            else:
                if not static_flmt.check(event.user_id):
                    raise IgnoredException("用户处于黑名单中")
                static_flmt.start_cd(event.user_id)
                if matcher.priority != 999:
                    try:
                        ban_result = Config.get_config("hook", "BAN_RESULT")
                        if ban_result and matcher.plugin_name not in ignore_rst_module:
                            await bot.send_private_msg(
                                user_id=event.user_id,
                                message=at(event.user_id)
                                + ban_result
                                + f" 在..在 {time}后才会理你喔",
                            )
                    except ActionFailed:
                        pass
            raise IgnoredException("用户处于黑名单中")
