from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from utils.message_builder import image

__plugin_name__ = '更新信息'

__plugin_usage__ = '无'


update_info = on_command("更新信息", aliases={'更新日志'}, priority=5, block=True)


@update_info.handle()
async def _(bot: Bot, event: Event, state: T_State):
    img = image('update_info.png')
    if img:
        await update_info.finish(image('update_info.png'))
    else:
        await update_info.finish('目前没有更新信息哦')





