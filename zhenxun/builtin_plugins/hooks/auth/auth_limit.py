from typing import ClassVar

from nonebot.exception import IgnoredException
from nonebot_plugin_uninfo import Uninfo
from pydantic import BaseModel

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.plugin_limit import PluginLimit
from zhenxun.services.log import logger
from zhenxun.utils.enum import LimitWatchType, PluginLimitType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.utils import CountLimiter, FreqLimiter, UserBlockLimiter


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
        session: Uninfo,
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
        session: Uninfo,
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


async def auth_limit(plugin: PluginInfo, session: Uninfo):
    """插件限制

    参数:
        plugin: PluginInfo
        session: Uninfo
    """
    user_id = session.user.id
    group_id = None
    channel_id = None
    if session.group:
        if session.group.parent:
            group_id = session.group.parent.id
            channel_id = session.group.id
        else:
            group_id = session.group.id
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
        await LimitManage.check(plugin.module, user_id, group_id, channel_id, session)
