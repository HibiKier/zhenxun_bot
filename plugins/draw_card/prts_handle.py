
import os
import nonebot
import random
from .config import PRTS_FIVE_P, PRTS_FOUR_P, PRTS_SIX_P, PRTS_THREE_P
from .update_game_info import update_info
from .util import generate_img, init_star_rst, max_card, BaseData, UpEvent, set_list
from .init_card_pool import init_game_pool
from pathlib import Path
from .announcement import PrtsAnnouncement
from dataclasses import dataclass
from util.init_result import image
from configs.path_config import DRAW_PATH
from services.log import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

up_char_file = Path() / "data" / "draw_card" / "draw_card_up" / "prts_up_char.json"

prts_dict = {}
UP_OPERATOR = []
ALL_OPERATOR = []
_CURRENT_POOL_TITLE = ''


@dataclass
class Operator(BaseData):
    recruit_only: bool  # 公招限定
    event_only: bool  # 活动获得干员
    # special_only: bool  # 升变/异格干员


async def prts_draw(count: int = 300):
    cnlist = ['★★★★★★', '★★★★★', '★★★★', '★★★']
    operator_list, operator_dict, six_list, star_list, six_olist = _format_card_information(count)
    up_list = []
    if _CURRENT_POOL_TITLE:
        for x in UP_OPERATOR:
            for operator in x.operators:
                up_list.append(operator)
    rst = init_star_rst(star_list, cnlist, six_list, six_olist, up_list)
    if count > 90:
        operator_list = set_list(operator_list)
    pool_info = "当前up池: " if _CURRENT_POOL_TITLE else ""
    return pool_info + _CURRENT_POOL_TITLE + image(b64=await generate_img(operator_list, 'prts', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(operator_dict)


async def update_prts_info():
    global prts_dict, ALL_OPERATOR
    url = 'https://wiki.biligame.com/arknights/干员数据表'
    data, code = await update_info(url, 'prts', ['头像', '名称', '阵营', '星级', '性别', '是否感染', '初始生命', '初始防御',
                                                 '初始法抗', '再部署', '部署费用', '阻挡数', '攻击速度', '标签'])
    if code == 200:
        prts_dict = data
        ALL_OPERATOR = init_game_pool('prts', prts_dict, Operator)


@driver.on_startup
async def init_data():
    global prts_dict, ALL_OPERATOR
    if not os.path.exists(DRAW_PATH + '/draw_card_config/prts.json'):
        await update_prts_info()
    else:
        with open(DRAW_PATH + '/draw_card_config/prts.json', 'r', encoding='utf8') as f:
            prts_dict = json.load(f)
        ALL_OPERATOR = init_game_pool('prts', prts_dict, Operator)
    await _init_up_char()
    # print([x.operators for x in UP_OPERATOR if x.star == 5 and x.zoom > 1])


# 抽取干员
def _get_operator_card():
    star = random.sample([6, 5, 4, 3],
                         counts=[int(PRTS_SIX_P * 100), int(PRTS_FIVE_P * 100),
                                 int(PRTS_FOUR_P * 100), int(PRTS_THREE_P * 100)],
                         k=1)[0]
    if _CURRENT_POOL_TITLE:
        zooms = [x.zoom for x in UP_OPERATOR if x.star == star]
        zoom = 0
        weight = 0
        # 分配概率和权重
        for z in zooms:
            if z < 1:
                zoom = z
            else:
                weight = z
        # UP
        if random.random() < zoom:
            up_operators = [x.operators for x in UP_OPERATOR if x.star == star and x.zoom < 1][0]
            up_operator_name = random.choice(up_operators)
            # print(up_operator_name)
            acquire_operator = [x for x in ALL_OPERATOR if x.name == up_operator_name][0]
        else:
            all_star_operators = [x for x in ALL_OPERATOR if x.star == star
                                  and not any([x.limited, x.event_only, x.recruit_only])]
            weight_up_operators = [x.operators for x in UP_OPERATOR if x.star == star and x.zoom > 1]
            # 权重
            if weight_up_operators and random.random() < 1.0 / float(len(all_star_operators)) * weight:
                up_operator_name = random.choice(weight_up_operators[0])
                acquire_operator = [x for x in ALL_OPERATOR if x.name == up_operator_name][0]
            else:
                acquire_operator = random.choice(all_star_operators)
    else:
        acquire_operator = random.choice([x for x in ALL_OPERATOR if x.star == star
                                          and not any([x.limited, x.event_only, x.recruit_only])])
    # print(f'{acquire_operator}: {star}')
    return acquire_operator, abs(star - 6)


# 整理抽卡数据
def _format_card_information(count: int):
    operator_list = []  # 抽取的干员列表
    operator_dict = {}  # 抽取各干员次数
    star_list = [0, 0, 0, 0]  # 各个星级次数
    six_list = []  # 六星干员列表
    six_index_list = []  # 六星干员获取位置
    for i in range(count):
        operator, code = _get_operator_card()
        star_list[code] += 1
        if code == 0:
            six_list.append(operator.name)
            six_index_list.append(i)
        try:
            operator_dict[operator.name] += 1
        except KeyError:
            operator_dict[operator.name] = 1
        operator_list.append(operator)
    return operator_list, operator_dict, six_list, star_list, six_index_list


# 获取up干员和概率
async def _init_up_char():
    global up_char_dict, _CURRENT_POOL_TITLE
    up_char_dict = await PrtsAnnouncement.update_up_char()
    # print(up_char_dict)
    _CURRENT_POOL_TITLE = up_char_dict['title']
    up_char_dict = up_char_dict['up_char']
    logger.info(f'成功获取明日方舟当前up信息...当前up池: {_CURRENT_POOL_TITLE}')
    average_dict = {'6': {}, '5': {}, '4': {}}
    for star in up_char_dict.keys():
        for key in up_char_dict[star].keys():
            if average_dict[star].get(up_char_dict[star][key]):
                average_dict[star][up_char_dict[star][key]].append(key)
            else:
                average_dict[star][up_char_dict[star][key]] = [key]
    up_char_dict = {'6': {}, '5': {}, '4': {}}
    for star in average_dict.keys():
        for str_zoom in average_dict[star].keys():
            if str_zoom[0] == '权':
                zoom = float(str_zoom[1:])
            else:
                zoom = float(str_zoom) / 100
            UP_OPERATOR.append(UpEvent(star=int(star), operators=average_dict[star][str_zoom], zoom=zoom))


async def reload_pool():
    await _init_up_char()
