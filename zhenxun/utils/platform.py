import random
from typing import Literal
from collections.abc import Callable, Awaitable

import httpx
import nonebot
from pydantic import BaseModel
from nonebot.adapters import Bot
from nonebot.utils import is_coroutine_callable
from nonebot_plugin_alconna import SupportScope
from nonebot.adapters.dodo import Bot as DodoBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot_plugin_uninfo import Uninfo, get_interface
from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot_plugin_alconna.uniseg import Target, Receipt, UniMessage

from zhenxun.services.log import logger
from zhenxun.configs.config import BotConfig
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.models.friend_user import FriendUser
from zhenxun.utils.exception import NotFindSuperuser
from zhenxun.models.group_console import GroupConsole

driver = nonebot.get_driver()


class UserData(BaseModel):
    name: str
    """昵称"""
    card: str | None = None
    """名片/备注"""
    user_id: str
    """用户id"""
    group_id: str | None = None
    """群组id"""
    role: str | None = None
    """角色"""
    avatar_url: str | None = None
    """头像url"""
    join_time: int | None = None
    """加入时间"""


class PlatformUtils:
    @classmethod
    def is_qbot(cls, session: Uninfo | Bot) -> bool:
        """判断bot是否为qq官bot

        参数:
            session: Uninfo

        返回:
            bool: 是否为官bot
        """
        if isinstance(session, Bot):
            return bool(BotConfig.get_qbot_uid(session.self_id))
        return session.scope == SupportScope.qq_api

    @classmethod
    async def ban_user(cls, bot: Bot, user_id: str, group_id: str, duration: int):
        """禁言

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 群组id
            duration: 禁言时长(分钟)
        """
        if isinstance(bot, v11Bot):
            await bot.set_group_ban(
                group_id=int(group_id),
                user_id=int(user_id),
                duration=duration * 60,
            )

    @classmethod
    async def send_superuser(
        cls,
        bot: Bot,
        message: UniMessage | str,
        superuser_id: str | None = None,
    ) -> Receipt | None:
        """发送消息给超级用户

        参数:
            bot: Bot
            message: 消息
            superuser_id: 指定超级用户id.

        异常:
            NotFindSuperuser: 未找到超级用户id

        返回:
            Receipt | None: Receipt
        """
        if not superuser_id:
            if platform := cls.get_platform(bot):
                if platform_superusers := BotConfig.get_superuser(platform):
                    superuser_id = random.choice(platform_superusers)
                else:
                    raise NotFindSuperuser()
        if isinstance(message, str):
            message = MessageUtils.build_message(message)
        return await cls.send_message(bot, superuser_id, None, message)

    @classmethod
    async def get_group_member_list(cls, bot: Bot, group_id: str) -> list[UserData]:
        """获取群组/频道成员列表

        参数:
            bot: Bot
            group_id: 群组/频道id

        返回:
            list[UserData]: 用户数据列表
        """
        if isinstance(bot, v11Bot):
            if member_list := await bot.get_group_member_list(group_id=int(group_id)):
                return [
                    UserData(
                        name=user["nickname"],
                        card=user["card"],
                        user_id=user["user_id"],
                        group_id=user["group_id"],
                        role=user["role"],
                        join_time=user["join_time"],
                    )
                    for user in member_list
                ]
        if isinstance(bot, v12Bot):
            if member_list := await bot.get_group_member_list(group_id=group_id):
                return [
                    UserData(
                        name=user["user_name"],
                        card=user["user_displayname"],
                        user_id=user["user_id"],
                        group_id=group_id,
                    )
                    for user in member_list
                ]
        if isinstance(bot, DodoBot):
            if result_data := await bot.get_member_list(
                island_source_id=group_id, page_size=100, max_id=0
            ):
                max_id = result_data.max_id
                result_list = result_data.list
                while max_id == 100:
                    result_data = await bot.get_member_list(
                        island_source_id=group_id, page_size=100, max_id=0
                    )
                    result_list += result_data.list
                    max_id = result_data.max_id
                return [
                    UserData(
                        name=user.nick_name,
                        card=user.personal_nick_name,
                        avatar_url=user.avatar_url,
                        user_id=user.dodo_source_id,
                        group_id=user.island_source_id,
                        join_time=int(user.join_time.timestamp()),
                    )
                    for user in result_list
                ]
        if isinstance(bot, KaiheilaBot):
            if result_data := await bot.guild_userList(guild_id=group_id):
                if result_data.users:
                    data_list = []
                    for user in result_data.users:
                        second = None
                        if user.joined_at:
                            second = int(user.joined_at / 1000)
                        data_list.append(
                            UserData(
                                name=user.nickname or "",
                                avatar_url=user.avatar,
                                user_id=user.id_,  # type: ignore
                                group_id=group_id,
                                join_time=second,
                            )
                        )
                    return data_list
        return []

    @classmethod
    async def get_user(
        cls, bot: Bot, user_id: str, group_id: str | None = None
    ) -> UserData | None:
        """获取用户信息

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 群组/频道id.

        返回:
            UserData | None: 用户数据
        """
        if isinstance(bot, v11Bot):
            if group_id:
                if user := await bot.get_group_member_info(
                    group_id=int(group_id), user_id=int(user_id)
                ):
                    return UserData(
                        name=user["nickname"],
                        card=user["card"],
                        user_id=user["user_id"],
                        group_id=user["group_id"],
                        role=user["role"],
                        join_time=user["join_time"],
                    )
            elif friend_list := await bot.get_friend_list():
                for f in friend_list:
                    if f["user_id"] == int(user_id):
                        return UserData(
                            name=f["nickname"],
                            card=f["remark"],
                            user_id=f["user_id"],
                        )
        if isinstance(bot, v12Bot):
            if group_id:
                if user := await bot.get_group_member_info(
                    group_id=group_id, user_id=user_id
                ):
                    return UserData(
                        name=user["user_name"],
                        card=user["user_displayname"],
                        user_id=user["user_id"],
                        group_id=group_id,
                    )
            elif friend_list := await bot.get_friend_list():
                for f in friend_list:
                    if f["user_id"] == int(user_id):
                        return UserData(
                            name=f["user_name"],
                            card=f["user_remark"],
                            user_id=f["user_id"],
                        )
        if isinstance(bot, DodoBot) and group_id:
            if user := await bot.get_member_info(
                island_source_id=group_id, dodo_source_id=user_id
            ):
                return UserData(
                    name=user.nick_name,
                    card=user.personal_nick_name,
                    avatar_url=user.avatar_url,
                    user_id=user.dodo_source_id,
                    group_id=user.island_source_id,
                    join_time=int(user.join_time.timestamp()),
                )
        if isinstance(bot, KaiheilaBot) and group_id:
            if user := await bot.user_view(guild_id=group_id, user_id=user_id):
                second = int(user.joined_at / 1000) if user.joined_at else None
                return UserData(
                    name=user.nickname or "",
                    avatar_url=user.avatar,
                    user_id=user_id,
                    group_id=group_id,
                    join_time=second,
                )
        return None

    @classmethod
    async def get_user_avatar(
        cls, user_id: str, platform: str, appid: str | None = None
    ) -> bytes | None:
        """快捷获取用户头像

        参数:
            user_id: 用户id
            platform: 平台
        """
        url = None
        if platform == "qq":
            if user_id.isdigit():
                url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=160"
            else:
                url = f"https://q.qlogo.cn/qqapp/{appid}/{user_id}/100"
        return await AsyncHttpx.get_content(url) if url else None

    @classmethod
    def get_user_avatar_url(
        cls, user_id: str, platform: str, appid: str | None = None
    ) -> str | None:
        """快捷获取用户头像url

        参数:
            user_id: 用户id
            platform: 平台
        """
        if platform == "qq":
            return (
                f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=160"
                if user_id.isdigit()
                else f"https://q.qlogo.cn/qqapp/{appid}/{user_id}/100"
            )
        else:
            return None

    @classmethod
    async def get_group_avatar(cls, gid: str, platform: str) -> bytes | None:
        """快捷获取用群头像

        参数:
            gid: 群组id
            platform: 平台
        """
        if platform == "qq":
            url = f"http://p.qlogo.cn/gh/{gid}/{gid}/640/"
            async with httpx.AsyncClient() as client:
                for _ in range(3):
                    try:
                        return (await client.get(url)).content
                    except Exception:
                        logger.error(
                            "获取群头像错误", "Util", target=gid, platform=platform
                        )
        return None

    @classmethod
    async def send_message(
        cls,
        bot: Bot,
        user_id: str | None,
        group_id: str | None,
        message: str | UniMessage,
    ) -> Receipt | None:
        """发送消息

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 群组id或频道id
            message: 消息文本

        返回:
            Receipt | None: 是否发送成功
        """
        if target := cls.get_target(bot, user_id, group_id):
            send_message = (
                MessageUtils.build_message(message)
                if isinstance(message, str)
                else message
            )
            return await send_message.send(target=target, bot=bot)
        return None

    @classmethod
    async def update_group(cls, bot: Bot) -> int:
        """更新群组信息

        参数:
            bot: Bot

        返回:
            int: 更新个数
        """
        create_list = []
        update_list = []
        group_list, platform = await cls.get_group_list(bot)
        if group_list:
            db_group = await GroupConsole.all()
            db_group_id = [(group.group_id, group.channel_id) for group in db_group]
            for group in group_list:
                group.platform = platform
                if (group.group_id, group.channel_id) not in db_group_id:
                    create_list.append(group)
                    logger.debug(
                        "群聊信息更新成功",
                        "更新群信息",
                        target=f"{group.group_id}:{group.channel_id}",
                    )
                else:
                    _group = next(
                        g
                        for g in db_group
                        if g.group_id == group.group_id
                        and g.channel_id == group.channel_id
                    )
                    _group.group_name = group.group_name
                    _group.max_member_count = group.max_member_count
                    _group.member_count = group.member_count
                    update_list.append(_group)
        if create_list:
            await GroupConsole.bulk_create(create_list, 10)
        if group_list:
            await GroupConsole.bulk_update(
                update_list, ["group_name", "max_member_count", "member_count"], 10
            )
        return len(create_list)

    @classmethod
    def get_platform(cls, t: Bot | Uninfo) -> str:
        """获取平台

        参数:
            bot: Bot

        返回:
            str | None: 平台
        """
        if isinstance(t, Bot):
            if interface := get_interface(t):
                info = interface.basic_info()
                platform = info["scope"].lower()
                return "qq" if platform.startswith("qq") else platform
        else:
            platform = t.basic["scope"].lower()
            return "qq" if platform.startswith("qq") else platform
        return "unknown"

    @classmethod
    async def get_group_list(cls, bot: Bot) -> tuple[list[GroupConsole], str]:
        """获取群组列表

        参数:
            bot: Bot

        返回:
            tuple[list[GroupConsole], str]: 群组列表, 平台
        """
        if isinstance(bot, v11Bot):
            group_list = await bot.get_group_list()
            return [
                GroupConsole(
                    group_id=str(g["group_id"]),
                    group_name=g["group_name"],
                    max_member_count=g["max_member_count"],
                    member_count=g["member_count"],
                )
                for g in group_list
            ], "qq"
        if isinstance(bot, v12Bot):
            group_list = await bot.get_group_list()
            return [
                GroupConsole(
                    group_id=g.group_id,  # type: ignore
                    user_name=g.group_name,  # type: ignore
                )
                for g in group_list
            ], "qq"
        if isinstance(bot, DodoBot):
            island_list = await bot.get_island_list()
            source_id_list = [
                (g.island_source_id, g.island_name)
                for g in island_list
                if g.island_source_id
            ]
            group_list = []
            for id, name in source_id_list:
                channel_list = await bot.get_channel_list(island_source_id=id)
                group_list.append(GroupConsole(group_id=id, group_name=name))
                group_list += [
                    GroupConsole(
                        group_id=id, group_name=c.channel_name, channel_id=c.channel_id
                    )
                    for c in channel_list
                ]
            return group_list, "dodo"
        if isinstance(bot, KaiheilaBot):
            group_list = []
            guilds = await bot.guild_list()
            if guilds.guilds:
                for guild_id, name in [(g.id_, g.name) for g in guilds.guilds if g.id_]:
                    view = await bot.guild_view(guild_id=guild_id)
                    group_list.append(GroupConsole(group_id=guild_id, group_name=name))
                    if view.channels:
                        group_list += [
                            GroupConsole(
                                group_id=guild_id, group_name=c.name, channel_id=c.id_
                            )
                            for c in view.channels
                            if c.type != 0
                        ]
            return group_list, "kaiheila"
        return [], ""

    @classmethod
    async def update_friend(cls, bot: Bot) -> int:
        """更新好友信息

        参数:
            bot: Bot

        返回:
            int: 更新个数
        """
        create_list = []
        friend_list, platform = await cls.get_friend_list(bot)
        if friend_list:
            user_id_list = await FriendUser.all().values_list("user_id", flat=True)
            for friend in friend_list:
                friend.platform = platform
                if friend.user_id not in user_id_list:
                    create_list.append(friend)
        if create_list:
            await FriendUser.bulk_create(create_list, 10)
        return len(create_list)

    @classmethod
    async def get_friend_list(cls, bot: Bot) -> tuple[list[FriendUser], str]:
        """获取好友列表

        参数:
            bot: Bot

        返回:
            list[FriendUser]: 好友列表
        """
        if isinstance(bot, v11Bot):
            friend_list = await bot.get_friend_list()
            return [
                FriendUser(user_id=str(f["user_id"]), user_name=f["nickname"])
                for f in friend_list
            ], "qq"
        if isinstance(bot, v12Bot):
            friend_list = await bot.get_friend_list()
            return [
                FriendUser(
                    user_id=f.user_id,  # type: ignore
                    user_name=f.user_displayname or f.user_remark or f.user_name,  # type: ignore
                )
                for f in friend_list
            ], "qq"
        # if isinstance(bot, DodoBot):
        #     # TODO: dodo好友列表
        #     pass
        # if isinstance(bot, KaiheilaBot):
        #     # TODO: kaiheila好友列表
        #     pass
        # if isinstance(bot, DiscordBot):
        #     # TODO: discord好友列表
        #     pass
        return [], ""

    @classmethod
    def get_target(
        cls,
        bot: Bot,
        user_id: str | None = None,
        group_id: str | None = None,
        channel_id: str | None = None,
    ):
        """获取发生Target

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 频道id或群组id
            channel_id: 频道id

        返回:
            target: 对应平台Target
        """
        target = None
        if isinstance(bot, v11Bot | v12Bot):
            if group_id:
                target = Target(group_id)
            elif user_id:
                target = Target(user_id, private=True)
        elif isinstance(bot, DodoBot | KaiheilaBot):
            if group_id and channel_id:
                target = Target(channel_id, parent_id=group_id, channel=True)
            elif user_id:
                target = Target(user_id, private=True)
        return target


async def broadcast_group(
    message: str | UniMessage,
    bot: Bot | list[Bot] | None = None,
    bot_id: str | set[str] | None = None,
    ignore_group: set[int] | None = None,
    check_func: Callable[[Bot, str], Awaitable] | None = None,
    log_cmd: str | None = None,
    platform: Literal["qq", "dodo", "kaiheila"] | None = None,
):
    """获取所有Bot或指定Bot对象广播群聊

    参数:
        message: 广播消息内容
        bot: 指定bot对象.
        bot_id: 指定bot id.
        ignore_group: 忽略群聊列表.
        check_func: 发送前对群聊检测方法，判断是否发送.
        log_cmd: 日志标记.
        platform: 指定平台
    """
    if platform and platform not in ["qq", "dodo", "kaiheila"]:
        raise ValueError("指定平台不支持")
    if not message:
        raise ValueError("群聊广播消息不能为空")
    bot_dict = nonebot.get_bots()
    bot_list: list[Bot] = []
    if bot:
        if isinstance(bot, list):
            bot_list = bot
        else:
            bot_list.append(bot)
    elif bot_id:
        _bot_id_list = bot_id
        if isinstance(bot_id, str):
            _bot_id_list = [bot_id]
        for id_ in _bot_id_list:
            if bot_id in bot_dict:
                bot_list.append(bot_dict[bot_id])
            else:
                logger.warning(f"Bot:{id_} 对象未连接或不存在")
    else:
        bot_list = list(bot_dict.values())
    _used_group = []
    for _bot in bot_list:
        try:
            if platform and platform != PlatformUtils.get_platform(_bot):
                continue
            group_list, _ = await PlatformUtils.get_group_list(_bot)
            if group_list:
                for group in group_list:
                    key = f"{group.group_id}:{group.channel_id}"
                    try:
                        if (
                            ignore_group
                            and (
                                group.group_id in ignore_group
                                or group.channel_id in ignore_group
                            )
                        ) or key in _used_group:
                            logger.debug(
                                "广播方法群组重复, 已跳过...",
                                log_cmd,
                                group_id=group.group_id,
                            )
                            continue
                        is_run = False
                        if check_func:
                            if is_coroutine_callable(check_func):
                                is_run = await check_func(_bot, group.group_id)
                            else:
                                is_run = check_func(_bot, group.group_id)
                        if not is_run:
                            logger.debug(
                                "广播方法检测运行方法为 False, 已跳过...",
                                log_cmd,
                                group_id=group.group_id,
                            )
                            continue
                        target = PlatformUtils.get_target(
                            _bot, None, group.group_id, group.channel_id
                        )
                        if target:
                            _used_group.append(key)
                            message_list = message
                            await MessageUtils.build_message(message_list).send(
                                target, _bot
                            )
                            logger.debug("发送成功", log_cmd, target=key)
                        else:
                            logger.warning("target为空", log_cmd, target=key)
                    except Exception as e:
                        logger.error("发送失败", log_cmd, target=key, e=e)
        except Exception as e:
            logger.error(f"Bot: {_bot.self_id} 获取群聊列表失败", command=log_cmd, e=e)
