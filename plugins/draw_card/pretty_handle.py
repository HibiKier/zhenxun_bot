import os
import nonebot
from .update_game_info import update_info
from .announcement import PrettyAnnouncement
from .util import download_img, init_star_rst, generate_img, max_card, BaseData, \
    set_list, get_star, format_card_information, UpEvent
import random
from .config import PRETTY_THREE_P, PRETTY_TWO_P, DRAW_PATH, PRETTY_ONE_P, PRETTY_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
from util.init_result import image
from configs.path_config import IMAGE_PATH

try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

ALL_CHAR = []
ALL_CARD = []

_CURRENT_CHAR_POOL_TITLE = ""
_CURRENT_CARD_POOL_TITLE = ""
UP_CHAR = []
UP_CARD = []
POOL_IMG = []


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
    up_type = []
    up_list = []
    title = ''
    if pool_name == 'char' and _CURRENT_CHAR_POOL_TITLE:
        up_type = UP_CHAR
        title = _CURRENT_CHAR_POOL_TITLE
    elif pool_name == 'card' and _CURRENT_CARD_POOL_TITLE:
        up_type = UP_CARD
        title = _CURRENT_CARD_POOL_TITLE
    tmp = ''
    if up_type:
        for x in up_type:
            for operator in x.operators:
                up_list.append(operator.split(']')[1] if pool_name == 'char' else operator)
            if x.star == 3:
                if pool_name == 'char':
                    tmp += f'三星UP：{" ".join(x.operators)} \n'
                else:
                    tmp += f'SSR UP：{" ".join(x.operators)} \n'
            elif x.star == 2:
                if pool_name == 'char':
                    tmp += f'二星UP：{" ".join(x.operators)} \n'
                else:
                    tmp += f'SR UP：{" ".join(x.operators)} \n'
            elif x.star == 1:
                if pool_name == 'char':
                    tmp += f'一星UP：{" ".join(x.operators)} '
                else:
                    tmp += f'R UP：{" ".join(x.operators)} '
    tmp = tmp[:-1] if tmp and tmp[-1] == '\n' else tmp
    pool_info = f'当前up池：{title}\n{tmp}' if title else ''
    rst = init_star_rst(star_list, cnlist, three_list, three_olist, up_list)
    if count > 90:
        obj_list = set_list(obj_list)
    return pool_info + image(b64=await generate_img(obj_list, 'pretty', star_list)) \
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
    global ALL_CHAR, ALL_CARD, _CURRENT_CHAR_POOL_TITLE, _CURRENT_CARD_POOL_TITLE
    star = get_star([3, 2, 1], [PRETTY_THREE_P, PRETTY_TWO_P, PRETTY_ONE_P])
    if pool_name == 'card':
        title = _CURRENT_CARD_POOL_TITLE
        up_data = UP_CARD
        data = ALL_CARD
    else:
        title = _CURRENT_CHAR_POOL_TITLE
        up_data = UP_CHAR
        data = ALL_CHAR
    # 有UP池子
    if title and star in [x.star for x in up_data]:
        all_char_lst = [x for x in data if x.star == star and not x.limited]
        # 抽到UP
        if random.random() < 1 / len(all_char_lst) * (0.7 / 0.1385):
            all_up_star = [x.operators for x in up_data if x.star == star][0]
            acquire_operator = random.choice(all_up_star)
            if pool_name == 'char':
                acquire_operator = acquire_operator.split(']')[1]
            acquire_operator = [x for x in data if x.name == acquire_operator][0]
        else:
            acquire_operator = random.choice([x for x in data if x.star == star and not x.limited])
    else:
        acquire_operator = random.choice([x for x in data if x.star == star and not x.limited])
    return acquire_operator, 3 - star


# 获取up和概率
async def _init_up_char():
    global _CURRENT_CHAR_POOL_TITLE, _CURRENT_CARD_POOL_TITLE, UP_CHAR, UP_CARD, POOL_IMG
    UP_CHAR = []
    UP_CARD = []
    up_char_dict = await PrettyAnnouncement.update_up_char()
    _CURRENT_CHAR_POOL_TITLE = up_char_dict['char']['title']
    _CURRENT_CARD_POOL_TITLE = up_char_dict['card']['title']
    if _CURRENT_CHAR_POOL_TITLE and _CURRENT_CARD_POOL_TITLE:
        await download_img(up_char_dict['char']['pool_img'], 'pretty', 'up_char_pool_img')
        await download_img(up_char_dict['card']['pool_img'], 'pretty', 'up_card_pool_img')
        POOL_IMG = image('up_char_pool_img.png', '/draw_card/pretty/') + \
                   image('up_card_pool_img.png', '/draw_card/pretty/')
    else:
        if os.path.exists(IMAGE_PATH + '/draw_card/genshin/up_char_pool_img.png'):
            os.remove(IMAGE_PATH + '/draw_card/pretty/up_char_pool_img.png')
        if os.path.exists(IMAGE_PATH + '/draw_card/genshin/up_arms_pool_img.png'):
            os.remove(IMAGE_PATH + '/draw_card/pretty/up_card_pool_img.png')
    print(f'成功获取赛马娘当前up信息...当前up池: {_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_CARD_POOL_TITLE}')
    for key in up_char_dict.keys():
        for star in up_char_dict[key]['up_char'].keys():
            up_lst = []
            for char in up_char_dict[key]['up_char'][star].keys():
                up_lst.append(char)
            if key == 'char':
                if up_lst:
                    UP_CHAR.append(UpEvent(star=int(star), operators=up_lst, zoom=0))
            else:
                if up_lst:
                    UP_CARD.append(UpEvent(star=int(star), operators=up_lst, zoom=0))


async def reload_pretty_pool():
    await _init_up_char()
    return f'当前UP池子：{_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_CARD_POOL_TITLE} {POOL_IMG}'


