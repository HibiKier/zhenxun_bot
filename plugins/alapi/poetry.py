from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from configs.config import ALAPI_TOKEN
from services.log import logger
from .util import get_data

__plugin_name__ = '古诗'
__plugin_usage__ = '用法： 无'


poetry = on_command("念诗", aliases={'来首诗', '念首诗'}, priority=5, block=True)


poetry_url = 'https://v2.alapi.cn/api/shici'


@poetry.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    params = {
        'token': ALAPI_TOKEN
    }
    data, code = await get_data(poetry_url, params)
    if code != 200:
        await poetry.finish(data, at_sender=True)
    data = data['data']
    content = data['content']
    title = data['origin']
    author = data['author']
    await poetry.send(f'{content}\n\t——{author}《{title}》')
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 发送古诗: f'{content}\n\t--{author}《{title}》'")



