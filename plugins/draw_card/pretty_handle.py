
import nonebot
from .update_game_info import update_info
from .announcement import PrettyAnnouncement
from .util import init_star_rst, generate_img, max_card, BaseData, \
    set_list, get_star, format_card_information, init_up_char
import random
from .config import PRETTY_THREE_P, PRETTY_TWO_P, DRAW_PATH, PRETTY_ONE_P, PRETTY_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
from nonebot.adapters.cqhttp import MessageSegment, Message

try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

announcement = PrettyAnnouncement()

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
    return pool_info + MessageSegment.image("base64://" + await generate_img(obj_list, 'pretty', star_list)) \
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
    await _pretty_init_up_char()


async def init_pretty_data():
    global ALL_CHAR, ALL_CARD
    if PRETTY_FLAG:
        with open(DRAW_PATH + 'pretty.json', 'r', encoding='utf8') as f:
            pretty_char_dict = json.load(f)
        with open(DRAW_PATH + 'pretty_card.json', 'r', encoding='utf8') as f:
            pretty_card_dict = json.load(f)
        ALL_CHAR = init_game_pool('pretty', pretty_char_dict, PrettyChar)
        ALL_CARD = init_game_pool('pretty_card', pretty_card_dict, PrettyChar)
        await _pretty_init_up_char()


# 抽取卡池
def _get_pretty_card(pool_name: str, mode: int = 1):
    global ALL_CHAR, ALL_CARD, _CURRENT_CHAR_POOL_TITLE, _CURRENT_CARD_POOL_TITLE
    if mode == 1:
        star = get_star([3, 2, 1], [PRETTY_THREE_P, PRETTY_TWO_P, PRETTY_ONE_P])
    else:
        star = get_star([3, 2], [PRETTY_THREE_P, PRETTY_TWO_P])
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
            print(acquire_operator)
            acquire_operator = [x for x in data if x.name == acquire_operator][0]
        else:
            acquire_operator = random.choice([x for x in data if x.star == star and not x.limited])
    else:
        acquire_operator = random.choice([x for x in data if x.star == star and not x.limited])
    return acquire_operator, 3 - star


# 获取up和概率
async def _pretty_init_up_char():
    global _CURRENT_CHAR_POOL_TITLE, _CURRENT_CARD_POOL_TITLE, UP_CHAR, UP_CARD, POOL_IMG
    _CURRENT_CHAR_POOL_TITLE, _CURRENT_CARD_POOL_TITLE, POOL_IMG, UP_CHAR, UP_CARD = await init_up_char(announcement)


async def reload_pretty_pool():
    await _pretty_init_up_char()
    return Message(f'当前UP池子：{_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_CARD_POOL_TITLE} {POOL_IMG}')


