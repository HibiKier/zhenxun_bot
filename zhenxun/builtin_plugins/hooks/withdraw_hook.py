import asyncio
from typing import Optional

from nonebot.adapters import Bot
from nonebot.adapters.discord import Bot as DiscordBot
from nonebot.adapters.dodo import Bot as DodoBot
from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor

from zhenxun.services.log import logger
from zhenxun.utils.utils import WithdrawManager

# TODO: 其他平台撤回消息


# 消息撤回
@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
):
    tasks = []
    for message_id in WithdrawManager._data:
        second = WithdrawManager._data[message_id]
        tasks.append(asyncio.ensure_future(_withdraw_message(bot, message_id, second)))
        WithdrawManager.remove(message_id)
    await asyncio.gather(*tasks)


async def _withdraw_message(bot: Bot, message_id: str, time: int):
    await asyncio.sleep(time)
    logger.debug(f"撤回消息ID: {message_id}", "HOOK")
    if isinstance(bot, v11Bot):
        await bot.delete_msg(message_id=int(message_id))
    elif isinstance(bot, v12Bot):
        await bot.delete_message(message_id=message_id)
    elif isinstance(bot, DodoBot):
        pass
    elif isinstance(bot, KaiheilaBot):
        pass
    elif isinstance(bot, DiscordBot):
        pass
