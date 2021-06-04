
from nonebot.adapters.cqhttp import MessageSegment
import random
from .update_game_requests_info import update_requests_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star, max_card
from .config import FGO_CARD_FOUR_P, FGO_CARD_FIVE_P, FGO_CARD_THREE_P, FGO_SERVANT_THREE_P, \
    FGO_SERVANT_FIVE_P, FGO_SERVANT_FOUR_P, FGO_FLAG, DRAW_PATH
from dataclasses import dataclass
from .init_card_pool import init_game_pool

try:
    import ujson as json
except ModuleNotFoundError:
    import json

ALL_CHAR = []
ALL_CARD = []


@dataclass
class FgoChar(BaseData):
    pass


async def fgo_draw(count: int):
    #            0      1      2
    cnlist = ['★★★★★', '★★★★', '★★★']
    obj_list, obj_dict, max_star_list, star_list, max_star_index_list = _format_card_information(count)
    rst = init_star_rst(star_list, cnlist, max_star_list, max_star_index_list)
    if count > 90:
        obj_list = set_list(obj_list)
    return MessageSegment.image("base64://" + await generate_img(obj_list, 'fgo', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(obj_dict)


async def update_fgo_info():
    global ALL_CHAR, ALL_CARD
    data, code = await update_requests_info('fgo')
    if code == 200:
        ALL_CHAR = init_game_pool('fgo', data, FgoChar)
    data, code = await update_requests_info('fgo_card')
    if code == 200:
        ALL_CARD = init_game_pool('fgo_card', data, FgoChar)


async def init_fgo_data():
    global ALL_CHAR, ALL_CARD
    if FGO_FLAG:
        with open(DRAW_PATH + 'fgo.json', 'r', encoding='utf8') as f:
            fgo_dict = json.load(f)
        ALL_CHAR = init_game_pool('fgo', fgo_dict, FgoChar)
        with open(DRAW_PATH + 'fgo_card.json', 'r', encoding='utf8') as f:
            fgo_dict = json.load(f)
        ALL_CARD = init_game_pool('fgo', fgo_dict, FgoChar)


# 抽取卡池
def _get_fgo_card(mode: int = 1):
    global ALL_CHAR, ALL_CARD
    if mode == 1:
        star = get_star([8, 7, 6, 5, 4, 3], [FGO_SERVANT_FIVE_P, FGO_SERVANT_FOUR_P, FGO_SERVANT_THREE_P,
                                             FGO_CARD_FIVE_P, FGO_CARD_FOUR_P, FGO_CARD_THREE_P])
    elif mode == 2:
        star = get_star([5, 4], [FGO_CARD_FIVE_P, FGO_CARD_FOUR_P])
    else:
        star = get_star([8, 7, 6], [FGO_SERVANT_FIVE_P, FGO_SERVANT_FOUR_P, FGO_SERVANT_THREE_P])
    if star > 5:
        itype = 'servant'
        star -= 3
        chars = [x for x in ALL_CHAR if x.star == star if not x.limited]
    else:
        itype = 'card'
        chars = [x for x in ALL_CARD if x.star == star if not x.limited]
    return random.choice(chars), 5 - star, itype


# 整理数据
def _format_card_information(count: int):
    max_star_lst = []  # 获取的最高星级角色列表
    max_index_lst = []  # 获取最高星级角色的次数
    star_list = [0, 0, 0]
    obj_list = []  # 获取所有角色
    obj_dict = {}  # 获取角色次数字典
    servant_count = 0  # 保底计算
    card_count = 0  # 保底计算
    for i in range(count):
        servant_count += 1
        card_count += 1
        # 四星卡片保底
        if card_count == 9:
            obj, code, itype = _get_fgo_card(2)
        # 三星从者保底
        elif servant_count == 10:
            obj, code, itype = _get_fgo_card(3)
            _count = 0
        # 普通抽
        else:
            obj, code, itype = _get_fgo_card()
        star_list[code] += 1
        if itype == 'card' and code < 2:
            card_count = 0
        if itype == 'servant':
            servant_count = 0
        if code == 0:
            max_star_lst.append(obj.name)
            max_index_lst.append(i)
        try:
            obj_dict[obj.name] += 1
        except KeyError:
            obj_dict[obj.name] = 1
        obj_list.append(obj)
    return obj_list, obj_dict, max_star_lst, star_list, max_index_lst
