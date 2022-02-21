from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, run_postprocessor, IgnoredException
from nonebot.adapters.onebot.v11.exception import ActionFailed
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser
from models.bag_user import BagUser
from utils.manager import (
    plugins2settings_manager,
    admin_manager,
    group_manager,
    plugins_manager,
    plugins2cd_manager,
    plugins2block_manager,
    plugins2count_manager,
)
from ._utils import set_block_limit_false, status_message_manager
from nonebot.typing import T_State
from typing import Optional
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PokeNotifyEvent,
    PrivateMessageEvent,
    Message,
    Event,
)
from configs.config import Config
from models.ban_user import BanUser
from utils.utils import FreqLimiter
from utils.message_builder import at
from models.level_user import LevelUser
import nonebot

_flmt = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
_flmt_g = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
_flmt_s = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
_flmt_c = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))

ignore_rst_module = ["ai", "poke", "dialogue"]


# 权限检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    module = matcher.plugin_name
    plugins2info_dict = plugins2settings_manager.get_data()
    # 功能的金币检测 #######################################
    # 功能的金币检测 #######################################
    # 功能的金币检测 #######################################
    cost_gold = 0
    if isinstance(
        event, GroupMessageEvent
    ) and plugins2settings_manager.get_plugin_data(module).get("cost_gold"):
        cost_gold = plugins2settings_manager.get_plugin_data(module).get("cost_gold")
        if await BagUser.get_gold(event.user_id, event.group_id) < cost_gold:
            await send_msg(f"金币不足..该功能需要{cost_gold}金币..", bot, event)
            raise IgnoredException(f"{module} 金币限制...")
        # 当插件不阻塞超级用户时，超级用户提前扣除金币
        if (
            str(event.user_id) in bot.config.superusers
            and not plugins2info_dict[module]["limit_superuser"]
        ):
            await BagUser.spend_gold(event.user_id, event.group_id, cost_gold)
    try:
        if (
            (not isinstance(event, MessageEvent) and module != "poke")
            or await BanUser.is_ban(event.user_id)
            and str(event.user_id) not in bot.config.superusers
        ) or (
            str(event.user_id) in bot.config.superusers
            and plugins2info_dict.get(module)
            and not plugins2info_dict[module]["limit_superuser"]
        ):
            return
    except AttributeError:
        pass
    # 超级用户命令
    try:
        _plugin = nonebot.plugin.get_plugin(module)
        _module = _plugin.module
        plugin_name = _module.__getattribute__("__zx_plugin_name__")
        if (
            "[superuser]" in plugin_name.lower()
            and str(event.user_id) in bot.config.superusers
        ):
            return
    except AttributeError:
        pass
    # 群黑名单检测 群总开关检测
    if isinstance(event, GroupMessageEvent) or matcher.plugin_name == "poke":
        try:
            if (
                group_manager.get_group_level(event.group_id) < 0
                and str(event.user_id) not in bot.config.superusers
            ):
                raise IgnoredException("群黑名单")
            if not group_manager.check_group_bot_status(event.group_id):
                try:
                    if str(event.get_message()) != "醒来":
                        raise IgnoredException("功能总开关关闭状态")
                except ValueError:
                    raise IgnoredException("功能总开关关闭状态")
        except AttributeError:
            pass
    if module in admin_manager.keys() and matcher.priority not in [1, 9]:
        if isinstance(event, GroupMessageEvent):
            # 个人权限
            if (
                not await LevelUser.check_level(
                    event.user_id,
                    event.group_id,
                    admin_manager.get_plugin_level(module),
                )
                and admin_manager.get_plugin_level(module) > 0
            ):
                try:
                    if _flmt.check(event.user_id):
                        _flmt.start_cd(event.user_id)
                        await bot.send_group_msg(
                            group_id=event.group_id,
                            message=f"{at(event.user_id)}你的权限不足喔，该功能需要的权限等级："
                            f"{admin_manager.get_plugin_level(module)}",
                        )
                except ActionFailed:
                    pass
                set_block_limit_false(event, module)
                if event.is_tome():
                    status_message_manager.add(event.group_id)
                raise IgnoredException("权限不足")
        else:
            if not await LevelUser.check_level(
                event.user_id, 0, admin_manager.get_plugin_level(module)
            ):
                try:
                    await bot.send_private_msg(
                        user_id=event.user_id,
                        message=f"你的权限不足喔，该功能需要的权限等级：{admin_manager.get_plugin_level(module)}",
                    )
                except ActionFailed:
                    pass
                set_block_limit_false(event, module)
                if event.is_tome():
                    status_message_manager.add(event.user_id)
                raise IgnoredException("权限不足")
    if module in plugins2info_dict.keys() and matcher.priority not in [1, 9]:
        # 戳一戳单独判断
        if isinstance(event, GroupMessageEvent) or (
            isinstance(event, PokeNotifyEvent) and event.group_id
        ):
            if status_message_manager.get(event.group_id) is None:
                status_message_manager.delete(event.group_id)
            if plugins2info_dict[module]["level"] > group_manager.get_group_level(
                event.group_id
            ):
                try:
                    if _flmt_g.check(event.user_id) and module not in ignore_rst_module:
                        _flmt_g.start_cd(event.user_id)
                        await bot.send_group_msg(
                            group_id=event.group_id, message="群权限不足..."
                        )
                except ActionFailed:
                    pass
                if event.is_tome():
                    status_message_manager.add(event.group_id)
                set_block_limit_false(event, module)
                raise IgnoredException("群权限不足")
            # 插件状态
            if not group_manager.get_plugin_status(module, event.group_id):
                try:
                    if module not in ignore_rst_module and _flmt_s.check(
                        event.group_id
                    ):
                        _flmt_s.start_cd(event.group_id)
                        await bot.send_group_msg(
                            group_id=event.group_id, message="该群未开启此功能.."
                        )
                except ActionFailed:
                    pass
                if event.is_tome():
                    status_message_manager.add(event.group_id)
                set_block_limit_false(event, module)
                raise IgnoredException("未开启此功能...")
            # 管理员禁用
            if not group_manager.get_plugin_status(f"{module}:super", event.group_id):
                try:
                    if (
                        _flmt_s.check(event.group_id)
                        and module not in ignore_rst_module
                    ):
                        _flmt_s.start_cd(event.group_id)
                        await bot.send_group_msg(
                            group_id=event.group_id, message="管理员禁用了此群该功能..."
                        )
                except ActionFailed:
                    pass
                if event.is_tome():
                    status_message_manager.add(event.group_id)
                set_block_limit_false(event, module)
                raise IgnoredException("管理员禁用了此群该功能...")
            # 群聊禁用
            if not plugins_manager.get_plugin_status(module, block_type="group"):
                try:
                    if (
                        _flmt_c.check(event.group_id)
                        and module not in ignore_rst_module
                    ):
                        _flmt_c.start_cd(event.group_id)
                        await bot.send_group_msg(
                            group_id=event.group_id, message="该功能在群聊中已被禁用..."
                        )
                except ActionFailed:
                    pass
                if event.is_tome():
                    status_message_manager.add(event.group_id)
                set_block_limit_false(event, module)
                raise IgnoredException("该插件在群聊中已被禁用...")
        else:
            # 私聊禁用
            if not plugins_manager.get_plugin_status(module, block_type="private"):
                try:
                    if _flmt_c.check(event.user_id):
                        _flmt_c.start_cd(event.user_id)
                        await bot.send_private_msg(
                            user_id=event.user_id, message="该功能在私聊中已被禁用..."
                        )
                except ActionFailed:
                    pass
                if event.is_tome():
                    status_message_manager.add(event.user_id)
                set_block_limit_false(event, module)
                raise IgnoredException("该插件在私聊中已被禁用...")
        # 维护
        if not plugins_manager.get_plugin_status(module, block_type="all"):
            if isinstance(
                event, GroupMessageEvent
            ) and group_manager.check_group_is_white(event.group_id):
                return
            try:
                if isinstance(event, GroupMessageEvent):
                    if (
                        _flmt_c.check(event.group_id)
                        and module not in ignore_rst_module
                    ):
                        _flmt_c.start_cd(event.group_id)
                        await bot.send_group_msg(
                            group_id=event.group_id, message="此功能正在维护..."
                        )
                else:
                    await bot.send_private_msg(
                        user_id=event.user_id, message="此功能正在维护..."
                    )
            except ActionFailed:
                pass
            if event.is_tome():
                id_ = (
                    event.group_id
                    if isinstance(event, GroupMessageEvent)
                    else event.user_id
                )
                status_message_manager.add(id_)
            set_block_limit_false(event, module)
            raise IgnoredException("此功能正在维护...")

    # 以下为限制检测 #######################################################
    # 以下为限制检测 #######################################################
    # 以下为限制检测 #######################################################
    # 以下为限制检测 #######################################################
    # 以下为限制检测 #######################################################
    # 以下为限制检测 #######################################################
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
    # 功能花费的金币 #######################################
    # 功能花费的金币 #######################################
    if cost_gold:
        await BagUser.spend_gold(event.user_id, event.group_id, cost_gold)


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
    if not isinstance(event, MessageEvent) and matcher.plugin_name != "poke":
        return
    module = matcher.plugin_name
    set_block_limit_false(event, module)


async def init_rst(rst: str, event: MessageEvent):
    if "[uname]" in rst:
        uname = event.sender.card or event.sender.nickname
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
