import json
import os
from typing import Dict
from utils.http_utils import AsyncHttpx
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, Bot
from services.log import logger
from utils.message_builder import image
from configs.path_config import IMAGE_PATH

__zx_plugin_name__ = "随机丁真"
__plugin_usage__ = """
usage：
    获取随机丁真梗图
    指令：
        丁真
""".strip()
__plugin_des__ = "随机丁真"
__plugin_cmd__ = [
    "丁真",
]
__plugin_version__ = 0.2
__plugin_author__ = "Pr0pHesyer"
__plugin_settings__ = {
    "level": 0,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [
        "丁真"
    ],
}

dingzhen = on_keyword({"丁真"}, priority=9, block=True)
# 常量
url = 'https://api.aya1.top/randomdj?r=0'
randomUrl = url + "&g=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
                  " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://api.aya1.top",
}




@dingzhen.handle()
async def SentRandomDingzhen(bot: Bot, event: MessageEvent, state: T_State):
    try:
        # 获取json字典
        dingzhenJson = (await AsyncHttpx.get(randomUrl)).json()
        gotPicUrl = dingzhenJson["url"]
        if not await AsyncHttpx.download_file(
                gotPicUrl,
                IMAGE_PATH / "temp" / f"dingzhen_{event.user_id}.png",
                headers=headers,
        ):
            await dingzhen.finish("丁真没了..", at_sender=True)
        # 发送消息
        await dingzhen.send(image(f"dingzhen_{event.user_id}.png", "temp"), at_sender=True)

        logger.info(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
            f" 丁真 {dingzhenJson} "
        )
    except:
        logger.info(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 丁真 未找到"
        )
        await dingzhen.send(f"丁真没了..", at_sender=True)
