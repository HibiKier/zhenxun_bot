import random
from enum import Enum

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.services.log import logger

from .models.buff_skin import BuffSkin

BLUE = 0.7981
BLUE_ST = 0.0699
PURPLE = 0.1626
PURPLE_ST = 0.0164
PINK = 0.0315
PINK_ST = 0.0048
RED = 0.0057
RED_ST = 0.00021
KNIFE = 0.0021
KNIFE_ST = 0.000041

# 崭新
FACTORY_NEW_S = 0
FACTORY_NEW_E = 0.0699999
# 略磨
MINIMAL_WEAR_S = 0.07
MINIMAL_WEAR_E = 0.14999
# 久经
FIELD_TESTED_S = 0.15
FIELD_TESTED_E = 0.37999
# 破损
WELL_WORN_S = 0.38
WELL_WORN_E = 0.44999
# 战痕
BATTLE_SCARED_S = 0.45
BATTLE_SCARED_E = 0.99999


class UpdateType(Enum):
    """
    更新类型
    """

    CASE = "case"
    WEAPON_TYPE = "weapon_type"


NAME2COLOR = {
    "消费级": "WHITE",
    "工业级": "LIGHTBLUE",
    "军规级": "BLUE",
    "受限": "PURPLE",
    "保密": "PINK",
    "隐秘": "RED",
    "非凡": "KNIFE",
}

COLOR2NAME = {
    "WHITE": "消费级",
    "LIGHTBLUE": "工业级",
    "BLUE": "军规级",
    "PURPLE": "受限",
    "PINK": "保密",
    "RED": "隐秘",
    "KNIFE": "非凡",
}

COLOR2COLOR = {
    "WHITE": (255, 255, 255),
    "LIGHTBLUE": (0, 179, 255),
    "BLUE": (0, 85, 255),
    "PURPLE": (149, 0, 255),
    "PINK": (255, 0, 162),
    "RED": (255, 34, 0),
    "KNIFE": (255, 225, 0),
}

ABRASION_SORT = ["崭新出厂", "略有磨损", "久经沙场", "破损不堪", "战横累累"]

CASE_BACKGROUND = IMAGE_PATH / "csgo_cases" / "_background" / "shu"

# 刀
KNIFE2ID = {
    "鲍伊猎刀": "weapon_knife_survival_bowie",
    "蝴蝶刀": "weapon_knife_butterfly",
    "弯刀": "weapon_knife_falchion",
    "折叠刀": "weapon_knife_flip",
    "穿肠刀": "weapon_knife_gut",
    "猎杀者匕首": "weapon_knife_tactical",
    "M9刺刀": "weapon_knife_m9_bayonet",
    "刺刀": "weapon_bayonet",
    "爪子刀": "weapon_knife_karambit",
    "暗影双匕": "weapon_knife_push",
    "短剑": "weapon_knife_stiletto",
    "熊刀": "weapon_knife_ursus",
    "折刀": "weapon_knife_gypsy_jackknife",
    "锯齿爪刀": "weapon_knife_widowmaker",
    "海豹短刀": "weapon_knife_css",
    "系绳匕首": "weapon_knife_cord",
    "求生匕首": "weapon_knife_canis",
    "流浪者匕首": "weapon_knife_outdoor",
    "骷髅匕首": "weapon_knife_skeleton",
    "血猎手套": "weapon_bloodhound_gloves",
    "驾驶手套": "weapon_driver_gloves",
    "手部束带": "weapon_hand_wraps",
    "摩托手套": "weapon_moto_gloves",
    "专业手套": "weapon_specialist_gloves",
    "运动手套": "weapon_sport_gloves",
    "九头蛇手套": "weapon_hydra_gloves",
    "狂牙手套": "weapon_brokenfang_gloves",
}

WEAPON2ID = {}

# 武器箱
CASE2ID = {
    "变革": "set_community_32",
    "反冲": "set_community_31",
    "梦魇": "set_community_30",
    "激流": "set_community_29",
    "蛇噬": "set_community_28",
    "狂牙大行动": "set_community_27",
    "裂空": "set_community_26",
    "棱彩2号": "set_community_25",
    "CS20": "set_community_24",
    "裂网大行动": "set_community_23",
    "棱彩": "set_community_22",
    "头号特训": "set_community_21",
    "地平线": "set_community_20",
    "命悬一线": "set_community_19",
    "光谱2号": "set_community_18",
    "九头蛇大行动": "set_community_17",
    "光谱": "set_community_16",
    "手套": "set_community_15",
    "伽玛2号": "set_gamma_2",
    "伽玛": "set_community_13",
    "幻彩3号": "set_community_12",
    "野火大行动": "set_community_11",
    "左轮": "set_community_10",
    "暗影": "set_community_9",
    "弯曲猎手": "set_community_8",
    "幻彩2号": "set_community_7",
    "幻彩": "set_community_6",
    "先锋": "set_community_5",
    "电竞2014夏季": "set_esports_iii",
    "突围大行动": "set_community_4",
    "猎杀者": "set_community_3",
    "凤凰": "set_community_2",
    "电竞2013冬季": "set_esports_ii",
    "冬季攻势": "set_community_1",
    "军火交易3号": "set_weapons_iii",
    "英勇": "set_bravo_i",
    "电竞2013": "set_esports",
    "军火交易2号": "set_weapons_ii",
    "军火交易": "set_weapons_i",
}


def get_wear(rand: float) -> str:
    """判断磨损度

    Args:
        rand (float): 随机rand

    Returns:
        str: 磨损名称
    """
    if rand <= FACTORY_NEW_E:
        return "崭新出厂"
    if MINIMAL_WEAR_S <= rand <= MINIMAL_WEAR_E:
        return "略有磨损"
    if FIELD_TESTED_S <= rand <= FIELD_TESTED_E:
        return "久经沙场"
    if WELL_WORN_S <= rand <= WELL_WORN_E:
        return "破损不堪"
    return "战痕累累"


def random_color_and_st(rand: float) -> tuple[str, bool]:
    """获取皮肤品质及是否暗金

    参数:
        rand (float): 随机rand

    返回:
        tuple[str, bool]: 品质，是否暗金
    """
    if rand <= KNIFE:
        if random.random() <= KNIFE_ST:
            return ("KNIFE", True)
        return ("KNIFE", False)
    elif KNIFE < rand <= RED:
        if random.random() <= RED_ST:
            return ("RED", True)
        return ("RED", False)
    elif RED < rand <= PINK:
        if random.random() <= PINK_ST:
            return ("PINK", True)
        return ("PINK", False)
    elif PINK < rand <= PURPLE:
        if random.random() <= PURPLE_ST:
            return ("PURPLE", True)
        return ("PURPLE", False)
    else:
        if random.random() <= BLUE_ST:
            return ("BLUE", True)
        return ("BLUE", False)


async def random_skin(num: int, case_name: str) -> list[tuple[BuffSkin, float]]:
    """
    随机抽取皮肤
    """
    case_name = case_name.replace("武器箱", "").replace(" ", "")
    color_map = {}
    for _ in range(num):
        rand = random.random()
        # 尝试降低磨损
        if rand > MINIMAL_WEAR_E:
            for _ in range(2):
                if random.random() < 0.5:
                    logger.debug(f"[START]开箱随机磨损触发降低磨损条件: {rand}")
                    if random.random() < 0.2:
                        rand /= 3
                    else:
                        rand /= 2
                    logger.debug(f"[END]开箱随机磨损触发降低磨损条件: {rand}")
                    break
        abrasion = get_wear(rand)
        logger.debug(f"开箱随机磨损: {rand} | {abrasion}")
        color, is_stattrak = random_color_and_st(rand)
        if not color_map.get(color):
            color_map[color] = {}
        if is_stattrak:
            if not color_map[color].get(f"{abrasion}_st"):
                color_map[color][f"{abrasion}_st"] = []
            color_map[color][f"{abrasion}_st"].append(rand)
        else:
            if not color_map[color].get(abrasion):
                color_map[color][f"{abrasion}"] = []
            color_map[color][f"{abrasion}"].append(rand)
    skin_list = []
    for color in color_map:
        for abrasion in color_map[color]:
            rand_list = color_map[color][abrasion]
            is_stattrak = "_st" in abrasion
            abrasion = abrasion.replace("_st", "")
            skin_list_ = await BuffSkin.random_skin(
                len(rand_list), color, abrasion, is_stattrak, case_name
            )
            skin_list += [(skin, rand) for skin, rand in zip(skin_list_, rand_list)]
    return skin_list


# M249（StatTrak™） | 等高线
