from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
import re


withdraw_msg = on_command('撤回', priority=5, block=True)


@withdraw_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    r = re.search(r'\[CQ:reply,id=(\d*)]', event.raw_message)
    if r:
        await bot.delete_msg(message_id=int(r.group(1)), self_id=int(bot.self_id))

