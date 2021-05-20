from nonebot import on_command
from .data_source import get_yiqing_data, clear_data
from services.log import logger
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from .config import city_list
from util.utils import scheduler

__plugin_name__ = '疫情查询'
__plugin_usage__ = '查询疫情帮助:\n\t对我说 查询疫情 省份/城市，我会回复疫情的实时数据\n\t示例: 查询疫情 温州'


yiqing = on_command("疫情", aliases={"查询疫情", "疫情查询"}, priority=5, block=True)


@yiqing.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if str(event.get_message()).strip() in ['帮助']:
        await yiqing.finish(__plugin_usage__)
    msg = str(event.get_message()).strip()
    if msg:
        if msg in city_list.keys():
            province = msg
            city = ''
        else:
            for key in city_list.keys():
                if msg in city_list.get(key):
                    province = key
                    city = msg
                    break
    else:
        await yiqing.finish(__plugin_usage__)
    try:
        result = await get_yiqing_data(province, city)
        if result:
            await yiqing.send(result)
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 查询疫情:" + result)
        else:
            await yiqing.send("查询失败!!!!", at_sender=True)
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 查询疫情失败")
    except UnboundLocalError:
        await yiqing.finish('参数正确吗？只要一个参数啊', at_sender=True)


@scheduler.scheduled_job(
    'cron',
    hour=0,
    minute=1,
)
async def _():
    clear_data()
