from typing import Dict
from unittest import result

from nonebot.adapters import Bot, Event
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_saa import Mention, MessageFactory, Text
from nonebot_plugin_session import EventSession
from pydantic import BaseModel

from zhenxun.configs.config import Config
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.level_user import LevelUser
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.plugin_limit import PluginLimit
from zhenxun.models.user_console import UserConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import (
    BlockType,
    GoldHandle,
    LimitWatchType,
    PluginLimitType,
    PluginType,
)
from zhenxun.utils.exception import InsufficientGold
from zhenxun.utils.utils import CountLimiter, FreqLimiter, UserBlockLimiter


class Limit(BaseModel):

    limit: PluginLimit
    limiter: FreqLimiter | UserBlockLimiter | CountLimiter

    class Config:
        arbitrary_types_allowed = True


class LimitManage:

    add_module = []

    cd_limit: Dict[str, Limit] = {}
    block_limit: Dict[str, Limit] = {}
    count_limit: Dict[str, Limit] = {}

    @classmethod
    def add_limit(cls, limit: PluginLimit):
        """添加限制

        参数:
            limit: PluginLimit
        """
        if limit.module not in cls.add_module:
            cls.add_module.append(limit.module)
            if limit.limit_type == PluginLimitType.BLOCK:
                cls.block_limit[limit.module] = Limit(
                    limit=limit, limiter=UserBlockLimiter()
                )
            elif limit.limit_type == PluginLimitType.CD:
                cls.cd_limit[limit.module] = Limit(
                    limit=limit, limiter=FreqLimiter(limit.cd)
                )
            elif limit.limit_type == PluginLimitType.COUNT:
                cls.count_limit[limit.module] = Limit(
                    limit=limit, limiter=CountLimiter(limit.max_count)
                )

    @classmethod
    def unblock(
        cls, module: str, user_id: str, group_id: str | None, channel_id: str | None
    ):
        """解除插件block

        参数:
            module: 模块名
            user_id: 用户id
            group_id: 群组id
            channel_id: 频道id
        """
        if limit_model := cls.block_limit.get(module):
            limit = limit_model.limit
            limiter: UserBlockLimiter = limit_model.limiter  # type: ignore
            key_type = user_id
            if group_id and limit.watch_type == LimitWatchType.GROUP:
                key_type = channel_id or group_id
            limiter.set_false(key_type)

    @classmethod
    async def check(
        cls,
        module: str,
        user_id: str,
        group_id: str | None,
        channel_id: str | None,
        session: EventSession,
    ):
        """检测限制

        参数:
            module: 模块名
            user_id: 用户id
            group_id: 群组id
            channel_id: 频道id
            session: Session

        异常:
            IgnoredException: IgnoredException
        """
        if limit_model := cls.cd_limit.get(module):
            await cls.__check(limit_model, user_id, group_id, channel_id, session)
        if limit_model := cls.block_limit.get(module):
            await cls.__check(limit_model, user_id, group_id, channel_id, session)
        if limit_model := cls.count_limit.get(module):
            await cls.__check(limit_model, user_id, group_id, channel_id, session)

    @classmethod
    async def __check(
        cls,
        limit_model: Limit,
        user_id: str,
        group_id: str | None,
        channel_id: str | None,
        session: EventSession,
    ):
        """检测限制

        参数:
            limit_model: Limit
            user_id: 用户id
            group_id: 群组id
            channel_id: 频道id
            session: Session

        异常:
            IgnoredException: IgnoredException
        """
        if limit_model:
            limit = limit_model.limit
            limiter = limit_model.limiter
            is_limit = (
                LimitWatchType.ALL
                or (group_id and limit.watch_type == LimitWatchType.GROUP)
                or (not group_id and limit.watch_type == LimitWatchType.USER)
            )
            key_type = user_id
            if group_id and limit.watch_type == LimitWatchType.GROUP:
                key_type = channel_id or group_id
            if is_limit and not limiter.check(key_type):
                if limit.result:
                    await Text(limit.result).send()
                logger.debug(
                    f"{limit.module}({limit.limit_type}) 正在限制中...",
                    "HOOK",
                    session=session,
                )
                raise IgnoredException(f"{limit.module} 正在限制中...")
            else:
                if isinstance(limiter, FreqLimiter):
                    limiter.start_cd(key_type)
                if isinstance(limiter, UserBlockLimiter):
                    limiter.set_true(key_type)
                if isinstance(limiter, CountLimiter):
                    limiter.increase(key_type)


class IsSuperuserException(Exception):
    pass


class AuthChecker:
    """
    权限检查
    """

    def __init__(self):
        check_notice_info_cd = Config.get_config("hook", "CHECK_NOTICE_INFO_CD")
        if check_notice_info_cd is None or check_notice_info_cd < 0:
            raise ValueError("模块: [hook], 配置项: [CHECK_NOTICE_INFO_CD] 为空或小于0")
        self._flmt = FreqLimiter(check_notice_info_cd)
        self._flmt_g = FreqLimiter(check_notice_info_cd)
        self._flmt_s = FreqLimiter(check_notice_info_cd)
        self._flmt_c = FreqLimiter(check_notice_info_cd)

    async def auth(
        self,
        matcher: Matcher,
        bot: Bot,
        session: EventSession,
        message: UniMsg,
    ):
        """权限检查

        参数:
            matcher: matcher
            bot: bot
            session: EventSession
            message: UniMsg
        """
        is_ignore = False
        cost_gold = 0
        user_id = session.id1
        group_id = session.id3
        channel_id = session.id2
        if not group_id:
            group_id = channel_id
            channel_id = None
        if user_id and matcher.plugin and (module := matcher.plugin.name):
            user = await UserConsole.get_user(user_id, session.platform)
            if plugin := await PluginInfo.get_or_none(module=module):
                if plugin.plugin_type == PluginType.HIDDEN:
                    return
                try:
                    cost_gold = await self.auth_cost(user, plugin, session)
                    if session.id1 in bot.config.superusers:
                        if plugin.plugin_type == PluginType.SUPERUSER:
                            raise IsSuperuserException()
                        if not plugin.limit_superuser:
                            cost_gold = 0
                            raise IsSuperuserException()
                    await self.auth_group(plugin, session, message)
                    await self.auth_admin(plugin, session)
                    await self.auth_plugin(plugin, session)
                    await self.auth_limit(plugin, session)
                except IsSuperuserException:
                    logger.debug(
                        f"超级用户或被ban跳过权限检测...", "HOOK", session=session
                    )
                except IgnoredException:
                    is_ignore = True
                    LimitManage.unblock(
                        matcher.plugin.name, user_id, group_id, channel_id
                    )
        if cost_gold and user_id:
            """花费金币"""
            try:
                await UserConsole.reduce_gold(
                    user_id,
                    cost_gold,
                    GoldHandle.PLUGIN,
                    matcher.plugin.name if matcher.plugin else "",
                    session.platform,
                )
            except InsufficientGold:
                if u := await UserConsole.get_user(user_id):
                    u.gold = 0
                    await u.save(update_fields=["gold"])
            logger.debug(f"调用功能花费金币: {cost_gold}", "HOOK", session=session)
        if is_ignore:
            raise IgnoredException("权限检测 ignore")

    async def auth_limit(self, plugin: PluginInfo, session: EventSession):
        """插件限制

        参数:
            plugin: PluginInfo
            session: EventSession
        """
        user_id = session.id1
        group_id = session.id3
        channel_id = session.id2
        if not group_id:
            group_id = channel_id
            channel_id = None
        limit_list: list[PluginLimit] = await plugin.plugin_limit.all()  # type: ignore
        for limit in limit_list:
            LimitManage.add_limit(limit)
        if user_id:
            await LimitManage.check(
                plugin.module, user_id, group_id, channel_id, session
            )

    async def auth_plugin(self, plugin: PluginInfo, session: EventSession):
        """插件状态

        参数:
            plugin: PluginInfo
            session: EventSession
        """
        user_id = session.id1
        group_id = session.id3
        channel_id = session.id2
        if not group_id:
            group_id = channel_id
            channel_id = None
        if user_id:
            if group_id:
                if await GroupConsole.is_super_block_plugin(
                    group_id, plugin.module, channel_id
                ):
                    """超级用户群组插件状态"""
                    if self._flmt_s.check(group_id or user_id):
                        self._flmt_s.start_cd(group_id or user_id)
                        await Text("超级管理员禁用了该群此功能...").send(reply=True)
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 超级管理员禁用了该群此功能...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("超级管理员禁用了该群此功能...")
                if await GroupConsole.is_block_plugin(
                    group_id, plugin.module, channel_id
                ):
                    """群组插件状态"""
                    if self._flmt_s.check(group_id or user_id):
                        self._flmt_s.start_cd(group_id or user_id)
                        await Text("该群未开启此功能...").send(reply=True)
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 未开启此功能...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("该群未开启此功能...")
                if not plugin.status and plugin.block_type == BlockType.GROUP:
                    """全局群组禁用"""
                    try:
                        if self._flmt_c.check(group_id):
                            self._flmt_c.start_cd(group_id)
                            await Text("该功能在群组中已被禁用...").send(reply=True)
                    except Exception as e:
                        logger.error(
                            "auth_plugin 发送消息失败", "HOOK", session=session, e=e
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 该插件在群组中已被禁用...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("该插件在群组中已被禁用...")
            else:
                if not plugin.status and plugin.block_type == BlockType.PRIVATE:
                    """全局私聊禁用"""
                    try:
                        if self._flmt_c.check(user_id):
                            self._flmt_c.start_cd(user_id)
                            await Text("该功能在私聊中已被禁用...").send()
                    except Exception as e:
                        logger.error(
                            "auth_admin 发送消息失败", "HOOK", session=session, e=e
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 该插件在私聊中已被禁用...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("该插件在私聊中已被禁用...")
            if not plugin.status and plugin.block_type == BlockType.ALL:
                """全局状态"""
                if group_id:
                    if await GroupConsole.is_super_group(group_id, channel_id):
                        raise IsSuperuserException()
                if self._flmt_s.check(group_id or user_id):
                    self._flmt_s.start_cd(group_id or user_id)
                    await Text("全局未开启此功能...").send()
                logger.debug(
                    f"{plugin.name}({plugin.module}) 全局未开启此功能...",
                    "HOOK",
                    session=session,
                )
                raise IgnoredException("全局未开启此功能...")

    async def auth_admin(self, plugin: PluginInfo, session: EventSession):
        """管理员命令 个人权限

        参数:
            plugin: PluginInfo
            session: EventSession
        """
        user_id = session.id1
        group_id = session.id3 or session.id2
        if user_id and plugin.admin_level:
            if group_id:
                if not await LevelUser.check_level(
                    user_id, group_id, plugin.admin_level
                ):
                    try:
                        if self._flmt.check(user_id):
                            self._flmt.start_cd(user_id)
                            await MessageFactory(
                                [
                                    Mention(user_id),
                                    Text(
                                        f"你的权限不足喔，该功能需要的权限等级: {plugin.admin_level}"
                                    ),
                                ]
                            ).send(reply=True)
                    except Exception as e:
                        logger.error(
                            "auth_admin 发送消息失败", "HOOK", session=session, e=e
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 管理员权限不足...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("管理员权限不足...")
            else:
                if not await LevelUser.check_level(user_id, None, plugin.admin_level):
                    try:
                        await Text(
                            f"你的权限不足喔，该功能需要的权限等级: {plugin.admin_level}"
                        ).send()
                    except Exception as e:
                        logger.error(
                            "auth_admin 发送消息失败", "HOOK", session=session, e=e
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 管理员权限不足...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("权限不足")

    async def auth_group(
        self, plugin: PluginInfo, session: EventSession, message: UniMsg
    ):
        """群黑名单检测 群总开关检测

        参数:
            plugin: PluginInfo
            session: EventSession
            message: UniMsg
        """
        if group_id := session.id3 or session.id2:
            text = message.extract_plain_text()
            group = await GroupConsole.get_or_none(
                group_id=group_id, channel_id__isnull=True
            )
            if not group:
                """群不存在"""
                raise IgnoredException("群不存在")
            if group.level < 0:
                """群权限小于0"""
                logger.debug(
                    f"{plugin.name}({plugin.module}) 群黑名单, 群权限-1...",
                    "HOOK",
                    session=session,
                )
                raise IgnoredException("群黑名单")
            if not group.status:
                """群休眠"""
                if text.strip() != "醒来":
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 功能总开关关闭状态...",
                        "HOOK",
                        session=session,
                    )
                    raise IgnoredException("功能总开关关闭状态")

    async def auth_cost(
        self, user: UserConsole, plugin: PluginInfo, session: EventSession
    ) -> int:
        """检测是否满足金币条件

        参数:
            user: UserConsole
            plugin: PluginInfo
            session: EventSession

        返回:
            int: 需要消耗的金币
        """
        if user.gold < plugin.cost_gold:
            """插件消耗金币不足"""
            try:
                await Text(f"金币不足..该功能需要{plugin.cost_gold}金币..").send()
            except Exception as e:
                logger.error("auth_cost 发送消息失败", "HOOK", session=session, e=e)
            logger.debug(
                f"{plugin.name}({plugin.module}) 金币限制..该功能需要{plugin.cost_gold}金币..",
                "HOOK",
                session=session,
            )
            raise IgnoredException(f"{plugin.name}({plugin.module}) 金币限制...")
        return plugin.cost_gold


checker = AuthChecker()
