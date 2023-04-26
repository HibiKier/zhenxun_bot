from dataclasses import dataclass
from typing import TypedDict

from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent as V11GMEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MEvent
from nonebot.adapters.onebot.v12 import Bot as V12Bot
from nonebot.adapters.onebot.v12 import ChannelMessageEvent as V12CMEvent
from nonebot.adapters.onebot.v12 import GroupMessageEvent as V12GMEvent
from nonebot.adapters.onebot.v12 import MessageEvent as V12MEvent


class UserInfo(TypedDict):
    name: str
    gender: str


@dataclass
class User:
    async def get_info(self) -> UserInfo:
        raise NotImplementedError


@dataclass
class V11User(User):
    bot: V11Bot
    event: V11MEvent
    user_id: int

    async def get_info(self) -> UserInfo:
        if isinstance(self.event, V11GMEvent):
            info = await self.bot.get_group_member_info(
                group_id=self.event.group_id, user_id=self.user_id
            )
        else:
            info = await self.bot.get_stranger_info(user_id=self.user_id)
        name = info.get("card", "") or info.get("nickname", "")
        gender = info.get("sex", "")
        return UserInfo(name=name, gender=gender)


@dataclass
class V12User(User):
    bot: V12Bot
    event: V12MEvent
    user_id: str

    async def get_info(self) -> UserInfo:
        if isinstance(self.event, V12GMEvent):
            info = await self.bot.get_group_member_info(
                group_id=self.event.group_id, user_id=self.user_id
            )
        elif isinstance(self.event, V12CMEvent):
            info = await self.bot.get_guild_member_info(
                guild_id=self.event.guild_id, user_id=self.user_id
            )
        else:
            info = await self.bot.get_user_info(user_id=self.user_id)
        name = info.get("user_displayname", "") or info.get("user_name", "")
        gender = "unknown"
        return UserInfo(name=name, gender=gender)
