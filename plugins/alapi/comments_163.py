from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from configs.config import ALAPI_TOKEN
from .util import get_data
from services.log import logger

__plugin_name__ = '网易云热评'
__plugin_usage__ = '用法： 生了个人，我很抱歉'

comments_163 = on_command("网易云热评", aliases={'网易云评论', '到点了', '12点了'}, priority=5, block=True)


comments_163_url = 'https://v2.alapi.cn/api/comment'


@comments_163.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    params = {
        'token': ALAPI_TOKEN
    }
    data, code = await get_data(comments_163_url, params)
    if code != 200:
        await comments_163.finish(data, at_sender=True)
    data = data['data']
    comment = data['comment_content']
    song_name = data['title']
    await comments_163.send(f'{comment}\n\t——《{song_name}》')
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 发送网易云热评: {comment} \n\t\t————{song_name}")





