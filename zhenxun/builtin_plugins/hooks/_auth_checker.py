from typing import ClassVar

from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot_plugin_alconna import At, UniMsg
from nonebot_plugin_session import EventSession
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError

from zhenxun.configs.config import Config
from zhenxun.models.bot_console import BotConsole
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
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import CountLimiter, FreqLimiter, UserBlockLimiter

base_config = Config.get("hook")


class Limit(BaseModel):
    limit: PluginLimit
    limiter: FreqLimiter | UserBlockLimiter | CountLimiter

    class Config:
        arbitrary_types_allowed = True


class LimitManage:
    add_module: ClassVar[list] = []

    cd_limit: ClassVar[dict[str, Limit]] = {}
    block_limit: ClassVar[dict[str, Limit]] = {}
    count_limit: ClassVar[dict[str, Limit]] = {}

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
            logger.debug(
                f"解除对象: {key_type} 的block限制",
                "AuthChecker",
                session=user_id,
                group_id=group_id,
            )
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
        limit_model: Limit | None,
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
        if not limit_model:
            return
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
                await MessageUtils.build_message(limit.result).send()
            logger.debug(
                f"{limit.module}({limit.limit_type}) 正在限制中...",
                "AuthChecker",
                session=session,
            )
            raise IgnoredException(f"{limit.module} 正在限制中...")
        else:
            logger.debug(
                f"开始进行限制 {limit.module}({limit.limit_type})...",
                "AuthChecker",
                session=user_id,
                group_id=group_id,
            )
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

    def is_send_limit_message(self, plugin: PluginInfo, sid: str) -> bool:
        """是否发送提示消息

        参数:
            plugin: PluginInfo

        返回:
            bool: 是否发送提示消息
        """
        if not base_config.get("IS_SEND_TIP_MESSAGE"):
            return False
        if plugin.plugin_type == PluginType.DEPENDANT:
            return False
        return plugin.module != "ai" if self._flmt_s.check(sid) else False

    async def auth(
        self,
        matcher: Matcher,
        event: Event,
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
        if matcher.type == "notice" and not isinstance(event, PokeNotifyEvent):
            """过滤除poke外的notice"""
            return
        if user_id and matcher.plugin and (module_path := matcher.plugin.module_name):
            try:
                user = await UserConsole.get_user(user_id, session.platform)
            except IntegrityError as e:
                logger.debug(
                    "重复创建用户，已跳过该次权限...",
                    "AuthChecker",
                    session=session,
                    e=e,
                )
                return
            if plugin := await PluginInfo.get_or_none(module_path=module_path):
                if plugin.plugin_type == PluginType.HIDDEN:
                    logger.debug(
                        f"插件: {plugin.name}:{plugin.module} "
                        "为HIDDEN，已跳过权限检查..."
                    )
                    return
                try:
                    cost_gold = await self.auth_cost(user, plugin, session)
                    if session.id1 in bot.config.superusers:
                        if plugin.plugin_type == PluginType.SUPERUSER:
                            raise IsSuperuserException()
                        if not plugin.limit_superuser:
                            cost_gold = 0
                            raise IsSuperuserException()
                    await self.auth_bot(plugin, bot.self_id)
                    await self.auth_group(plugin, session, message)
                    await self.auth_admin(plugin, session)
                    await self.auth_plugin(plugin, session, event)
                    await self.auth_limit(plugin, session)
                except IsSuperuserException:
                    logger.debug(
                        "超级用户或被ban跳过权限检测...", "AuthChecker", session=session
                    )
                except IgnoredException:
                    is_ignore = True
                    LimitManage.unblock(
                        matcher.plugin.name, user_id, group_id, channel_id
                    )
                except AssertionError as e:
                    is_ignore = True
                    logger.debug("消息无法发送", session=session, e=e)
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
            logger.debug(
                f"调用功能花费金币: {cost_gold}", "AuthChecker", session=session
            )
        if is_ignore:
            raise IgnoredException("权限检测 ignore")

    async def auth_bot(self, plugin: PluginInfo, bot_id: str):
        """机器人权限

        参数:
            plugin: PluginInfo
            bot_id: bot_id
        """
        if not await BotConsole.get_bot_status(bot_id):
            logger.debug("Bot休眠中阻断权限检测...", "AuthChecker")
            raise IgnoredException("BotConsole休眠权限检测 ignore")
        if await BotConsole.is_block_plugin(bot_id, plugin.module):
            logger.debug(
                f"Bot插件 {plugin.name}({plugin.module}) 权限检查结果为关闭...",
                "AuthChecker",
            )
            raise IgnoredException("BotConsole插件权限检测 ignore")

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
        if plugin.module not in LimitManage.add_module:
            limit_list: list[PluginLimit] = await plugin.plugin_limit.filter(
                status=True
            ).all()  # type: ignore
            for limit in limit_list:
                LimitManage.add_limit(limit)
        if user_id:
            await LimitManage.check(
                plugin.module, user_id, group_id, channel_id, session
            )

    async def auth_plugin(
        self, plugin: PluginInfo, session: EventSession, event: Event
    ):
        """插件状态

        参数:
            plugin: PluginInfo
            session: EventSession
        """
        group_id = session.id3
        channel_id = session.id2
        if not group_id:
            group_id = channel_id
            channel_id = None
        if user_id := session.id1:
            is_poke = isinstance(event, PokeNotifyEvent)
            if group_id:
                sid = group_id or user_id
                if await GroupConsole.is_superuser_block_plugin(
                    group_id, plugin.module
                ):
                    """超级用户群组插件状态"""
                    if self.is_send_limit_message(plugin, sid) and not is_poke:
                        self._flmt_s.start_cd(group_id or user_id)
                        await MessageUtils.build_message(
                            "超级管理员禁用了该群此功能..."
                        ).send(reply_to=True)
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 超级管理员禁用了该群此功能...",
                        "AuthChecker",
                        session=session,
                    )
                    raise IgnoredException("超级管理员禁用了该群此功能...")
                if await GroupConsole.is_normal_block_plugin(group_id, plugin.module):
                    """群组插件状态"""
                    if self.is_send_limit_message(plugin, sid) and not is_poke:
                        self._flmt_s.start_cd(group_id or user_id)
                        await MessageUtils.build_message("该群未开启此功能...").send(
                            reply_to=True
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 未开启此功能...",
                        "AuthChecker",
                        session=session,
                    )
                    raise IgnoredException("该群未开启此功能...")
                if plugin.block_type == BlockType.GROUP:
                    """全局群组禁用"""
                    try:
                        if self.is_send_limit_message(plugin, sid) and not is_poke:
                            self._flmt_c.start_cd(group_id)
                            await MessageUtils.build_message(
                                "该功能在群组中已被禁用..."
                            ).send(reply_to=True)
                    except Exception as e:
                        logger.error(
                            "auth_plugin 发送消息失败",
                            "AuthChecker",
                            session=session,
                            e=e,
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 该插件在群组中已被禁用...",
                        "AuthChecker",
                        session=session,
                    )
                    raise IgnoredException("该插件在群组中已被禁用...")
            else:
                sid = user_id
                if plugin.block_type == BlockType.PRIVATE:
                    """全局私聊禁用"""
                    try:
                        if self.is_send_limit_message(plugin, sid) and not is_poke:
                            self._flmt_c.start_cd(user_id)
                            await MessageUtils.build_message(
                                "该功能在私聊中已被禁用..."
                            ).send()
                    except Exception as e:
                        logger.error(
                            "auth_admin 发送消息失败",
                            "AuthChecker",
                            session=session,
                            e=e,
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 该插件在私聊中已被禁用...",
                        "AuthChecker",
                        session=session,
                    )
                    raise IgnoredException("该插件在私聊中已被禁用...")
            if not plugin.status and plugin.block_type == BlockType.ALL:
                """全局状态"""
                if group_id and await GroupConsole.is_super_group(group_id):
                    raise IsSuperuserException()
                logger.debug(
                    f"{plugin.name}({plugin.module}) 全局未开启此功能...",
                    "AuthChecker",
                    session=session,
                )
                if self.is_send_limit_message(plugin, sid) and not is_poke:
                    self._flmt_s.start_cd(group_id or user_id)
                    await MessageUtils.build_message("全局未开启此功能...").send()
                raise IgnoredException("全局未开启此功能...")

    async def auth_admin(self, plugin: PluginInfo, session: EventSession):
        """管理员命令 个人权限

        参数:
            plugin: PluginInfo
            session: EventSession
        """
        user_id = session.id1
        if user_id and plugin.admin_level:
            if group_id := session.id3 or session.id2:
                if not await LevelUser.check_level(
                    user_id, group_id, plugin.admin_level
                ):
                    try:
                        if self._flmt.check(user_id):
                            self._flmt.start_cd(user_id)
                            await MessageUtils.build_message(
                                [
                                    At(flag="user", target=user_id),
                                    f"你的权限不足喔，"
                                    f"该功能需要的权限等级: {plugin.admin_level}",
                                ]
                            ).send(reply_to=True)
                    except Exception as e:
                        logger.error(
                            "auth_admin 发送消息失败",
                            "AuthChecker",
                            session=session,
                            e=e,
                        )
                    logger.debug(
                        f"{plugin.name}({plugin.module}) 管理员权限不足...",
                        "AuthChecker",
                        session=session,
                    )
                    raise IgnoredException("管理员权限不足...")
            elif not await LevelUser.check_level(user_id, None, plugin.admin_level):
                try:
                    await MessageUtils.build_message(
                        f"你的权限不足喔，该功能需要的权限等级: {plugin.admin_level}"
                    ).send()
                except Exception as e:
                    logger.error(
                        "auth_admin 发送消息失败", "AuthChecker", session=session, e=e
                    )
                logger.debug(
                    f"{plugin.name}({plugin.module}) 管理员权限不足...",
                    "AuthChecker",
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
        if not (group_id := session.id3 or session.id2):
            return
        text = message.extract_plain_text()
        group = await GroupConsole.get_group(group_id)
        if not group:
            """群不存在"""
            logger.debug(
                "群组信息不存在...",
                "AuthChecker",
                session=session,
            )
            raise IgnoredException("群不存在")
        if group.level < 0:
            """群权限小于0"""
            logger.debug(
                "群黑名单, 群权限-1...",
                "AuthChecker",
                session=session,
            )
            raise IgnoredException("群黑名单")
        if not group.status:
            """群休眠"""
            if text.strip() != "醒来":
                logger.debug("群休眠状态...", "AuthChecker", session=session)
                raise IgnoredException("群休眠状态")
        if plugin.level > group.level:
            """插件等级大于群等级"""
            logger.debug(
                f"{plugin.name}({plugin.module}) 群等级限制.."
                f"该功能需要的群等级: {plugin.level}..",
                "AuthChecker",
                session=session,
            )
            raise IgnoredException(f"{plugin.name}({plugin.module}) 群等级限制...")

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
                await MessageUtils.build_message(
                    f"金币不足..该功能需要{plugin.cost_gold}金币.."
                ).send()
            except Exception as e:
                logger.error(
                    "auth_cost 发送消息失败", "AuthChecker", session=session, e=e
                )
            logger.debug(
                f"{plugin.name}({plugin.module}) 金币限制.."
                f"该功能需要{plugin.cost_gold}金币..",
                "AuthChecker",
                session=session,
            )
            raise IgnoredException(f"{plugin.name}({plugin.module}) 金币限制...")
        return plugin.cost_gold


checker = AuthChecker()
