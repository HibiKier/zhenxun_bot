import nonebot_plugin_alconna as alc
from nonebot.adapters import Bot
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.dodo import Bot as DodoBot
from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_saa import (
    Image,
    MessageFactory,
    TargetDoDoChannel,
    TargetQQGroup,
    Text,
)
from nonebot_plugin_session import EventSession
from pydantic import BaseModel

from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger


class GroupChannel(BaseModel):

    group_id: str
    """群组id"""
    channel_id: str | None = None
    """频道id"""


class BroadcastManage:

    @classmethod
    async def send(
        cls, bot: Bot, message: UniMsg, session: EventSession
    ) -> tuple[int, int]:
        """发送广播消息

        参数:
            bot: Bot
            message: 消息内容
            session: Session

        返回:
            tuple[int, int]: 发送成功的群组数量, 发送失败的群组数量
        """
        message_list = []
        for msg in message:
            if isinstance(msg, alc.Image) and msg.url:
                message_list.append(Image(msg.url))
            elif isinstance(msg, alc.Text):
                message_list.append(Text(msg.text))
        if group_list := await cls.__get_group_list(bot):
            error_count = 0
            for group in group_list:
                try:
                    if not await GroupConsole.is_block_task(
                        group.group_id, "broadcast", group.channel_id
                    ):
                        if isinstance(bot, (v11Bot, v12Bot)):
                            target = TargetQQGroup(group_id=int(group.group_id))
                        elif isinstance(bot, DodoBot):
                            target = TargetDoDoChannel(channel_id=group.channel_id)  # type: ignore
                        await MessageFactory(message_list).send_to(target, bot)
                        logger.debug(
                            "发送成功",
                            "广播",
                            session=session,
                            target=f"{group.group_id}:{group.channel_id}",
                        )
                except Exception as e:
                    error_count += 1
                    logger.error(
                        "发送失败",
                        "广播",
                        session=session,
                        target=f"{group.group_id}:{group.channel_id}",
                        e=e,
                    )
            return len(group_list) - error_count, error_count
        return 0, 0

    @classmethod
    async def __get_group_list(cls, bot: Bot) -> list[GroupChannel]:
        """获取群组id列表

        参数:
            bot: Bot

        返回:
            list[str]: 群组id列表
        """
        if isinstance(bot, (v11Bot, v12Bot)):
            group_list = await bot.get_group_list()
            return [GroupChannel(group_id=str(g["group_id"])) for g in group_list]
        if isinstance(bot, DodoBot):
            island_list = await bot.get_island_list()
            source_id_list = [
                g.island_source_id for g in island_list if g.island_source_id
            ]
            channel_id_list = []
            for id in source_id_list:
                channel_list = await bot.get_channel_list(island_source_id=id)
                channel_id_list += [
                    GroupChannel(group_id=id, channel_id=c.channel_id)
                    for c in channel_list
                ]
            return channel_id_list
        if isinstance(bot, KaiheilaBot):
            # TODO: kaiheila获取群组列表
            pass
            # group_list = await bot.guild_list()
            # if group_list.guilds:
            #     return [g.open_id for g in group_list.guilds if g.open_id]
        if isinstance(bot, DiscordBot):
            # TODO: discord获取群组列表
            pass
        return []
