import asyncio

from nonebot.adapters import Bot
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor

from zhenxun.utils.withdraw_manage import WithdrawManager


@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Exception | None,
    bot: Bot,
):
    tasks = []
    index_list = list(WithdrawManager._data.keys())
    for index in index_list:
        (
            bot,
            message_id,
            time,
        ) = WithdrawManager._data[index]
        tasks.append(
            asyncio.ensure_future(
                WithdrawManager.withdraw_message(bot, message_id, time)
            )
        )
        WithdrawManager.remove(index)
    await asyncio.gather(*tasks)
