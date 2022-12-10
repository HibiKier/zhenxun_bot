from typing import Optional

import nonebot
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    PrivateMessageEvent,
    Bot,
    Event,
    MessageEvent,
    Message,
    PokeNotifyEvent,
)
from nonebot.exception import ActionFailed, IgnoredException
from nonebot.internal.matcher import Matcher

from models.bag_user import BagUser
from models.ban_user import BanUser
from models.friend_user import FriendUser
from models.group_member_info import GroupInfoUser
from models.level_user import LevelUser
from models.user_shop_gold_log import UserShopGoldLog
from utils.decorator import Singleton
from utils.manager import (
    plugins2block_manager,
    StaticData,
    plugins2settings_manager,
    group_manager,
    admin_manager,
    plugins_manager,
    plugins2cd_manager,
    plugins2count_manager,
)
from utils.message_builder import at
from utils.utils import FreqLimiter
from configs.config import Config
import time

ignore_rst_module = ["ai", "poke", "dialogue"]

other_limit_plugins = ["poke"]


class StatusMessageManager(StaticData):
    def __init__(self):
        super().__init__(None)

    def add(self, id_: int):
        self._data[id_] = time.time()

    def delete(self, id_: int):
        if self._data.get(id_):
            del self._data[id_]

    def check(self, id_: int, t: int = 30) -> bool:
        if self._data.get(id_):
            if time.time() - self._data[id_] > t:
                del self._data[id_]
                return True
            return False
        return True


status_message_manager = StatusMessageManager()


def set_block_limit_false(event, module):
    """
    设置用户block为false
    :param event: event
    :param module: 插件模块
    """
    if plugins2block_manager.check_plugin_block_status(module):
        plugin_block_data = plugins2block_manager.get_plugin_block_data(module)
        check_type = plugin_block_data.check_type
        limit_type = plugin_block_data.limit_type
        if not (
            (isinstance(event, GroupMessageEvent) and check_type == "private")
            or (isinstance(event, PrivateMessageEvent) and check_type == "group")
        ):
            block_type_ = event.user_id
            if limit_type == "group" and isinstance(event, GroupMessageEvent):
                block_type_ = event.group_id
            plugins2block_manager.set_false(block_type_, module)


async def send_msg(msg: str, bot: Bot, event: MessageEvent):
    """
    说明:
        发送信息
    参数:
        :param msg: pass
        :param bot: pass
        :param event: pass
    """
    if "[uname]" in msg:
        uname = event.sender.card or event.sender.nickname
        msg = msg.replace("[uname]", uname)
    if "[nickname]" in msg:
        if isinstance(event, GroupMessageEvent):
            nickname = await GroupInfoUser.get_group_member_nickname(
                event.user_id, event.group_id
            )
        else:
            nickname = await FriendUser.get_friend_nickname(event.user_id)
        msg = msg.replace("[nickname]", nickname)
    if "[at]" in msg and isinstance(event, GroupMessageEvent):
        msg = msg.replace("[at]", str(at(event.user_id)))
    try:
        if isinstance(event, GroupMessageEvent):
            status_message_manager.add(event.group_id)
            await bot.send_group_msg(group_id=event.group_id, message=Message(msg))
        else:
            status_message_manager.add(event.user_id)
            await bot.send_private_msg(user_id=event.user_id, message=Message(msg))
    except ActionFailed:
        pass


class ReturnException(Exception):
    pass


@Singleton
class AuthChecker:
    """
    权限检查
    """

    def __init__(self):
        self._flmt = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
        self._flmt_g = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
        self._flmt_s = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))
        self._flmt_c = FreqLimiter(Config.get_config("hook", "CHECK_NOTICE_INFO_CD"))

    async def auth(self, matcher: Matcher, bot: Bot, event: Event):
        """
        说明:
            权限检查
        参数:
            :param matcher: matcher
            :param bot: bot
            :param event: event
        """
        try:
            plugin_name = matcher.plugin_name
            cost_gold = await self.auth_cost(plugin_name, bot, event)
            await self.auth_basic(plugin_name, bot, event)
            self.auth_group(plugin_name, bot, event)
            await self.auth_admin(plugin_name, matcher, bot, event)
            await self.auth_plugin(plugin_name, matcher, bot, event)
            await self.auth_limit(plugin_name, bot, event)
            if cost_gold and str(event.user_id) not in bot.config.superusers:
                await BagUser.spend_gold(event.user_id, event.group_id, cost_gold)
        except ReturnException:
            return

    async def auth_limit(self, plugin_name: str, bot: Bot, event: Event):
        """
        说明:
            插件限制
        参数:
            :param plugin_name: 模块名
            :param bot: bot
            :param event: event
        """
        if plugins2cd_manager.check_plugin_cd_status(plugin_name):
            plugin_cd_data = plugins2cd_manager.get_plugin_cd_data(plugin_name)
            check_type = plugin_cd_data.check_type
            limit_type = plugin_cd_data.limit_type
            msg = plugin_cd_data.rst
            if (
                (isinstance(event, PrivateMessageEvent) and check_type == "private")
                or (isinstance(event, GroupMessageEvent) and check_type == "group")
                or plugins2cd_manager.get_plugin_data(plugin_name).check_type == "all"
            ):
                cd_type_ = event.user_id
                if limit_type == "group" and isinstance(event, GroupMessageEvent):
                    cd_type_ = event.group_id
                if not plugins2cd_manager.check(plugin_name, cd_type_):
                    if msg:
                        await send_msg(msg, bot, event)
                    raise IgnoredException(f"{plugin_name} 正在cd中...")
                else:
                    plugins2cd_manager.start_cd(plugin_name, cd_type_)
        # Block
        if plugins2block_manager.check_plugin_block_status(plugin_name):
            plugin_block_data = plugins2block_manager.get_plugin_block_data(plugin_name)
            check_type = plugin_block_data.check_type
            limit_type = plugin_block_data.limit_type
            msg = plugin_block_data.rst
            if (
                (isinstance(event, PrivateMessageEvent) and check_type == "private")
                or (isinstance(event, GroupMessageEvent) and check_type == "group")
                or check_type == "all"
            ):
                block_type_ = event.user_id
                if limit_type == "group" and isinstance(event, GroupMessageEvent):
                    block_type_ = event.group_id
                if plugins2block_manager.check(block_type_, plugin_name):
                    if msg:
                        await send_msg(msg, bot, event)
                    raise IgnoredException(f"{event.user_id}正在调用{plugin_name}....")
                else:
                    plugins2block_manager.set_true(block_type_, plugin_name)
        # Count
        if (
            plugins2count_manager.check_plugin_count_status(plugin_name)
            and event.user_id not in bot.config.superusers
        ):
            plugin_count_data = plugins2count_manager.get_plugin_count_data(plugin_name)
            limit_type = plugin_count_data.limit_type
            msg = plugin_count_data.rst
            count_type_ = event.user_id
            if limit_type == "group" and isinstance(event, GroupMessageEvent):
                count_type_ = event.group_id
            if not plugins2count_manager.check(plugin_name, count_type_):
                if msg:
                    await send_msg(msg, bot, event)
                raise IgnoredException(f"{plugin_name} count次数限制...")
            else:
                plugins2count_manager.increase(plugin_name, count_type_)

    async def auth_plugin(self, plugin_name: str, matcher: Matcher, bot: Bot, event: Event):
        """
        说明:
            插件状态
        参数:
            :param plugin_name: 模块名
            :param matcher: matcher
            :param bot: bot
            :param event: event
        """
        if plugin_name in plugins2settings_manager.keys() and matcher.priority not in [
            1,
            999,
        ]:
            # 戳一戳单独判断
            if (
                isinstance(event, GroupMessageEvent)
                or isinstance(event, PokeNotifyEvent)
                or matcher.plugin_name in other_limit_plugins
            ):
                if status_message_manager.get(event.group_id) is None:
                    status_message_manager.delete(event.group_id)
                if plugins2settings_manager[
                    plugin_name
                ].level > group_manager.get_group_level(event.group_id):
                    try:
                        if (
                            self._flmt_g.check(event.user_id)
                            and plugin_name not in ignore_rst_module
                        ):
                            self._flmt_g.start_cd(event.user_id)
                            await bot.send_group_msg(
                                group_id=event.group_id, message="群权限不足..."
                            )
                    except ActionFailed:
                        pass
                    if event.is_tome():
                        status_message_manager.add(event.group_id)
                    set_block_limit_false(event, plugin_name)
                    raise IgnoredException("群权限不足")
                # 插件状态
                if not group_manager.get_plugin_status(plugin_name, event.group_id):
                    try:
                        if plugin_name not in ignore_rst_module and self._flmt_s.check(
                            event.group_id
                        ):
                            self._flmt_s.start_cd(event.group_id)
                            await bot.send_group_msg(
                                group_id=event.group_id, message="该群未开启此功能.."
                            )
                    except ActionFailed:
                        pass
                    if event.is_tome():
                        status_message_manager.add(event.group_id)
                    set_block_limit_false(event, plugin_name)
                    raise IgnoredException("未开启此功能...")
                # 管理员禁用
                if not group_manager.get_plugin_status(
                    f"{plugin_name}:super", event.group_id
                ):
                    try:
                        if (
                            self._flmt_s.check(event.group_id)
                            and plugin_name not in ignore_rst_module
                        ):
                            self._flmt_s.start_cd(event.group_id)
                            await bot.send_group_msg(
                                group_id=event.group_id, message="管理员禁用了此群该功能..."
                            )
                    except ActionFailed:
                        pass
                    if event.is_tome():
                        status_message_manager.add(event.group_id)
                    set_block_limit_false(event, plugin_name)
                    raise IgnoredException("管理员禁用了此群该功能...")
                # 群聊禁用
                if not plugins_manager.get_plugin_status(
                    plugin_name, block_type="group"
                ):
                    try:
                        if (
                            self._flmt_c.check(event.group_id)
                            and plugin_name not in ignore_rst_module
                        ):
                            self._flmt_c.start_cd(event.group_id)
                            await bot.send_group_msg(
                                group_id=event.group_id, message="该功能在群聊中已被禁用..."
                            )
                    except ActionFailed:
                        pass
                    if event.is_tome():
                        status_message_manager.add(event.group_id)
                    set_block_limit_false(event, plugin_name)
                    raise IgnoredException("该插件在群聊中已被禁用...")
            else:
                # 私聊禁用
                if not plugins_manager.get_plugin_status(
                    plugin_name, block_type="private"
                ):
                    try:
                        if self._flmt_c.check(event.user_id):
                            self._flmt_c.start_cd(event.user_id)
                            await bot.send_private_msg(
                                user_id=event.user_id, message="该功能在私聊中已被禁用..."
                            )
                    except ActionFailed:
                        pass
                    if event.is_tome():
                        status_message_manager.add(event.user_id)
                    set_block_limit_false(event, plugin_name)
                    raise IgnoredException("该插件在私聊中已被禁用...")
            # 维护
            if not plugins_manager.get_plugin_status(plugin_name, block_type="all"):
                if isinstance(
                    event, GroupMessageEvent
                ) and group_manager.check_group_is_white(event.group_id):
                    raise ReturnException()
                try:
                    if isinstance(event, GroupMessageEvent):
                        if (
                            self._flmt_c.check(event.group_id)
                            and plugin_name not in ignore_rst_module
                        ):
                            self._flmt_c.start_cd(event.group_id)
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
                set_block_limit_false(event, plugin_name)
                raise IgnoredException("此功能正在维护...")

    async def auth_admin(self, plugin_name: str, matcher: Matcher, bot: Bot, event: Event):
        """
        说明:
            管理员命令 个人权限
        参数:
            :param plugin_name: 模块名
            :param matcher: matcher
            :param bot: bot
            :param event: event
        """
        if plugin_name in admin_manager.keys() and matcher.priority not in [1, 999]:
            if isinstance(event, GroupMessageEvent):
                # 个人权限
                if (
                    not await LevelUser.check_level(
                        event.user_id,
                        event.group_id,
                        admin_manager.get_plugin_level(plugin_name),
                    )
                    and admin_manager.get_plugin_level(plugin_name) > 0
                ):
                    try:
                        if self._flmt.check(event.user_id):
                            self._flmt.start_cd(event.user_id)
                            await bot.send_group_msg(
                                group_id=event.group_id,
                                message=f"{at(event.user_id)}你的权限不足喔，该功能需要的权限等级："
                                f"{admin_manager.get_plugin_level(plugin_name)}",
                            )
                    except ActionFailed:
                        pass
                    set_block_limit_false(event, plugin_name)
                    if event.is_tome():
                        status_message_manager.add(event.group_id)
                    raise IgnoredException("权限不足")
            else:
                if not await LevelUser.check_level(
                    event.user_id, 0, admin_manager.get_plugin_level(plugin_name)
                ):
                    try:
                        await bot.send_private_msg(
                            user_id=event.user_id,
                            message=f"你的权限不足喔，该功能需要的权限等级：{admin_manager.get_plugin_level(plugin_name)}",
                        )
                    except ActionFailed:
                        pass
                    set_block_limit_false(event, plugin_name)
                    if event.is_tome():
                        status_message_manager.add(event.user_id)
                    raise IgnoredException("权限不足")

    def auth_group(self, plugin_name: str, bot: Bot, event: Event):
        """
        说明:
            群黑名单检测 群总开关检测
        参数:
            :param plugin_name: 模块名
            :param bot: bot
            :param event: event
        """
        if isinstance(event, GroupMessageEvent) or plugin_name in other_limit_plugins:
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

    async def auth_basic(self, plugin_name: str, bot: Bot, event: Event):
        """
        说明:
            检测是否满足超级用户权限，是否被ban等
        参数:
            :param plugin_name: 模块名
            :param bot: bot
            :param event: event
        """
        try:
            if (
                (
                    not isinstance(event, MessageEvent)
                    and plugin_name not in other_limit_plugins
                )
                or await BanUser.is_ban(event.user_id)
                and str(event.user_id) not in bot.config.superusers
            ) or (
                str(event.user_id) in bot.config.superusers
                and plugins2settings_manager.get_plugin_data(plugin_name)
                and not plugins2settings_manager.get_plugin_data(
                    plugin_name
                ).limit_superuser
            ):
                raise ReturnException()
            _plugin = nonebot.plugin.get_plugin(plugin_name)
            _module = _plugin.module
            _plugin_name = _module.__getattribute__("__zx_plugin_name__")
            if (
                "[superuser]" in _plugin_name.lower()
                and str(event.user_id) in bot.config.superusers
            ):
                raise ReturnException()
        except AttributeError:
            pass

    async def auth_cost(self, plugin_name: str, bot: Bot, event: Event) -> int:
        """
        说明:
            检测是否满足金币条件
        参数:
            :param plugin_name: 模块名
            :param bot: bot
            :param event: event
        """
        cost_gold = 0
        if isinstance(event, GroupMessageEvent) and (
            psm := plugins2settings_manager.get_plugin_data(plugin_name)
        ):
            if psm.cost_gold > 0:
                if (
                    await BagUser.get_gold(event.user_id, event.group_id)
                    < psm.cost_gold
                ):
                    await send_msg(f"金币不足..该功能需要{psm.cost_gold}金币..", bot, event)
                    raise IgnoredException(f"{plugin_name} 金币限制...")
                # 当插件不阻塞超级用户时，超级用户提前扣除金币
                if (
                    str(event.user_id) in bot.config.superusers
                    and not psm.limit_superuser
                ):
                    await BagUser.spend_gold(
                        event.user_id, event.group_id, psm.cost_gold
                    )
                await UserShopGoldLog.add_shop_log(
                    event.user_id, event.group_id, 2, plugin_name, psm.cost_gold, 1
                )
                cost_gold = psm.cost_gold
        return cost_gold
