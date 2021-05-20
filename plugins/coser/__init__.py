from nonebot import on_command
from util.utils import get_message_text
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from services.log import logger
from util.init_result import image
import requests

__plugin_usage_coser__ = '不得看看可爱的coser？发送‘coser’'


coser = on_command('cos', aliases={'coser', '括丝'}, priority=5, block=True)


url_2 = 'http://api.rosysun.cn/cos'


@coser.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if get_message_text(event.json()) in ['帮助']:
        await coser.finish(__plugin_usage_coser__)
    img_url = requests.get(url_2).text
    await coser.send(image(img_url))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 发送COSER")














