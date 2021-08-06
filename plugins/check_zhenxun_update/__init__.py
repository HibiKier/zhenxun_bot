from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot import on_command
from .data_source import check_update


update_zhenxun = on_command('检查更新真寻', permission=SUPERUSER, priority=1, block=True)


@update_zhenxun.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        await check_update(bot)
    except Exception as e:
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f'更新真寻未知错误 {type(e)}：{e}'
        )
    else:
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f'请重启真寻....'
        )





