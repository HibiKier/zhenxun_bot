from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
)
from configs.config import Config
from models.ban_user import BanUser
from utils.utils import BanCheckLimiter
from utils.message_builder import at
from services.log import logger


_blmt = BanCheckLimiter(
    Config.get_config("hook", "MALICIOUS_CHECK_TIME"),
    Config.get_config("hook", "MALICIOUS_BAN_COUNT"),
)


# 恶意触发命令检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if matcher.type == "message" and matcher.priority not in [1, 9]:
        if state["_prefix"]["raw_command"]:
            if _blmt.check(f'{event.user_id}{state["_prefix"]["raw_command"]}'):
                if await BanUser.ban(
                    event.user_id,
                    9,
                    Config.get_config("hook", "MALICIOUS_BAN_TIME") * 60,
                ):
                    logger.info(f"USER {event.user_id} 触发了恶意触发检测")
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
                raise IgnoredException("检测到恶意触发命令")
        _blmt.add(f'{event.user_id}{state["_prefix"]["raw_command"]}')
