import ujson as json
import os
from nonebot.adapters.cqhttp import MessageSegment
import nonebot
import random
from .update_game_info import update_info
from .update_game_simple_info import update_simple_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star, max_card
from .config import PCR_TWO_P, PCR_THREE_P, PCR_ONE_P, DRAW_PATH, PCR_FLAG, PCR_G_TWO_P, PCR_G_THREE_P, PCR_TAI
from dataclasses import dataclass
from .init_card_pool import init_game_pool

driver: nonebot.Driver = nonebot.get_driver()

ALL_CHAR = []


@dataclass
class PcrChar(BaseData):
    pass


async def pcr_draw(count: int):
    #            0      1      2
    cnlist = ['★★★', '★★', '★']
    char_list, three_list, three_index_list, char_dict, star_list = _format_card_information(count)
    rst = init_star_rst(star_list, cnlist, three_list, three_index_list)
    if count > 90:
        char_list = set_list(char_list)
    return MessageSegment.image("base64://" + await generate_img(char_list, 'pcr', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(char_dict)


async def update_pcr_info():
    global ALL_CHAR
    if PCR_TAI:
        url = 'https://wiki.biligame.com/pcr/角色图鉴'
        data, code = await update_simple_info(url, 'pcr')
    else:
        url = 'https://wiki.biligame.com/pcr/角色筛选表'
        data, code = await update_info(url, 'pcr')
    if code == 200:
        ALL_CHAR = init_game_pool('pcr', data, PcrChar)


async def init_pcr_data():
    global ALL_CHAR
    if PCR_FLAG:
        with open(DRAW_PATH + 'pcr.json', 'r', encoding='utf8') as f:
            pcr_dict = json.load(f)
        ALL_CHAR = init_game_pool('pcr', pcr_dict, PcrChar)


# 抽取卡池
def _get_pcr_card(mode: int = 1):
    global ALL_CHAR
    if mode == 2:
        star = get_star([3, 2], [PCR_G_THREE_P, PCR_G_TWO_P])
    else:
        star = get_star([3, 2, 1], [PCR_THREE_P, PCR_TWO_P, PCR_ONE_P])
    chars = [x for x in ALL_CHAR if x.star == star and not x.limited]
    return random.choice(chars), 3 - star


def _format_card_information(_count: int):
    char_list = []
    star_list = [0, 0, 0]
    three_index_list = []
    three_list = []
    char_dict = {}
    # 保底计算
    count = 0
    for i in range(_count):
        count += 1
        # 十连保底
        if count == 10:
            char, code = _get_pcr_card(2)
            count = 0
        else:
            char, code = _get_pcr_card()
            if code < 2:
                count = 0
        star_list[code] += 1
        if code == 0:
            three_list.append(char.name)
            three_index_list.append(i)
        try:
            char_dict[char.name] += 1
        except KeyError:
            char_dict[char.name] = 1
        char_list.append(char)
    return char_list, three_list, three_index_list, char_dict, star_list
