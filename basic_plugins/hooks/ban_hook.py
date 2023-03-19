from nonebot.adapters.onebot.v11 import ActionFailed, Bot, Event, GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.message import IgnoredException, run_preprocessor
from nonebot.typing import T_State

from configs.config import Config
from models.ban_user import BanUser
from services.log import logger
from utils.message_builder import at
from utils.utils import FreqLimiter, is_number, static_flmt

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
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)
    if user_id and (
        matcher.priority not in [1, 999] or matcher.plugin_name in other_limit_plugins
    ):
        if (
            await BanUser.is_super_ban(user_id)
            and str(user_id) not in bot.config.superusers
        ):
            logger.debug(f"用户处于超级黑名单中...", "HOOK", user_id, group_id)
            raise IgnoredException("用户处于超级黑名单中")
        if await BanUser.is_ban(user_id) and str(user_id) not in bot.config.superusers:
            time = await BanUser.check_ban_time(user_id)
            if isinstance(time, int):
                time = abs(int(time))
                if time < 60:
                    time = str(time) + " 秒"
                else:
                    time = str(int(time / 60)) + " 分钟"
            else:
                time = str(time) + " 分钟"
            if isinstance(event, GroupMessageEvent):
                if not static_flmt.check(user_id):
                    logger.debug(f"用户处于黑名单中...", "HOOK", user_id, group_id)
                    raise IgnoredException("用户处于黑名单中")
                static_flmt.start_cd(user_id)
                if matcher.priority != 999:
                    try:
                        ban_result = Config.get_config("hook", "BAN_RESULT")
                        if (
                            ban_result
                            and _flmt.check(user_id)
                            and matcher.plugin_name not in ignore_rst_module
                        ):
                            _flmt.start_cd(user_id)
                            await bot.send_group_msg(
                                group_id=event.group_id,
                                message=at(user_id)
                                + ban_result
                                + f" 在..在 {time} 后才会理你喔",
                            )
                    except ActionFailed:
                        pass
            else:
                if not static_flmt.check(user_id):
                    logger.debug(f"用户处于黑名单中...", "HOOK", user_id, group_id)
                    raise IgnoredException("用户处于黑名单中")
                static_flmt.start_cd(user_id)
                if matcher.priority != 999:
                    ban_result = Config.get_config("hook", "BAN_RESULT")
                    if ban_result and matcher.plugin_name not in ignore_rst_module:
                        await bot.send_private_msg(
                            user_id=user_id,
                            message=at(user_id) + ban_result + f" 在..在 {time}后才会理你喔",
                        )
            logger.debug(f"用户处于黑名单中...", "HOOK", user_id, group_id)
            raise IgnoredException("用户处于黑名单中")
