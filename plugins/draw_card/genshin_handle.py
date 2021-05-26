
import os
from util.init_result import image
import nonebot
import random
from .update_game_info import update_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star
from .config import GENSHIN_FIVE_P, GENSHIN_FOUR_P, GENSHIN_G_FIVE_P, GENSHIN_G_FOUR_P, GENSHIN_THREE_P, I72_ADD, \
    DRAW_PATH, GENSHIN_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

genshin_five = {}
genshin_count = {}
genshin_pl_count = {}

ALL_CHAR = []
ALL_ARMS = []


@dataclass
class GenshinChar(BaseData):
    pass


async def genshin_draw(user_id: int, count: int):
    #                   0      1      2
    cnlist = ['★★★★★', '★★★★', '★★★']
    char_list, five_list, five_index_list, char_dict, star_list = _format_card_information(count, user_id)
    rst = init_star_rst(star_list, cnlist, five_list, five_index_list)
    temp = ''
    if count > 90:
        char_list = set_list(char_list)
    return image(b64=await generate_img(char_list, 'genshin', star_list)) + '\n' + rst[:-1] + \
           temp[:-1] + f'\n距离保底发还剩 {90 - genshin_count[user_id] if genshin_count.get(user_id) else "^"} 抽' \
           + "\n【五星：0.6%，四星：5.1%\n第72抽开始五星概率每抽加0.585%】"


async def update_genshin_info():
    global ALL_CHAR, ALL_ARMS
    url = 'https://wiki.biligame.com/ys/角色筛选'
    data, code = await update_info(url, 'genshin')
    if code == 200:
        ALL_CHAR = init_game_pool('genshin', data, GenshinChar)
    url = 'https://wiki.biligame.com/ys/武器图鉴'
    data, code = await update_info(url, 'genshin_arms', ['头像', '名称', '类型', '稀有度.alt',
                                                         '获取途径', '初始基础属性1', '初始基础属性2',
                                                         '攻击力（MAX）', '副属性（MAX）', '技能'])
    if code == 200:
        ALL_ARMS = init_game_pool('genshin', data, GenshinChar)


# asyncio.get_event_loop().run_until_complete(update_genshin_info())


@driver.on_startup
async def init_data():
    global ALL_CHAR, ALL_ARMS
    if GENSHIN_FLAG:
        if not os.path.exists(DRAW_PATH + 'genshin.json') or not os.path.exists(DRAW_PATH + 'genshin_arms.json'):
            await update_genshin_info()
        else:
            with open(DRAW_PATH + 'genshin.json', 'r', encoding='utf8') as f:
                genshin_dict = json.load(f)
            with open(DRAW_PATH + 'genshin_arms.json', 'r', encoding='utf8') as f:
                genshin_ARMS_dict = json.load(f)
            ALL_CHAR = init_game_pool('genshin', genshin_dict, GenshinChar)
            ALL_ARMS = init_game_pool('genshin', genshin_ARMS_dict, GenshinChar)


# 抽取卡池
def _get_genshin_card(mode: int = 1, add: float = 0.0):
    global ALL_ARMS, ALL_CHAR
    if mode == 1:
        star = get_star([5, 4, 3], [GENSHIN_FIVE_P + add, GENSHIN_FOUR_P, GENSHIN_THREE_P])
    elif mode == 2:
        star = get_star([5, 4], [GENSHIN_G_FIVE_P + add, GENSHIN_G_FOUR_P])
    else:
        star = 5
    chars = [x for x in (ALL_ARMS if random.random() < 0.5 or star == 3 else ALL_CHAR) if x.star == star]
    return random.choice(chars), abs(star - 5)


def _format_card_information(_count: int, user_id):
    char_list = []
    star_list = [0, 0, 0]
    five_index_list = []
    five_list = []
    five_dict = {}
    add = 0.0
    if genshin_count.get(user_id) and _count <= 90:
        f_count = genshin_count[user_id]
    else:
        f_count = 0
    if genshin_pl_count.get(user_id) and _count <= 90:
        count = genshin_pl_count[user_id]
    else:
        count = 0
    for i in range(_count):
        count += 1
        f_count += 1
        # 十连保底
        if count == 10 and f_count != 90:
            if f_count >= 72:
                add += I72_ADD
            char, code = _get_genshin_card(2, add)
            count = 0
        # 大保底
        elif f_count == 90:
            char, code = _get_genshin_card(3)
        else:
            if f_count >= 72:
                add += I72_ADD
            char, code = _get_genshin_card(add=add)
            if code == 1:
                count = 0
        star_list[code] += 1
        if code == 0:
            if _count <= 90:
                genshin_five[user_id] = f_count
            add = 0.0
            f_count = 0
            five_list.append(char.name)
            five_index_list.append(i)
            try:
                five_dict[char.name] += 1
            except KeyError:
                five_dict[char.name] = 1
        char_list.append(char)
    if _count <= 90:
        genshin_count[user_id] = f_count
        genshin_pl_count[user_id] = count
    return char_list, five_list, five_index_list, five_dict, star_list


def reset_count(user_id: int):
    genshin_count[user_id] = 0
    genshin_pl_count[user_id] = 0
