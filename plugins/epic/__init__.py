from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from util.utils import scheduler, get_bot
from .data_source import get_epic_game
from models.group_remind import GroupRemind
from nonebot.adapters.cqhttp.exception import ActionFailed

__plugin_usage__ = 'epic免费游戏提醒'


epic = on_command("epic", priority=5, block=True)


@epic.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    # try:
    if str(event.get_message()) in ['帮助']:
        await epic.finish(__plugin_usage__)
    try:
        result = await get_epic_game()
    except:
        result = '网络出错了！'
    await epic.send(result)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 获取epic免费游戏")
    # except Exception as e:
    #     logger.error(f'epic 出错 e:{e}')
    #     await epic.finish('网络好像炸了，再试一次？', at_sender=True)


# epic免费游戏
@scheduler.scheduled_job(
    'cron',
    hour=12,
    minute=1,
)
async def _():
    # try:
    bot = get_bot()
    gl = await bot.get_group_list(self_id=bot.self_id)
    gl = [g['group_id'] for g in gl]
    for g in gl:
        if await GroupRemind.get_status(g, 'epic'):
            result = await get_epic_game()
            if result == '今天没有游戏可以白嫖了！':
                return
            try:
                await bot.send_group_msg(group_id=g,
                                         message=result)
            except ActionFailed:
                logger.error(f'{g}群 epic免费游戏推送错误')
    # except Exception as e:
    #     logger.error(f'epic免费游戏推送错误 e:{e}')




