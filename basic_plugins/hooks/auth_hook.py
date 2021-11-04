from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.adapters.cqhttp.exception import ActionFailed
from utils.manager import (
    plugins2settings_manager,
    admin_manager,
    group_manager,
    plugins_manager,
)
from .utils import set_block_limit_false, status_message_manager
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PokeNotifyEvent,
)
from configs.config import Config
from models.ban_user import BanUser
from utils.utils import FreqLimiter
from utils.message_builder import at
from models.level_user import LevelUser


_flmt = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
_flmt_g = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
_flmt_s = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
_flmt_c = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))


ignore_rst_module = ["ai", "poke", "dialogue"]


# 权限检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    module = matcher.module
    plugins2info_dict = plugins2settings_manager.get_data()
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
    # 群黑名单检测
    if isinstance(event, GroupMessageEvent):
        if group_manager.get_group_level(event.group_id) < 0:
            raise IgnoredException("群黑名单")
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
