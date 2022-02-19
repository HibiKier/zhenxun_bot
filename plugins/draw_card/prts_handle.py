from nonebot.adapters.onebot.v11 import MessageSegment, Message
import random
from .config import DRAW_DATA_PATH, draw_config
from .update_game_info import update_info
from .util import generate_img, init_star_rst, max_card, BaseData, UpEvent, set_list, get_star
from .init_card_pool import init_game_pool
from .announcement import PrtsAnnouncement
from dataclasses import dataclass
from nonebot.log import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json


announcement = PrtsAnnouncement()

prts_dict = {}
UP_OPERATOR = []
ALL_OPERATOR = []
_CURRENT_POOL_TITLE = ''
POOL_IMG = ''


@dataclass
class Operator(BaseData):
    recruit_only: bool  # 公招限定
    event_only: bool  # 活动获得干员
    # special_only: bool  # 升变/异格干员


async def prts_draw(count: int = 300):
    cnlist = ['★★★★★★', '★★★★★', '★★★★', '★★★']
    star_list = [0, 0, 0, 0]
    operator_list, operator_dict, six_list, star_list, six_index_list = format_card_information(count, star_list)
    up_list = []
    tmp = ''
    if _CURRENT_POOL_TITLE:
        for x in UP_OPERATOR:
            for operator in x.operators:
                up_list.append(operator)
            if x.star == 6:
                tmp += f'六星UP：{" ".join(x.operators)} \n'
            elif x.star == 5:
                tmp += f'五星UP：{" ".join(x.operators)} \n'
            elif x.star == 4:
                tmp += f'四星UP：{" ".join(x.operators)}'
    rst = init_star_rst(star_list, cnlist, six_list, six_index_list, up_list)
    if count > 90:
        operator_list = set_list(operator_list)
    pool_info = f"当前up池: {_CURRENT_POOL_TITLE}\n{tmp}" if _CURRENT_POOL_TITLE else ""
    return pool_info + MessageSegment.image(
        "base64://" + await generate_img(operator_list, 'prts', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(operator_dict)


async def update_prts_info():
    global prts_dict, ALL_OPERATOR
    url = 'https://wiki.biligame.com/arknights/干员数据表'
    data, code = await update_info(url, 'prts', ['头像', '名称', '阵营', '星级', '性别', '是否感染', '获取途径', '初始生命', '初始防御',
                                                 '初始法抗', '再部署', '部署费用', '阻挡数', '攻击速度', '标签'])
    if code == 200:
        prts_dict = data
        ALL_OPERATOR = init_game_pool('prts', prts_dict, Operator)
        await _init_up_char()


async def init_prts_data():
    global prts_dict, ALL_OPERATOR
    if draw_config.PRTS_FLAG:
        with (DRAW_DATA_PATH / 'prts.json').open('r', encoding='utf8') as f:
            prts_dict = json.load(f)
        ALL_OPERATOR = init_game_pool('prts', prts_dict, Operator)
        await _init_up_char()


# 抽取干员
def _get_operator_card(add: float):
    prts_config = draw_config.prts
    star = get_star([6, 5, 4, 3], [prts_config.PRTS_SIX_P + add, prts_config.PRTS_FIVE_P, prts_config.PRTS_FOUR_P, prts_config.PRTS_THREE_P])
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
        up_operator_name = ""
        # UPs
        try:
            if 0 < zoom:
                up_operators = [x.operators for x in UP_OPERATOR if x.star == star and x.zoom < 1][0]
                up_operator_name = random.choice(up_operators)
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
        except IndexError:
            acquire_operator = Operator(up_operator_name, star, True, False, False)
    else:
        acquire_operator = random.choice([x for x in ALL_OPERATOR if x.star == star
                                          and not any([x.limited, x.event_only, x.recruit_only])])
    return acquire_operator, 6 - star


# 整理数据
def format_card_information(count: int, star_list: list):
    max_star_lst = []       # 获取的最高星级角色列表
    max_index_lst = []      # 获取最高星级角色的次数
    obj_list = []           # 获取所有角色
    obj_dict = {}           # 获取角色次数字典
    add = 0.0
    count_idx = 0
    for i in range(count):
        count_idx += 1
        obj, code = _get_operator_card(add)
        star_list[code] += 1
        if code == 0:
            max_star_lst.append(obj.name)
            max_index_lst.append(i)
            add = 0.0
            count_idx = 0
        elif count_idx > 50:
            add += 0.02
        try:
            obj_dict[obj.name] += 1
        except KeyError:
            obj_dict[obj.name] = 1
        obj_list.append(obj)
    return obj_list, obj_dict, max_star_lst, star_list, max_index_lst


# 获取up干员和概率
async def _init_up_char():
    global _CURRENT_POOL_TITLE, POOL_IMG, UP_OPERATOR
    UP_OPERATOR = []
    up_char_dict = await announcement.update_up_char()
    _CURRENT_POOL_TITLE = up_char_dict['char']['title']
    if _CURRENT_POOL_TITLE:
        POOL_IMG = MessageSegment.image(up_char_dict['char']['pool_img'])
    up_char_dict = up_char_dict['char']['up_char']
    logger.info(f'成功获取明日方舟当前up信息...当前up池: {_CURRENT_POOL_TITLE}')
    average_dict = {'6': {}, '5': {}, '4': {}}
    for star in up_char_dict.keys():
        for key in up_char_dict[star].keys():
            if average_dict[star].get(up_char_dict[star][key]):
                average_dict[star][up_char_dict[star][key]].append(key)
            else:
                average_dict[star][up_char_dict[star][key]] = [key]
    for star in average_dict.keys():
        for str_zoom in average_dict[star].keys():
            if str_zoom[0] == '权':
                zoom = float(str_zoom[1:])
            else:
                zoom = float(str_zoom) / 100
            UP_OPERATOR.append(UpEvent(star=int(star), operators=average_dict[star][str_zoom], zoom=zoom))


async def reload_prts_pool():
    await _init_up_char()
    return Message(f'当前UP池：{_CURRENT_POOL_TITLE} {POOL_IMG}')
