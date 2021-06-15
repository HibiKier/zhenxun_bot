from nonebot import on_regex
from .data_source import get_weather_of_city
from nonebot.adapters.cqhttp import Bot, Event
from jieba import posseg
from services.log import logger
from nonebot.typing import T_State
from .config import city_list
import re
from util.utils import get_message_text

__plugin_name__ = '天气查询'
__plugin_usage__ = "普普通通的查天气吧\n示例：北京天气"


weather = on_regex(r".*?(.*)市?的?天气.*?", priority=5, block=True)


@weather.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = get_message_text(event.json())
    msg = re.search(r'.*?(.*)市?的?天气.*?', msg)
    msg = msg.group(1)
    if msg[-1] == '的':
        msg = msg[:-1]
    if msg[-1] != '市':
        msg += '市'
    city = ''
    if msg:
        citys = []
        for x in city_list.keys():
            for city in city_list[x]:
                citys.append(city)
        for word in posseg.lcut(msg):
            if word.word in city_list.keys():
                await weather.finish("不要查一个省的天气啊，这么大查起来很累人的..", at_sender=True)
            if word.flag == 'ns' or word.word[:-1] in citys:
                city = str(word.word).strip()
                break
            if word.word == '火星':
                await weather.finish('没想到你个小呆子还真的想看火星天气！\n火星大气中含有95％的二氧化碳,气压低，加之极度的干燥，'
                                     '就阻止了水的形成积聚。这意味着火星几乎没有云,冰层覆盖了火星的两极，它们的融化和冻结受到火星与太'
                                     '阳远近距离的影响,它产生了强大的尘埃云，阻挡了太阳光，使冰层的融化慢下来。\n所以说火星天气太恶劣了，'
                                     '去过一次就不想再去第二次了')
    if city:
        city_weather = await get_weather_of_city(city)
        logger.info(f'(USER {event.user_id}, GROUP {event.group_id if event.message_type != "private" else "private"} ) '
                    f'查询天气:' + city)
        await weather.finish(city_weather)
    # if str(event.get_message()).strip() == '天气':
    #     state['city'] = '-1'
    #     return
    # msg = str(event.get_message()).strip()
    # print(msg)
    # flag = True
    # if msg.find('开启') != -1 or msg.find('关闭') != -1:
    #     state['city'] = '-1'
    #     return
    # if msg.startswith('天气'):
    #     if not msg.endswith('市'):
    #         state['city'] = msg[2:] + '市'
    #     else:
    #         state['city'] = msg[2:]
    #     flag = False
    # elif msg.find('的天气') != -1:
    #     i = msg.find('的天气')
    #     msg = msg[:i] + '市' + msg[i:]
    # elif msg.find('天气') != -1:
    #     i = msg.find('天气')
    #     msg = msg[:i] + '市' + msg[i:]
    # if msg != "天气" and flag:
    #     print(posseg.lcut(msg))
    #     for word in posseg.lcut(msg):
    #         if word.word in city_list.keys():# and word.word in ['北京', '上海', '天津', '重庆', '台湾']:
    #             await weather.finish("不要查一个省的天气啊，这么大查起来很累人的..", at_sender=True)
    #         if word.flag == 'ns':
    #             state["city"] = word.word
    #             break
    #         if word.word == '火星':
    #             await weather.finish('没想到你个小呆子还真的想看火星天气！\n火星大气中含有95％的二氧化碳,气压低，加之极度的干燥，'
    #                                  '就阻止了水的形成积聚。这意味着火星几乎没有云,冰层覆盖了火星的两极，它们的融化和冻结受到火星与太'
    #                                  '阳远近距离的影响,它产生了强大的尘埃云，阻挡了太阳光，使冰层的融化慢下来。\n所以说火星天气太恶劣了，'
    #                                  '去过一次就不想再去第二次了')


# @weather.got("city", prompt="你想查询哪个城市的天气呢？")
# async def _(bot: Bot, event: Event, state: dict):
#     if state['city'] == '-1' or not state['city'].strip():
#         return
#     if state['city'] in ['取消', '算了']:
#         await weather.finish('已取消此次调用..')
#     if state['city'][-1] != '市':
#         state['city'] += '市'
#     city_weather = await get_weather_of_city(state['city'].strip())
#     logger.info(f'(USER {event.user_id}, GROUP {event.group_id if event.message_type != "private" else "private"} ) '
#                 f'查询天气:' + state['city'])
#     await weather.finish(city_weather)

