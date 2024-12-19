from datetime import datetime, timedelta
import time

import nonebot
from nonebot.adapters import Bot
from nonebot.drivers import Driver

from zhenxun.models.chat_history import ChatHistory
from zhenxun.models.statistics import Statistics
from zhenxun.utils.platform import PlatformUtils

from ..main.data_source import bot_live
from .model import BotInfo

driver: Driver = nonebot.get_driver()


CONNECT_TIME = 0


@driver.on_startup
async def _():
    global CONNECT_TIME
    CONNECT_TIME = int(time.time())


class BotManage:
    @classmethod
    async def __build_bot_info(cls, bot: Bot) -> BotInfo:
        """构建Bot信息

        参数:
            bot: Bot

        返回:
            BotInfo: Bot信息
        """
        now = datetime.now()
        platform = PlatformUtils.get_platform(bot) or ""
        if platform == "qq":
            login_info = await bot.get_login_info()
            nickname = login_info["nickname"]
            ava_url = PlatformUtils.get_user_avatar_url(bot.self_id, "qq") or ""
        else:
            nickname = bot.self_id
            ava_url = ""
        bot_info = BotInfo(
            self_id=bot.self_id, nickname=nickname, ava_url=ava_url, platform=platform
        )
        group_list, _ = await PlatformUtils.get_group_list(bot)
        group_list = [g for g in group_list if g.channel_id is None]
        friend_list, _ = await PlatformUtils.get_friend_list(bot)
        bot_info.group_count = len(group_list)
        bot_info.friend_count = len(friend_list)
        bot_info.day_call = await Statistics.filter(
            create_time__gte=now - timedelta(hours=now.hour, minutes=now.minute),
            bot_id=bot.self_id,
        ).count()
        bot_info.received_messages = await ChatHistory.filter(
            bot_id=bot_info.self_id,
            create_time__gte=now - timedelta(hours=now.hour, minutes=now.minute),
        ).count()
        bot_info.connect_time = bot_live.get(bot.self_id) or 0
        if bot_info.connect_time:
            connect_date = datetime.fromtimestamp(CONNECT_TIME)
            bot_info.connect_date = connect_date.strftime("%Y-%m-%d %H:%M:%S")
        return bot_info

    @classmethod
    async def get_bot_list(cls) -> list[BotInfo]:
        """获取bot列表

        返回:
            list[BotInfo]: Bot列表
        """
        bot_list: list[BotInfo] = []
        for _, bot in nonebot.get_bots().items():
            bot_list.append(await cls.__build_bot_info(bot))
        return bot_list
