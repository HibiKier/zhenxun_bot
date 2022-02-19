from nonebot.adapters.onebot.v11 import MessageSegment, Message
import random
from .update_game_info import update_info
from .util import (
    generate_img,
    init_rst,
    BaseData,
    set_list,
    get_star,
    init_up_char,
)
from .config import DRAW_DATA_PATH, draw_config
from .count_manager import GenshinCountManager
from dataclasses import dataclass
from .init_card_pool import init_game_pool
from .announcement import GenshinAnnouncement

try:
    import ujson as json
except ModuleNotFoundError:
    import json


announcement = GenshinAnnouncement()

draw_count_manager = GenshinCountManager((10, 90), ("4", "5"))

# genshin_five = {}
# genshin_count = {}
# genshin_pl_count = {}

ALL_CHAR = []
ALL_ARMS = []

UP_CHAR = []
UP_ARMS = []


_CURRENT_CHAR_POOL_TITLE = ""
_CURRENT_ARMS_POOL_TITLE = ""
POOL_IMG = ""


@dataclass
class GenshinChar(BaseData):
    pass


async def genshin_draw(user_id: int, count: int, pool_name: str):
    #                   0      1      2
    star = ["★★★★★", "★★★★", "★★★"]
    (
        char_list,
        five_dict,
        star_num_list,
    ) = _format_card_information(count, user_id, pool_name)
    title = ""
    up_type = []
    up_list = []
    if pool_name == "char" and _CURRENT_CHAR_POOL_TITLE:
        up_type = UP_CHAR
        title = _CURRENT_CHAR_POOL_TITLE
    elif pool_name == "arms" and _CURRENT_ARMS_POOL_TITLE:
        up_type = UP_ARMS
        title = _CURRENT_ARMS_POOL_TITLE
    tmp = ""
    if up_type:
        for x in up_type:
            for operator in x.operators:
                up_list.append(operator)
            if x.star == 5:
                tmp += f'五星UP：{" ".join(x.operators)} \n'
            elif x.star == 4:
                tmp += f'四星UP：{" ".join(x.operators)}'
    rst = init_rst(five_dict, star_num_list, star, up_list)
    pool_info = f"当前up池：{title}\n{tmp}" if title else ""
    if count > 90:
        char_list = set_list(char_list)
    return (
        pool_info
        + "\n"
        + MessageSegment.image(
            "base64://" + await generate_img(char_list, "genshin", star_num_list)
        )
        + rst
        + f'\n距离保底发还剩 {draw_count_manager.get_user_count(user_id, 1) % 90} 抽'
        + "\n【五星：0.6%，四星：5.1%\n第72抽开始五星概率每抽加0.585%】"
    )


async def update_genshin_info():
    global ALL_CHAR, ALL_ARMS
    url = "https://wiki.biligame.com/ys/角色筛选"
    data, code = await update_info(url, "genshin")
    if code == 200:
        ALL_CHAR = init_game_pool("genshin", data, GenshinChar)
    url = "https://wiki.biligame.com/ys/武器图鉴"
    data, code = await update_info(
        url,
        "genshin_arms",
    )
    if code == 200:
        ALL_ARMS = init_game_pool("genshin_arms", data, GenshinChar)
    await _genshin_init_up_char()


async def init_genshin_data():
    global ALL_CHAR, ALL_ARMS
    if draw_config.GENSHIN_FLAG:
        if not (DRAW_DATA_PATH / "genshin.json").exists() or not (DRAW_DATA_PATH / "genshin_arms.json").exists():
            await update_genshin_info()
        else:
            with (DRAW_DATA_PATH / "genshin.json").open("r", encoding="utf8") as f:
                genshin_dict = json.load(f)
            with (DRAW_DATA_PATH / "genshin_arms.json").open("r", encoding="utf8") as f:
                genshin_ARMS_dict = json.load(f)
            ALL_CHAR = init_game_pool("genshin", genshin_dict, GenshinChar)
            ALL_ARMS = init_game_pool("genshin_arms", genshin_ARMS_dict, GenshinChar)
        await _genshin_init_up_char()


# 抽取卡池
def _get_genshin_card(mode: int = 1, pool_name: str = "", add: float = 0.0, is_up: bool = False):
    """
    mode 1：普通抽 2：四星保底 3：五星保底
    """
    global ALL_ARMS, ALL_CHAR, UP_ARMS, UP_CHAR, _CURRENT_ARMS_POOL_TITLE, _CURRENT_CHAR_POOL_TITLE
    genshin_config = draw_config.genshin
    if mode == 1:
        star = get_star(
            [5, 4, 3], [genshin_config.GENSHIN_FIVE_P + add, genshin_config.GENSHIN_FOUR_P, genshin_config.GENSHIN_THREE_P]
        )
    elif mode == 2:
        star = get_star([5, 4], [genshin_config.GENSHIN_G_FIVE_P + add, genshin_config.GENSHIN_G_FOUR_P])
    else:
        star = 5
    if pool_name == "char":
        data_lst = UP_CHAR
        flag = _CURRENT_CHAR_POOL_TITLE
        type_all_lst = ALL_CHAR + [
            x for x in ALL_ARMS if x.star == star and x.star < 5
        ]
    elif pool_name == "arms":
        data_lst = UP_ARMS
        flag = _CURRENT_ARMS_POOL_TITLE
        type_all_lst = ALL_ARMS + [
            x for x in ALL_CHAR if x.star == star and x.star < 5
        ]
    else:
        data_lst = ""
        flag = ""
        type_all_lst = ""
    all_lst = ALL_ARMS + ALL_CHAR
    # 是否UP
    try:
        if flag and star > 3:
            # 获取up角色列表
            up_char_lst = [x.operators for x in data_lst if x.star == star][0]
            # print(up_char_lst)
            # 成功获取up角色
            if random.random() < 0.5 or is_up:
                up_char_name = random.choice(up_char_lst)
                acquire_char = [x for x in all_lst if x.name == up_char_name][0]
            else:
                # 无up
                all_char_lst = [
                    x
                    for x in type_all_lst
                    if x.star == star and x.name not in up_char_lst and not x.limited
                ]
                acquire_char = random.choice(all_char_lst)
        else:
            chars = [x for x in all_lst if x.star == star and not x.limited]
            acquire_char = random.choice(chars)
    except IndexError:
        chars = [x for x in all_lst if x.star == star and not x.limited]
        acquire_char = random.choice(chars)
    return acquire_char, 5 - star


def _format_card_information(_count: int, user_id, pool_name):
    char_list = []              # 获取角色列表
    star_num_list = [0, 0, 0]       # 各个星级数量
    five_dict = {}              # 五星数量
    add = 0.0
    pool = UP_CHAR if pool_name == 'char' else UP_ARMS
    for _ in range(_count):
        draw_count_manager.increase(user_id)
        star = draw_count_manager.check(user_id)
        if (draw_count_manager.get_user_count(user_id) - draw_count_manager.get_user_count(user_id, 1)) % 90 >= 72:
            add += draw_config.genshin.I72_ADD
        if star:
            star = int(star)
            if star == 4:
                char, code = _get_genshin_card(2, pool_name, add=add)
                draw_count_manager.record_count(user_id, 0)
            else:
                char, code = _get_genshin_card(3, pool_name, add, draw_count_manager.is_up(user_id))
        else:
            char, code = _get_genshin_card(1, pool_name, add, draw_count_manager.is_up(user_id))
        if code == 0:
            add = 0
            if not five_dict.get(char.name):
                five_dict[char.name] = [draw_count_manager.get_user_count(user_id)]
            else:
                five_dict[char.name].append(draw_count_manager.get_user_count(user_id) % 90)
            draw_count_manager.set_count(user_id, 2, draw_count_manager.get_user_count(user_id, 1))
            draw_count_manager.record_count(user_id, 0)
            draw_count_manager.record_count(user_id, 1)
            if char.name not in [x.operators for x in pool if x.star == 5][0]:
                draw_count_manager.set_is_up(user_id, True)
            else:
                draw_count_manager.set_is_up(user_id, False)
        star_num_list[code] += 1
        char_list.append(char)
    return char_list, five_dict, star_num_list






    # if genshin_count.get(user_id) and _count <= 90:
    #     f_count = genshin_count[user_id]
    # else:
    #     f_count = 0
    # if genshin_pl_count.get(user_id) and _count <= 90:
    #     count = genshin_pl_count[user_id]
    # else:
    #     count = 0
    # for i in range(_count):
    #     count += 1
    #     f_count += 1
    #     # 十连保底
    #     if count == 10 and f_count != 90:
    #         if f_count >= 72:
    #             add += I72_ADD
    #         char, code = _get_genshin_card(2, pool_name, add=add)
    #         count = 0
    #     # 大保底
    #     elif f_count == 90:
    #         char, code = _get_genshin_card(3, pool_name)
    #     else:
    #         if f_count >= 72:
    #             add += I72_ADD
    #         char, code = _get_genshin_card(pool_name=pool_name, add=add)
    #         if code == 1:
    #             count = 0
    #     star_list[code] += 1
    #     if code == 0:
    #         if _count <= 90:
    #             genshin_five[user_id] = f_count
    #         add = 0.0
    #         f_count = 0
    #         five_list.append(char.name)
    #         five_index_list.append(i)
    #         try:
    #             five_dict[char.name] += 1
    #         except KeyError:
    #             five_dict[char.name] = 1
    #     char_list.append(char)
    # if _count <= 90:
    #     genshin_count[user_id] = f_count
    #     genshin_pl_count[user_id] = count
    # return char_list, five_list, five_index_list, five_dict, star_list


def reset_count(user_id: int):
    draw_count_manager.reset(user_id)


# 获取up和概率
async def _genshin_init_up_char():
    global _CURRENT_CHAR_POOL_TITLE, _CURRENT_ARMS_POOL_TITLE, UP_CHAR, UP_ARMS, POOL_IMG
    (
        _CURRENT_CHAR_POOL_TITLE,
        _CURRENT_ARMS_POOL_TITLE,
        POOL_IMG,
        UP_CHAR,
        UP_ARMS,
    ) = await init_up_char(announcement)


async def reload_genshin_pool():
    await _genshin_init_up_char()
    return Message(
        f"当前UP池子：{_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_ARMS_POOL_TITLE} {POOL_IMG}"
    )
