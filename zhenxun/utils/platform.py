from typing import Awaitable, Callable, Literal, Set

import nonebot
from nonebot.adapters import Bot
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.dodo import Bot as DodoBot
from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot.utils import is_coroutine_callable
from nonebot_plugin_saa import (
    Image,
    MessageFactory,
    TargetDoDoChannel,
    TargetDoDoPrivate,
    TargetKaiheilaChannel,
    TargetKaiheilaPrivate,
    TargetQQGroup,
    TargetQQPrivate,
    Text,
)

from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger


class PlatformUtils:

    @classmethod
    async def send_message(
        cls,
        bot: Bot,
        user_id: str | None,
        group_id: str | None,
        message: str | Text | MessageFactory | Image,
    ) -> bool:
        """发送消息

        参数:
            bot: Bot
            user_id: 用户id
            group_id: 群组id或频道id
            message: 消息文本

        返回:
            bool: 是否发送成功
        """
        if target := cls.get_target(bot, user_id, group_id):
            send_message = Text(message) if isinstance(message, str) else message
            await send_message.send_to(target, bot)
            return True
        return False

    @classmethod
    async def update_group(cls, bot: Bot) -> int:
        """更新群组信息

        参数:
            bot: Bot

        返回:
            int: 更新个数
        """
        create_list = []
        group_list, platform = await cls.get_group_list(bot)
        if group_list:
            exists_group_list = await GroupConsole.all().values_list(
                "group_id", "channel_id"
            )
            for group in group_list:
                group.platform = platform
                if (group.group_id, group.channel_id) not in exists_group_list:
                    create_list.append(group)
                    logger.debug(
                        "群聊信息更新成功",
                        "更新群信息",
                        target=f"{group.group_id}:{group.channel_id}",
                    )
        if create_list:
            await GroupConsole.bulk_create(create_list, 10)
        return len(create_list)

    @classmethod
    def get_platform(cls, bot: Bot) -> str | None:
        """获取平台

        参数:
            bot: Bot

        返回:
            str | None: 平台
        """
        if isinstance(bot, (v11Bot, v12Bot)):
            return "qq"
        if isinstance(bot, DodoBot):
            return "dodo"
        if isinstance(bot, KaiheilaBot):
            return "kaiheila"
        if isinstance(bot, DiscordBot):
            return "discord"
        return None

    @classmethod
    async def get_group_list(cls, bot: Bot) -> tuple[list[GroupConsole], str]:
        """获取群组列表

        参数:
            bot: Bot

        返回:
            list[GroupConsole]: 群组列表
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
        if isinstance(bot, DiscordBot):
            # TODO: discord群组列表
            pass
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
        if isinstance(bot, DodoBot):
            # TODO: dodo好友列表
            pass
        if isinstance(bot, KaiheilaBot):
            # TODO: kaiheila好友列表
            pass
        if isinstance(bot, DiscordBot):
            # TODO: discord好友列表
            pass
        return [], ""

    @classmethod
    def get_target(
        cls,
        bot: Bot,
        user_id: str | None = None,
        group_id: str | None = None,
    ):
        """获取发生Target

        参数:
            bot: Bot
            group_id: 群组id
            channel_id: 频道id或群组id

        返回:
            target: 对应平台Target
        """
        target = None
        if isinstance(bot, (v11Bot, v12Bot)):
            if group_id:
                target = TargetQQGroup(group_id=int(group_id))
            elif user_id:
                target = TargetQQPrivate(user_id=int(user_id))
        elif isinstance(bot, DodoBot):
            if group_id:
                target = TargetDoDoChannel(channel_id=group_id)
            elif user_id:
                # target = TargetDoDoPrivate(user_id=user_id)
                pass
        elif isinstance(bot, KaiheilaBot):
            if group_id:
                target = TargetKaiheilaChannel(channel_id=group_id)
            elif user_id:
                target = TargetKaiheilaPrivate(user_id=user_id)
        return target


async def broadcast_group(
    message: str | MessageFactory,
    bot: Bot | list[Bot] | None = None,
    bot_id: str | Set[str] | None = None,
    ignore_group: Set[int] | None = None,
    check_func: Callable[[str, str | None], Awaitable] | None = None,
    log_cmd: str | None = None,
    platform: Literal["qq", "dodo", "kaiheila"] | None = None,
):
    """获取所有Bot或指定Bot对象广播群聊

    Args:
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
                            continue
                        is_continue = False
                        if check_func:
                            if is_coroutine_callable(check_func):
                                is_continue = not await check_func(
                                    group.group_id, group.channel_id
                                )
                            else:
                                is_continue = not check_func(
                                    group.group_id, group.channel_id
                                )
                        if is_continue:
                            continue
                        target = PlatformUtils.get_target(
                            _bot, None, group.group_id, group.channel_id
                        )
                        if target:
                            _used_group.append(key)
                            message_list = message
                            if isinstance(message, str):
                                message_list = MessageFactory([Text(message)])
                            await MessageFactory(message_list).send_to(target, _bot)
                            logger.debug("发送成功", log_cmd, target=key)
                        else:
                            logger.warning("target为空", log_cmd, target=key)
                    except Exception as e:
                        logger.error("发送失败", log_cmd, target=key, e=e)
        except Exception as e:
            logger.error(f"Bot: {_bot.self_id} 获取群聊列表失败", command=log_cmd, e=e)
