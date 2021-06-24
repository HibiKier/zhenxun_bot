from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message
from nonebot.typing import T_State
from configs.config import ALAPI_TOKEN
from util.init_result import image
from util.utils import get_message_text
from .util import get_data
from services.log import logger

__plugin_name__ = 'b封面'
__plugin_usage__ = '用法： b封面 (链接，av，bv，cv，直播id)\n\t' \
                   '示例：b封面 av86863038'


cover = on_command('b封面', priority=5, block=True)


cover_url = 'https://v2.alapi.cn/api/bilibili/cover'


@cover.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    params = {
        'token': ALAPI_TOKEN,
        'c': msg
    }
    data, code = await get_data(cover_url, params)
    if code != 200:
        await cover.finish(data, at_sender=True)
    data = data['data']
    title = data['title']
    img = data['cover']
    await cover.send(Message(f'title：{title}\n{image(img)}'))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 获取b站封面: {title} url：{img}")



