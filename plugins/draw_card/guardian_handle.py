
import os
import nonebot
from nonebot.adapters.cqhttp import MessageSegment
from util.init_result import image
from .update_game_info import update_info
from .util import init_star_rst, generate_img, max_card, BaseData,\
    set_list, get_star, format_card_information
import random
from .config import DRAW_PATH, GUARDIAN_ONE_CHAR_P, GUARDIAN_TWO_CHAR_P, GUARDIAN_THREE_CHAR_P, \
    GUARDIAN_THREE_CHAR_UP_P, GUARDIAN_TWO_ARMS_P, GUARDIAN_FIVE_ARMS_P, GUARDIAN_THREE_CHAR_OTHER_P, \
    GUARDIAN_FOUR_ARMS_P, GUARDIAN_THREE_ARMS_P, GUARDIAN_EXCLUSIVE_ARMS_P, GUARDIAN_EXCLUSIVE_ARMS_UP_P, \
    GUARDIAN_EXCLUSIVE_ARMS_OTHER_P, GUARDIAN_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

ALL_CHAR = []
ALL_ARMS = []


@dataclass
class GuardianChar(BaseData):
    pass


@dataclass
class GuardianArms(BaseData):
    pass


async def guardian_draw(count: int, pool_name):
    if pool_name == 'arms':
        cnlist = ['★★★★★', '★★★★', '★★★', '★★']
        star_list = [0, 0, 0, 0]
    else:
        cnlist = ['★★★', '★★', '★']
        star_list = [0, 0, 0]
    obj_list, obj_dict, max_list, star_list, max_index_list = format_card_information(count, star_list,
                                                                                      _get_guardian_card, pool_name)
    rst = init_star_rst(star_list, cnlist, max_list, max_index_list)
    if count > 90:
        obj_list = set_list(obj_list)
    return image(b64=await generate_img(obj_list, 'guardian', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(obj_dict)


async def update_guardian_info():
    global ALL_CHAR, ALL_ARMS
    url = 'https://wiki.biligame.com/gt/英雄筛选表'
    data, code = await update_info(url, 'guardian')
    if code == 200:
        ALL_CHAR = init_game_pool('guardian', data, GuardianChar)
    url = 'https://wiki.biligame.com/gt/武器'
    tmp, code_1 = await update_info(url, 'guardian_arms')
    url = 'https://wiki.biligame.com/gt/盾牌'
    data, code_2 = await update_info(url, 'guardian_arms')
    if code_1 == 200 and code_2 == 200:
        data.update(tmp)
        ALL_ARMS = init_game_pool('guardian_arms', data, GuardianArms)


@driver.on_startup
async def init_data():
    global ALL_CHAR, ALL_ARMS
    if GUARDIAN_FLAG:
        if not os.path.exists(DRAW_PATH + 'guardian.json') or not os.path.exists(DRAW_PATH + 'guardian_arms.json'):
            await update_guardian_info()
        else:
            with open(DRAW_PATH + 'guardian.json', 'r', encoding='utf8') as f:
                guardian_char_dict = json.load(f)
            with open(DRAW_PATH + 'guardian_arms.json', 'r', encoding='utf8') as f:
                guardian_arms_dict = json.load(f)
            ALL_CHAR = init_game_pool('guardian', guardian_char_dict, GuardianChar)
            ALL_ARMS = init_game_pool('guardian_arms', guardian_arms_dict, GuardianArms)


# 抽取卡池
def _get_guardian_card(itype):
    global ALL_CHAR, ALL_ARMS
    if itype != 'arms':
        star = get_star([3, 2, 1], [GUARDIAN_THREE_CHAR_P, GUARDIAN_TWO_CHAR_P, GUARDIAN_ONE_CHAR_P])
        chars = [x for x in ALL_CHAR if x.star == star]
        return random.choice(chars), abs(star - 3)
    else:
        star = get_star([5, 4, 3, 2], [GUARDIAN_FIVE_ARMS_P, GUARDIAN_FOUR_ARMS_P,
                                       GUARDIAN_THREE_ARMS_P, GUARDIAN_TWO_ARMS_P])
        arms = [x for x in ALL_ARMS if x.star == star]
        return random.choice(arms), abs(star - 5)


# 整理数据
def _format_card_information(count: int, pool_name: str):
    max_star_lst = []
    max_index_lst = []
    obj_list = []
    obj_dict = {}
    if pool_name == 'arms':
        star_list = [0, 0, 0, 0]
    else:
        star_list = [0, 0, 0]
    for i in range(count):
        obj, code = _get_guardian_card(pool_name)
        star_list[code] += 1
        if code == 0:
            max_star_lst.append(obj.name)
            max_index_lst.append(i)
        try:
            obj_dict[obj.name] += 1
        except KeyError:
            obj_dict[obj.name] = 1
        obj_list.append(obj)
    return obj_list, obj_dict, max_star_lst, star_list, max_index_lst
