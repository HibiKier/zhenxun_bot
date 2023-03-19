import asyncio
from typing import Optional

from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
from nonebot.typing import T_State

from services.log import logger
from utils.manager import withdraw_message_manager


# 消息撤回
@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: Event,
    state: T_State,
):
    tasks = []
    for id_, time in withdraw_message_manager.data:
        tasks.append(asyncio.ensure_future(_withdraw_message(bot, id_, time)))
        withdraw_message_manager.remove((id_, time))
    await asyncio.gather(*tasks)


async def _withdraw_message(bot: Bot, id_: int, time: int):
    await asyncio.sleep(time)
    logger.debug(f"撤回消息ID: {id_}", "HOOK")
    await bot.delete_msg(message_id=id_)
