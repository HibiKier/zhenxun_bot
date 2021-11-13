from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, run_postprocessor, IgnoredException
from nonebot.adapters.cqhttp.exception import ActionFailed
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser
from utils.message_builder import at
from .utils import status_message_manager, set_block_limit_false
from utils.manager import (
    plugins2cd_manager,
    plugins2block_manager,
    plugins2count_manager,
)
from typing import Optional
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    Event,
    MessageEvent,
    PrivateMessageEvent,
    GroupMessageEvent,
    Message,
)


# 命令cd | 命令阻塞 | 命令次数
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if not isinstance(event, MessageEvent) and matcher.module != "poke":
        return
    module = matcher.module
    if (
        isinstance(event, GroupMessageEvent)
        and status_message_manager.get(event.group_id) is None
    ):
        status_message_manager.delete(event.group_id)
    # Count
    if (
        plugins2count_manager.check_plugin_count_status(module)
        and event.user_id not in bot.config.superusers
    ):
        plugin_count_data = plugins2count_manager.get_plugin_count_data(module)
        limit_type = plugin_count_data["limit_type"]
        rst = plugin_count_data["rst"]
        count_type_ = event.user_id
        if limit_type == "group" and isinstance(event, GroupMessageEvent):
            count_type_ = event.group_id
        if not plugins2count_manager.check(module, count_type_):
            if rst:
                rst = await init_rst(rst, event)
                await send_msg(rst, bot, event)
            raise IgnoredException(f"{module} count次数限制...")
        else:
            plugins2count_manager.increase(module, count_type_)
    # Cd
    if plugins2cd_manager.check_plugin_cd_status(module):
        plugin_cd_data = plugins2cd_manager.get_plugin_cd_data(module)
        check_type = plugin_cd_data["check_type"]
        limit_type = plugin_cd_data["limit_type"]
        rst = plugin_cd_data["rst"]
        if (
            (isinstance(event, PrivateMessageEvent) and check_type == "private")
            or (isinstance(event, GroupMessageEvent) and check_type == "group")
            or plugins2cd_manager.get_plugin_data(module).get("check_type") == "all"
        ):
            cd_type_ = event.user_id
            if limit_type == "group" and isinstance(event, GroupMessageEvent):
                cd_type_ = event.group_id
            if not plugins2cd_manager.check(module, cd_type_):
                if rst:
                    rst = await init_rst(rst, event)
                    await send_msg(rst, bot, event)
                raise IgnoredException(f"{module} 正在cd中...")
            else:
                plugins2cd_manager.start_cd(module, cd_type_)
    # Block
    if plugins2block_manager.check_plugin_block_status(module):
        plugin_block_data = plugins2block_manager.get_plugin_block_data(module)
        check_type = plugin_block_data["check_type"]
        limit_type = plugin_block_data["limit_type"]
        rst = plugin_block_data["rst"]
        if (
            (isinstance(event, PrivateMessageEvent) and check_type == "private")
            or (isinstance(event, GroupMessageEvent) and check_type == "group")
            or check_type == "all"
        ):
            block_type_ = event.user_id
            if limit_type == "group" and isinstance(event, GroupMessageEvent):
                block_type_ = event.group_id
            if plugins2block_manager.check(block_type_, module):
                if rst:
                    rst = await init_rst(rst, event)
                    await send_msg(rst, bot, event)
                raise IgnoredException(f"{event.user_id}正在调用{module}....")
            else:
                plugins2block_manager.set_true(block_type_, module)


async def send_msg(rst: str, bot: Bot, event: MessageEvent):
    """
    发送信息
    :param rst: pass
    :param bot: pass
    :param event: pass
    """
    rst = await init_rst(rst, event)
    try:
        if isinstance(event, GroupMessageEvent):
            status_message_manager.add(event.group_id)
            await bot.send_group_msg(group_id=event.group_id, message=Message(rst))
        else:
            status_message_manager.add(event.user_id)
            await bot.send_private_msg(user_id=event.user_id, message=Message(rst))
    except ActionFailed:
        pass


# 解除命令block阻塞
@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: Event,
    state: T_State,
):
    if not isinstance(event, MessageEvent) and matcher.module != "poke":
        return
    module = matcher.module
    set_block_limit_false(event, module)


async def init_rst(rst: str, event: MessageEvent):
    if "[uname]" in rst:
        uname = event.sender.card if event.sender.card else event.sender.nickname
        rst = rst.replace("[uname]", uname)
    if "[nickname]" in rst:
        if isinstance(event, GroupMessageEvent):
            nickname = await GroupInfoUser.get_group_member_nickname(
                event.user_id, event.group_id
            )
        else:
            nickname = await FriendUser.get_friend_nickname(event.user_id)
        rst = rst.replace("[nickname]", nickname)
    if "[at]" in rst and isinstance(event, GroupMessageEvent):
        rst = rst.replace("[at]", str(at(event.user_id)))
    return rst
