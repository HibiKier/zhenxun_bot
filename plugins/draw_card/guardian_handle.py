
import os
import nonebot
from nonebot.adapters.cqhttp import MessageSegment
from .update_game_info import update_info
from services.log import logger
from .announcement import GuardianAnnouncement
from .util import init_star_rst, generate_img, max_card, BaseData,\
    set_list, get_star, format_card_information, UpEvent
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

_CURRENT_CHAR_POOL_TITLE = ''
_CURRENT_ARMS_POOL_TITLE = ''
UP_CHAR = []
UP_ARMS = []
POOL_IMG = ''


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
    title = ''
    up_type = []
    up_list = []
    if pool_name == 'char' and _CURRENT_CHAR_POOL_TITLE:
        up_type = UP_CHAR
        title = _CURRENT_CHAR_POOL_TITLE
    elif pool_name == 'arms' and _CURRENT_ARMS_POOL_TITLE:
        up_type = UP_ARMS
        title = _CURRENT_ARMS_POOL_TITLE
    tmp = ''
    if up_type:
        for x in up_type:
            for operator in x.operators:
                up_list.append(operator)
            if pool_name == 'char':
                if x.star == 3:
                    tmp += f'三星UP：{" ".join(x.operators)} \n'
            else:
                if x.star == 5:
                    tmp += f'五星UP：{" ".join(x.operators)}'
    obj_list, obj_dict, max_list, star_list, max_index_list = format_card_information(count, star_list,
                                                                                      _get_guardian_card, pool_name)
    rst = init_star_rst(star_list, cnlist, max_list, max_index_list, up_list)
    pool_info = f'当前up池：{title}\n{tmp}' if title else ''
    if count > 90:
        obj_list = set_list(obj_list)
    return pool_info + '\n' + MessageSegment.image(
        "base64://" + await generate_img(obj_list, 'guardian', star_list)) \
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


async def init_guardian_data():
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
        await _init_up_char()


# 抽取卡池
def _get_guardian_card(pool_name: str):
    global ALL_ARMS, ALL_CHAR, UP_ARMS, UP_CHAR, _CURRENT_ARMS_POOL_TITLE, _CURRENT_CHAR_POOL_TITLE
    if pool_name == 'char':
        star = get_star([3, 2, 1], [GUARDIAN_THREE_CHAR_P, GUARDIAN_TWO_CHAR_P, GUARDIAN_ONE_CHAR_P])
        up_lst = UP_CHAR
        flag = _CURRENT_CHAR_POOL_TITLE
        _max_star = 3
        all_data = ALL_CHAR
    else:
        star = get_star([5, 4, 3, 2], [GUARDIAN_FIVE_ARMS_P, GUARDIAN_FOUR_ARMS_P,
                                       GUARDIAN_THREE_ARMS_P, GUARDIAN_TWO_ARMS_P])
        up_lst = UP_ARMS
        flag = _CURRENT_ARMS_POOL_TITLE
        _max_star = 5
        all_data = ALL_ARMS
    # 是否UP
    if flag and star == _max_star and pool_name:
        # 获取up角色列表
        up_char_lst = [x.operators for x in up_lst if x.star == star][0]
        # 成功获取up角色
        if random.random() < 0.5:
            up_char_name = random.choice(up_char_lst)
            acquire_char = [x for x in all_data if x.name == up_char_name][0]
        else:
            # 无up
            all_char_lst = [x for x in all_data if x.star == star and x.name not in up_char_lst and not x.limited]
            acquire_char = random.choice(all_char_lst)
    else:
        chars = [x for x in all_data if x.star == star and not x.limited]
        acquire_char = random.choice(chars)
    return acquire_char, _max_star - star


# 获取up和概率
async def _init_up_char():
    global _CURRENT_CHAR_POOL_TITLE, _CURRENT_ARMS_POOL_TITLE, UP_CHAR, UP_ARMS, POOL_IMG
    UP_CHAR = []
    UP_ARMS = []
    up_char_dict = await GuardianAnnouncement.update_up_char()
    _CURRENT_CHAR_POOL_TITLE = up_char_dict['char']['title']
    _CURRENT_ARMS_POOL_TITLE = up_char_dict['arms']['title']
    if _CURRENT_CHAR_POOL_TITLE and _CURRENT_ARMS_POOL_TITLE:
        POOL_IMG = MessageSegment.image(up_char_dict['char']['pool_img']) + \
                   MessageSegment.image(up_char_dict['arms']['pool_img'])
    logger.info(f'成功获取坎公骑冠剑当前up信息...当前up池: {_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_ARMS_POOL_TITLE}')
    for key in up_char_dict.keys():
        for star in up_char_dict[key]['up_char'].keys():
            up_char_lst = []
            for char in up_char_dict[key]['up_char'][star].keys():
                up_char_lst.append(char)
            if key == 'char':
                UP_CHAR.append(UpEvent(star=int(star), operators=up_char_lst, zoom=0))
            else:
                UP_ARMS.append(UpEvent(star=int(star), operators=up_char_lst, zoom=0))


async def reload_guardian_pool():
    await _init_up_char()
    return f'当前UP池子：{_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_ARMS_POOL_TITLE} {POOL_IMG}'
