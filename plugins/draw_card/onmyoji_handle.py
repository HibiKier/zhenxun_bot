
from nonebot.adapters.cqhttp import MessageSegment
import random
from .update_game_requests_info import update_requests_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star, max_card
from .config import ONMYOJI_SR, ONMYOJI_SSR, ONMYOJI_SP, ONMYOJI_R, DRAW_PATH, ONMYOJI_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
import nonebot
try:
    import ujson as json
except ModuleNotFoundError:
    import json

ALL_CHAR = []


@dataclass
class OnmyojiChar(BaseData):
    pass


async def onmyoji_draw(count: int):
    #            0      1      2
    cnlist = ['SP', 'SSR', 'SR', 'R']
    obj_list, obj_dict, star_list, rst = format_card_information(count)
    rst = init_star_rst(star_list, cnlist, [], []) + rst
    if count > 90:
        obj_list = set_list(obj_list)
    return MessageSegment.image("base64://" + await generate_img(obj_list, 'onmyoji', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(obj_dict)


async def update_onmyoji_info():
    global ALL_CHAR
    data, code = await update_requests_info('onmyoji')
    if code == 200:
        ALL_CHAR = init_game_pool('onmyoji', data, OnmyojiChar)


async def init_onmyoji_data():
    global ALL_CHAR
    if ONMYOJI_FLAG:
        with open(DRAW_PATH + 'onmyoji.json', 'r', encoding='utf8') as f:
            azur_dict = json.load(f)
        ALL_CHAR = init_game_pool('onmyoji', azur_dict, OnmyojiChar)


onmyoji_star = {
    5: 'SP',
    4: 'SSR',
    3: 'SR',
    2: 'R',
}


# 抽取卡池
def _get_onmyoji_card():
    global ALL_CHAR
    star = get_star([5, 4, 3, 2], [ONMYOJI_SP, ONMYOJI_SSR, ONMYOJI_SR, ONMYOJI_R])
    chars = [x for x in ALL_CHAR if x.star == onmyoji_star[star] and not x.limited]
    return random.choice(chars), 5 - star


def format_card_information(count: int):
    star_list = [0, 0, 0, 0]
    obj_list = []           # 获取所有角色
    obj_dict = {}           # 获取角色次数字典
    rst = ''
    for i in range(count):
        obj, code = _get_onmyoji_card()
        star_list[code] += 1
        if code == 0:
            rst += f'第 {i+1} 抽获取SP {obj.name}\n'
        elif code == 1:
            rst += f'第 {i+1} 抽获取SSR {obj.name}\n'
        try:
            obj_dict[obj.name] += 1
        except KeyError:
            obj_dict[obj.name] = 1
        obj_list.append(obj)
    return obj_list, obj_dict, star_list, rst

