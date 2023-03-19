from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    GroupMessageEvent,
    MessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.message import IgnoredException, run_preprocessor
from nonebot.typing import T_State

from configs.config import Config
from models.ban_user import BanUser
from services.log import logger
from utils.message_builder import at
from utils.utils import BanCheckLimiter

malicious_check_time = Config.get_config("hook", "MALICIOUS_CHECK_TIME")
malicious_ban_count = Config.get_config("hook", "MALICIOUS_BAN_COUNT")

if not malicious_check_time:
    raise ValueError("模块: [hook], 配置项: [MALICIOUS_CHECK_TIME] 为空或小于0")
if not malicious_ban_count:
    raise ValueError("模块: [hook], 配置项: [MALICIOUS_BAN_COUNT] 为空或小于0")

_blmt = BanCheckLimiter(
    malicious_check_time,
    malicious_ban_count,
)


# 恶意触发命令检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)
    if not isinstance(event, MessageEvent):
        return
    malicious_ban_time = Config.get_config("hook", "MALICIOUS_BAN_TIME")
    if not malicious_ban_time:
        raise ValueError("模块: [hook], 配置项: [MALICIOUS_BAN_TIME] 为空或小于0")
    if matcher.type == "message" and matcher.priority not in [1, 999]:
        if state["_prefix"]["raw_command"]:
            if _blmt.check(f'{event.user_id}{state["_prefix"]["raw_command"]}'):
                await BanUser.ban(
                    event.user_id,
                    9,
                    malicious_ban_time * 60,
                )
                logger.info(
                    f"触发了恶意触发检测: {matcher.plugin_name}", "HOOK", user_id, group_id
                )
                if isinstance(event, GroupMessageEvent):
                    try:
                        await bot.send_group_msg(
                            group_id=event.group_id,
                            message=at(event.user_id) + "检测到恶意触发命令，您将被封禁 30 分钟",
                        )
                    except ActionFailed:
                        pass
                else:
                    try:
                        await bot.send_private_msg(
                            user_id=event.user_id,
                            message=at(event.user_id) + "检测到恶意触发命令，您将被封禁 30 分钟",
                        )
                    except ActionFailed:
                        pass
                logger.debug(
                    f"触发了恶意触发检测: {matcher.plugin_name}", "HOOK", user_id, group_id
                )
                raise IgnoredException("检测到恶意触发命令")
        _blmt.add(f'{event.user_id}{state["_prefix"]["raw_command"]}')
