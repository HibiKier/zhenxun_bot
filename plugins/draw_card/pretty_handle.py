
import os
import nonebot
from util.init_result import image
from configs.path_config import DRAW_PATH
from .update_game_info import update_info
from .util import download_img, init_star_rst, generate_img, max_card, BaseData, set_list
import random
from .config import PRETTY_THREE, PRETTY_TWO, PRETTY_ONE
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
    obj_list, obj_dict, three_list, star_list, three_olist = _format_card_information(count, pool_name)
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
    if not os.path.exists(DRAW_PATH + '/draw_card_config/pretty.json') or\
            not os.path.exists(DRAW_PATH + '/draw_card_config/pretty_card.json'):
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
        with open(DRAW_PATH + '/draw_card_config/pretty.json', 'r', encoding='utf8') as f:
            pretty_char_dict = json.load(f)
        with open(DRAW_PATH + '/draw_card_config/pretty_card.json', 'r', encoding='utf8') as f:
            pretty_card_dict = json.load(f)
        ALL_CHAR = init_game_pool('pretty', pretty_char_dict, PrettyChar)
        ALL_CARD = init_game_pool('pretty_card', pretty_card_dict, PrettyChar)


# 抽取卡池
def _get_pretty_card(itype):
    global ALL_CHAR, ALL_CARD
    star = random.sample([3, 2, 1],
                         counts=[int(PRETTY_THREE * 100), int(PRETTY_TWO * 100),
                                 int(PRETTY_ONE * 100)],
                         k=1)[0]
    chars = [x for x in (ALL_CARD if itype == 'card' else ALL_CHAR) if x.star == star]
    return random.choice(chars), abs(star - 3)


# 整理数据
def _format_card_information(count: int, pool_name: str):
    three_list = []
    three_olist = []
    obj_list = []
    obj_dict = {}
    star_list = [0, 0, 0]
    for i in range(count):
        obj, code = _get_pretty_card(pool_name)
        star_list[code] += 1
        if code == 0:
            three_list.append(obj.name)
            three_olist.append(i)
        try:
            obj_dict[obj.name] += 1
        except KeyError:
            obj_dict[obj.name] = 1
        obj_list.append(obj)
    return obj_list, obj_dict, three_list, star_list, three_olist
