import os
import nonebot
from nonebot.adapters.cqhttp import MessageSegment
from .update_game_info import update_info
from .util import download_img, init_star_rst, generate_img, max_card, BaseData, \
    set_list, get_star, format_card_information
import random
from .config import PRETTY_THREE_P, PRETTY_TWO_P, DRAW_PATH, PRETTY_ONE_P, PRETTY_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
import asyncio

try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

ALL_CHAR = []
ALL_CARD = []


@dataclass
class PrettyChar(BaseData):
    pass


async def pretty_draw(count: int, pool_name):
    if pool_name == 'card':
        cnlist = ['SSR', 'SR', 'R']
    else:
        cnlist = ['★★★', '★★', '★']
    star_list = [0, 0, 0]
    obj_list, obj_dict, three_list, star_list, three_olist = format_card_information(count, star_list,
                                                                                     _get_pretty_card, pool_name)
    rst = init_star_rst(star_list, cnlist, three_list, three_olist)
    if count > 90:
        obj_list = set_list(obj_list)
    return MessageSegment.image(
        "base64://" + await generate_img(obj_list, 'pretty', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(obj_dict)


async def update_pretty_info():
    global ALL_CHAR, ALL_CARD
    url = 'https://wiki.biligame.com/umamusume/赛马娘图鉴'
    data, code = await update_info(url, 'pretty')
    if code == 200:
        ALL_CHAR = init_game_pool('pretty', data, PrettyChar)
    url = 'https://wiki.biligame.com/umamusume/支援卡图鉴'
    data, code = await update_info(url, 'pretty_card')
    if code == 200:
        ALL_CARD = init_game_pool('pretty_card', data, PrettyChar)


async def init_pretty_data():
    global ALL_CHAR, ALL_CARD
    if PRETTY_FLAG:
        with open(DRAW_PATH + 'pretty.json', 'r', encoding='utf8') as f:
            pretty_char_dict = json.load(f)
        with open(DRAW_PATH + 'pretty_card.json', 'r', encoding='utf8') as f:
            pretty_card_dict = json.load(f)
        ALL_CHAR = init_game_pool('pretty', pretty_char_dict, PrettyChar)
        ALL_CARD = init_game_pool('pretty_card', pretty_card_dict, PrettyChar)


# 抽取卡池
def _get_pretty_card(pool_name: str):
    global ALL_CHAR, ALL_CARD
    star = get_star([3, 2, 1], [PRETTY_THREE_P, PRETTY_TWO_P, PRETTY_ONE_P])
    chars = [x for x in (ALL_CARD if pool_name == 'card' else ALL_CHAR) if x.star == star]
    return random.choice(chars), 3 - star
