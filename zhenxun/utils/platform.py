from nonebot.adapters import Bot
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.dodo import Bot as DodoBot
from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot

from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger


class PlatformManage:

    @classmethod
    async def update_group(cls, bot: Bot) -> int:
        """更新群组信息

        参数:
            bot: Bot

        返回:
            int: 更新个数
        """
        create_list = []
        group_list, platform = await cls.__get_group_list(bot)
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
    async def __get_group_list(cls, bot: Bot) -> tuple[list[GroupConsole], str]:
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
        friend_list, platform = await cls.__get_friend_list(bot)
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
    async def __get_friend_list(cls, bot: Bot) -> tuple[list[FriendUser], str]:
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
