import hashlib
from dataclasses import dataclass
from typing import Optional, Union

from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import MessageEvent as V11MEvent
from nonebot.adapters.onebot.v12 import Bot as V12Bot
from nonebot.adapters.onebot.v12 import ChannelMessageEvent as V12CMEvent
from nonebot.adapters.onebot.v12 import MessageEvent as V12MEvent

from ..exception import PlatformUnsupportError
from ..utils import download_url


@dataclass
class ImageSource:
    async def get_image(self) -> bytes:
        raise NotImplementedError


@dataclass
class ImageUrl(ImageSource):
    url: str

    async def get_image(self) -> bytes:
        return await download_url(self.url)


@dataclass
class QQAvatar(ImageSource):
    qq: str

    async def get_image(self) -> bytes:
        url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=640"
        data = await download_url(url)
        if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
            url = f"http://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=100"
            data = await download_url(url)
        return data


@dataclass
class UnsupportAvatar(ImageSource):
    platform: str

    async def get_image(self) -> bytes:
        raise PlatformUnsupportError(self.platform)


@dataclass
class QQGuildAvatar(ImageSource):
    """QQ频道 用户头像"""

    bot: V12Bot
    user_id: str
    guild_id: str
    avatar: Optional[str] = None

    async def get_image(self) -> bytes:
        if self.avatar is None:
            user_info = await self.bot.get_guild_member_info(
                guild_id=self.guild_id, user_id=self.user_id
            )
            # 直接这样好了，反正出错了会报错
            url = user_info["qqguild"]["user"]["avatar"]  # type: ignore
        else:
            url = self.avatar
        return await download_url(url)


def user_avatar(
    bot: Union[V11Bot, V12Bot], event: Union[V11MEvent, V12MEvent], user_id: str
) -> ImageSource:
    if isinstance(bot, V11Bot):
        return QQAvatar(qq=user_id)

    assert isinstance(event, V12MEvent)
    platform = bot.platform
    impl = bot.impl
    if platform == "qq":
        return QQAvatar(qq=user_id)
    if (
        platform == "qqguild"
        and impl == "nonebot-plugin-all4one"
        and isinstance(event, V12CMEvent)
    ):
        # 先转成 dict，这样就算以后用扩展模型也不会出错
        event_dict = event.dict()
        if user_id == str(event_dict["qqguild"]["author"]["id"]):
            return QQGuildAvatar(
                bot=bot,
                user_id=user_id,
                guild_id=event.guild_id,
                avatar=event_dict["qqguild"]["author"]["avatar"],
            )
        return QQGuildAvatar(bot=bot, user_id=user_id, guild_id=event.guild_id)

    return UnsupportAvatar(platform)
