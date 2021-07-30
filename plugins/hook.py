from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    PrivateMessageEvent,
    GroupMessageEvent,
)
from configs.config import (
    BAN_RESULT,
    admin_plugins_auth,
    MALICIOUS_BAN_TIME,
    MALICIOUS_CHECK_TIME,
    MALICIOUS_BAN_COUNT,
)
from models.ban_user import BanUser
from utils.utils import is_number, static_flmt, BanCheckLimiter
from utils.message_builder import at
from services.log import logger
from models.level_user import LevelUser

try:
    import ujson as json
except ModuleNotFoundError:
    import json


# 检查是否被ban
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if matcher.type == "message" and matcher.priority not in [1, 9]:
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
                    time = str(int(time / 60)) + " 分"
            else:
                time = str(time) + " 分"
            if event.message_type == "group":
                if not static_flmt.check(event.user_id):
                    raise IgnoredException("用户处于黑名单中")
                static_flmt.start_cd(event.user_id)
                if matcher.priority != 9:
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message=at(event.user_id) + BAN_RESULT + f" 在..在 {time}后才会理你喔",
                    )
            else:
                if not static_flmt.check(event.user_id):
                    raise IgnoredException("用户处于黑名单中")
                static_flmt.start_cd(event.user_id)
                if matcher.priority != 9:
                    await bot.send_private_msg(
                        user_id=event.user_id,
                        message=at(event.user_id) + BAN_RESULT + f" 在..在 {time}后才会理你喔",
                    )
            raise IgnoredException("用户处于黑名单中")


_blmt = BanCheckLimiter(MALICIOUS_CHECK_TIME, MALICIOUS_BAN_COUNT)


# 恶意触发命令检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if matcher.type == "message" and matcher.priority not in [1, 9]:
        if state["_prefix"]["raw_command"]:
            # print(state["_prefix"]["raw_command"])
            if _blmt.check(f'{event.user_id}{state["_prefix"]["raw_command"]}'):
                if await BanUser.ban(event.user_id, 9, MALICIOUS_BAN_TIME * 60):
                    logger.info(f"USER {event.user_id} 触发了恶意触发检测")
                # await update_img.finish('检测到恶意触发命令，您将被封禁 30 分钟', at_sender=True)
                if event.message_type == "group":
                    if not static_flmt.check(event.user_id):
                        return
                    static_flmt.start_cd(event.user_id)
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message=at(event.user_id) + "检测到恶意触发命令，您将被封禁 30 分钟",
                    )
                else:
                    if not static_flmt.check(event.user_id):
                        return
                    static_flmt.start_cd(event.user_id)
                    await bot.send_private_msg(
                        user_id=event.user_id,
                        message=at(event.user_id) + "检测到恶意触发命令，您将被封禁 30 分钟",
                    )
                raise IgnoredException("检测到恶意触发命令")
        _blmt.add(f'{event.user_id}{state["_prefix"]["raw_command"]}')


# 权限检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if not isinstance(event, MessageEvent) or await BanUser.is_ban(event.user_id):
        return
    if matcher.module in admin_plugins_auth.keys() and matcher.priority not in [1, 9]:
        if event.message_type == "group":
            if not await LevelUser.check_level(
                event.user_id, event.group_id, admin_plugins_auth[matcher.module]
            ):
                await bot.send_group_msg(
                    group_id=event.group_id,
                    message=f"{at(event.user_id)}你的权限不足喔，该功能需要的权限等级："
                    f"{admin_plugins_auth[matcher.module]}",
                )
                raise IgnoredException("权限不足")
        else:
            if not await LevelUser.check_level(
                event.user_id, 0, admin_plugins_auth[matcher.module]
            ):
                await bot.send_private_msg(
                    user_id=event.user_id,
                    message=f"你的权限不足喔，该功能需要的权限等级：{admin_plugins_auth[matcher.module]}",
                )
                raise IgnoredException("权限不足")


# 为什么AI会自己和自己聊天
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: PrivateMessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if event.user_id == int(bot.self_id):
        raise IgnoredException("为什么AI会自己和自己聊天")


# 有命令就别说话了
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    if matcher.type == "message":
        if state["_prefix"]["raw_command"] and matcher.module == "ai":
            raise IgnoredException("有命令就别说话了")


