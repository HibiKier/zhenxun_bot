from nonebot import on_regex
from .data_source import get_weather_of_city, update_city, get_city_list
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from jieba import posseg
from services.log import logger
from nonebot.typing import T_State
import re
from utils.utils import get_message_text

__plugin_name__ = "天气查询"
__plugin_usage__ = "普普通通的查天气吧\n示例：北京天气"


weather = on_regex(r".*?(.*)市?的?天气.*?", priority=5, block=True)


@weather.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    msg = re.search(r".*?(.*)市?的?天气.*?", msg)
    msg = msg.group(1)
    if msg[-1] == "的":
        msg = msg[:-1]
    if msg[-1] != "市":
        msg += "市"
    city = ""
    if msg:
        city_list = get_city_list()
        for word in posseg.lcut(msg):
            if word.flag == "ns" or word.word[:-1] in city_list:
                city = str(word.word).strip()
                break
            if word.word == "火星":
                await weather.finish(
                    "没想到你个小呆子还真的想看火星天气！\n火星大气中含有95％的二氧化碳,气压低，加之极度的干燥，"
                    "就阻止了水的形成积聚。这意味着火星几乎没有云,冰层覆盖了火星的两极，它们的融化和冻结受到火星与太"
                    "阳远近距离的影响,它产生了强大的尘埃云，阻挡了太阳光，使冰层的融化慢下来。\n所以说火星天气太恶劣了，"
                    "去过一次就不想再去第二次了"
                )
    if city:
        city_weather = await get_weather_of_city(city)
        logger.info(
            f'(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else "private"} ) '
            f"查询天气:" + city
        )
        await weather.finish(city_weather)
