
import os
import nonebot
from util.init_result import image
from .update_game_info import update_info
from .util import download_img, init_star_rst, generate_img, max_card, BaseData, \
    set_list, get_star, format_card_information
import random
from .config import PRETTY_THREE_P, PRETTY_TWO_P, DRAW_PATH, PRETTY_ONE_P, PRETTY_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
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
    return image(b64=await generate_img(obj_list, 'pretty', star_list)) \
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


@driver.on_startup
async def init_data():
    global ALL_CHAR, ALL_CARD
    if PRETTY_FLAG:
        if not os.path.exists(DRAW_PATH + 'pretty.json') or not os.path.exists(DRAW_PATH + 'pretty_card.json'):
            await update_pretty_info()
            for icon_url in [
                'https://patchwiki.biligame.com/images/umamusume/thumb/0/06/q23szwkbtd7pfkqrk3wcjlxxt9z595o.png'
                '/40px-SSR.png',
                'https://patchwiki.biligame.com/images/umamusume/thumb/3/3b/d1jmpwrsk4irkes1gdvoos4ic6rmuht.png'
                '/40px-SR.png',
                'https://patchwiki.biligame.com/images/umamusume/thumb/f/f7/afqs7h4snmvovsrlifq5ib8vlpu2wvk.png'
                '/40px-R.png']:
                await download_img(icon_url, 'pretty', icon_url.split('-')[-1][:-4])
        else:
            with open(DRAW_PATH + 'pretty.json', 'r', encoding='utf8') as f:
                pretty_char_dict = json.load(f)
            with open(DRAW_PATH + 'pretty_card.json', 'r', encoding='utf8') as f:
                pretty_card_dict = json.load(f)
            ALL_CHAR = init_game_pool('pretty', pretty_char_dict, PrettyChar)
            ALL_CARD = init_game_pool('pretty_card', pretty_card_dict, PrettyChar)


# 抽取卡池
def _get_pretty_card(itype):
    global ALL_CHAR, ALL_CARD
    star = get_star([3, 2, 1], [PRETTY_THREE_P, PRETTY_TWO_P, PRETTY_ONE_P])
    chars = [x for x in (ALL_CARD if itype == 'card' else ALL_CHAR) if x.star == star]
    return random.choice(chars), abs(star - 3)

