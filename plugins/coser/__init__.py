from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from services.log import logger
from utils.message_builder import image
import requests

__plugin_name__ = "coser"

__plugin_usage__ = "用法：发送‘coser’"


coser = on_command(
    "cos", aliases={"coser", "括丝", "COS", "Cos", "cOS", "coS"}, priority=5, block=True
)


url_2 = "http://api.rosysun.cn/cos"


@coser.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img_url = requests.get(url_2).text
    await coser.send(image(img_url))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送COSER"
    )
