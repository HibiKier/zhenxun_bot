import asyncio

from nonebot.adapters import Bot

# from nonebot.adapters.discord import Bot as DiscordBot
# from nonebot.adapters.dodo import Bot as DodoBot
# from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot_plugin_session import EventSession
from ruamel.yaml.comments import CommentedSeq

from zhenxun.services.log import logger


class WithdrawManager:
    _data = {}  # noqa: RUF012
    _index = 0

    @classmethod
    def check(cls, session: EventSession, withdraw_time: tuple[int, int]) -> bool:
        """配置项检查

        参数:
            session: Session
            withdraw_time: 配置项数据, (0, 1)

        返回:
            bool: 是否允许撤回
        """
        if withdraw_time[0] and withdraw_time[0] > 0:
            if withdraw_time[1] == 2:
                return True
            if withdraw_time[1] == 1 and (session.id2 or session.id3):
                return True
            if withdraw_time[1] == 0 and not session.id2 and not session.id3:
                return True
        return False

    @classmethod
    def append(cls, bot: Bot, message_id: str | int, time: int):
        """添加消息撤回

        参数:
            bot: Bot
            message_id: 消息Id
            time: 延迟时间
        """
        cls._data[cls._index] = (
            bot,
            message_id,
            time,
        )
        cls._index += 1

    @classmethod
    def remove(cls, index: int):
        """移除

        参数:
            index: index
        """
        if index in cls._data:
            del cls._data[index]

    @classmethod
    async def withdraw_message(
        cls,
        bot: Bot,
        message_id: str | int,
        time: int | tuple[int, int] | None = None,
        session: EventSession | None = None,
    ):
        """消息撤回

        参数:
            bot: Bot
            message_id: 消息Id
            time: 延迟时间
        """
        if time:
            gid = None
            _time = 1
            if isinstance(time, tuple | CommentedSeq):
                if time[0] == 0:
                    return
                if session:
                    gid = session.id3 or session.id2
                if not gid and int(time[1]) not in [0, 2]:
                    return
                if gid and int(time[1]) not in [1, 2]:
                    return
                _time = time[0]
            else:
                _time = time
            logger.debug(
                f"将在 {_time}秒 内撤回消息ID: {message_id}", "WithdrawManager"
            )
            await asyncio.sleep(_time)
        if isinstance(bot, v11Bot):
            logger.debug(f"v11Bot 撤回消息ID: {message_id}", "WithdrawManager")
            await bot.delete_msg(message_id=int(message_id))
        elif isinstance(bot, v12Bot):
            logger.debug(f"v12Bot 撤回消息ID: {message_id}", "WithdrawManager")
            await bot.delete_message(message_id=str(message_id))
        # elif isinstance(bot, KaiheilaBot):
        #     pass
        # elif isinstance(bot, DodoBot):
        #     pass
        # elif isinstance(bot, DiscordBot):
        #     pass
