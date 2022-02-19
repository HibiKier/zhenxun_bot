from nonebot.adapters.onebot.v11 import MessageSegment
import random
from .update_game_simple_info import update_simple_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star, max_card, format_card_information
from .config import draw_config, DRAW_DATA_PATH
from dataclasses import dataclass
from .init_card_pool import init_game_pool
try:
    import ujson as json
except ModuleNotFoundError:
    import json

ALL_CHAR = []


@dataclass
class AzurChar(BaseData):
    type_: str      # 舰娘类型


async def azur_draw(count: int, pool_name: str):
    #            0      1      2
    cnlist = ['金', '紫', '蓝', '白']
    star_list = [0, 0, 0, 0]
    char_list, char_dict, max_star_list, star_list, max_star_index_list = \
        format_card_information(count, star_list, _get_azur_card, pool_name, guaranteed=False)
    rst = init_star_rst(star_list, cnlist, max_star_list, max_star_index_list)
    if count > 90:
        char_list = set_list(char_list)
    return MessageSegment.image("base64://" + await generate_img(char_list, 'azur', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(char_dict)


async def update_azur_info():
    global ALL_CHAR
    url = 'https://wiki.biligame.com/blhx/舰娘图鉴'
    data, code = await update_simple_info(url, 'azur')
    if code == 200:
        ALL_CHAR = init_game_pool('azur', data, AzurChar)


async def init_azur_data():
    global ALL_CHAR
    if draw_config.AZUR_FLAG:
        with (DRAW_DATA_PATH / 'azur.json').open('r', encoding='utf8') as f:
            azur_dict = json.load(f)
        ALL_CHAR = init_game_pool('azur', azur_dict, AzurChar)


# 抽取卡池
def _get_azur_card(pool_name: str, mode: int = 1):
    global ALL_CHAR
    azur_config = draw_config.azur
    if pool_name == '轻型':
        type_ = ['驱逐', '轻巡', '维修']
    elif pool_name == '重型':
        type_ = ['重巡', '战列', '战巡', '重炮']
    else:
        type_ = ['维修', '潜艇', '重巡', '轻航', '航母']
    star = get_star([4, 3, 2, 1], [azur_config.AZUR_FOUR_P, azur_config.AZUR_THREE_P, azur_config.AZUR_TWO_P, azur_config.AZUR_ONE_P])
    chars = [x for x in ALL_CHAR if x.star == star and x.type_ in type_ and not x.limited]
    return random.choice(chars), 4 - star
