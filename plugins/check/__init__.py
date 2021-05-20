
from nonebot import on_command
from .data_source import Check
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER


__plugin_name__ = '自我检查'

check = Check()


check_ = on_command('自检', aliases={'check'}, rule=to_me(), permission=SUPERUSER, block=True, priority=1)


@check_.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await check_.send(await check.show())
