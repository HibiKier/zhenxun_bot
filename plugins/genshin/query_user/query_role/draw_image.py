from configs.path_config import IMAGE_PATH, TEMP_PATH
from utils.image_utils import BuildImage
from typing import List, Dict, Optional
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import MessageSegment
from utils.http_utils import AsyncHttpx
from utils.utils import get_user_avatar
from io import BytesIO
import random
import asyncio
import os


image_path = IMAGE_PATH / "genshin" / "genshin_card"


async def get_genshin_image(
    user_id: int,
    uid: str,
    char_data_list: List[Dict],
    role_data: Dict,
    world_data_dict: Dict,
    home_data_list: List[Dict],
    char_detailed_dict: dict = None,
    mys_data: Optional[List[Dict]] = None,
    nickname: Optional[str] = None,
) -> MessageSegment:
    """
    生成图片数据
    :param user_id：用户qq
    :param uid: 原神uid
    :param char_data_list: 角色列表
    :param role_data: 玩家数据
    :param world_data_dict: 国家数据字典
    :param home_data_list: 家园列表
    :param char_detailed_dict: 角色武器字典
    :param mys_data: 用户米游社数据
    :param nickname: 用户昵称
    """
    user_ava = BytesIO(await get_user_avatar(user_id))
    return await asyncio.get_event_loop().run_in_executor(
        None,
        _get_genshin_image,
        uid,
        char_data_list,
        role_data,
        world_data_dict,
        home_data_list,
        char_detailed_dict,
        mys_data,
        nickname,
        user_ava,
    )


def _get_genshin_image(
    uid: str,
    char_data_list: List[Dict],
    role_data: Dict,
    world_data_dict: Dict,
    home_data_list: List[Dict],
    char_detailed_dict: dict = None,
    mys_data: Optional[Dict] = None,
    nickname: Optional[str] = None,
    user_ava: Optional[BytesIO] = None,
) -> MessageSegment:
    """
    生成图片数据
    :param uid: 原神uid
    :param char_data_list: 角色列表
    :param role_data: 玩家数据
    :param world_data_dict: 国家数据字典
    :param home_data_list: 家园列表
    :param char_detailed_dict: 角色武器字典
    :param mys_data: 用户米游社数据
    :param nickname: 用户昵称
    :param user_ava：用户头像
    """
    user_image = get_user_data_image(uid, role_data, mys_data, nickname, user_ava)
    home_image = get_home_data_image(home_data_list)
    country_image = get_country_data_image(world_data_dict)
    char_image = get_char_data_image(char_data_list, char_detailed_dict)
    top_bk = BuildImage(user_image.w, user_image.h + max([home_image.h, country_image.h]) + 100, color="#F9F6F2")
    top_bk.paste(user_image, alpha=True)
    top_bk.paste(home_image, (0, user_image.h + 50), alpha=True)
    top_bk.paste(country_image, (home_image.w + 100, user_image.h + 50), alpha=True)
    bar = BuildImage(1600, 200, font_size=50, color="#F9F6F2", font="HYWenHei-85W.ttf")
    bar.text((50, 10), "角色背包", (104, 103, 101))
    bar.line((50, 90, 1550, 90), (227, 219, 209), width=10)

    foot = BuildImage(1700, 87, background=image_path / "head.png")
    head = BuildImage(1700, 87, background=image_path / "head.png")
    head.rotate(180)
    middle = BuildImage(
        1700, top_bk.h + bar.h + char_image.h, background=image_path / "middle.png"
    )
    A = BuildImage(middle.w, middle.h + foot.h + head.h)
    A.paste(head, (-5, 0), True)
    A.paste(middle, (0, head.h), True)
    A.paste(foot, (0, head.h + middle.h), True)
    A.crop((0, 0, A.w - 5, A.h))
    if A.h - top_bk.h - bar.h - char_image.h > 200:
        _h = A.h - top_bk.h - bar.h - char_image.h - 200
        A.crop((0, 0, A.w, A.h - _h))
        A.paste(foot, (0, A.h - 87))
    A.paste(top_bk, (0, 100), center_type="by_width")
    A.paste(bar, (50, top_bk.h + 80))
    A.paste(char_image, (0, top_bk.h + bar.h + 10), center_type="by_width")
    rand = random.randint(1, 10000)
    A.resize(0.8)
    A.save(TEMP_PATH / f"genshin_user_card_{rand}.png")
    return image(TEMP_PATH / f"genshin_user_card_{rand}.png")


def get_user_data_image(
    uid: str,
    role_data: Dict,
    mys_data: Optional[Dict] = None,
    nickname: Optional[str] = None,
    user_ava: Optional[BytesIO] = None,
) -> BuildImage:
    """
    画出玩家基本数据
    :param uid: 原神uid
    :param role_data: 玩家数据
    :param mys_data: 玩家米游社数据
    :param nickname: 用户昵称
    :param user_ava：用户头像
    """
    if mys_data:
        nickname = [x["nickname"] for x in mys_data if x["game_id"] == 2][0]
    region = BuildImage(1440, 450, color="#E3DBD1", font="HYWenHei-85W.ttf")
    region.circle_corner(30)
    uname_img = BuildImage(
        0,
        0,
        plain_text=nickname,
        font_size=40,
        color=(255, 255, 255, 0),
        font="HYWenHei-85W.ttf",
    )
    uid_img = BuildImage(
        0,
        0,
        plain_text=f"UID: {uid}",
        font_size=25,
        color=(255, 255, 255, 0),
        font="HYWenHei-85W.ttf",
        font_color=(21, 167, 89),
    )
    ava_bk = BuildImage(270, 270, background=image_path / "cover.png")
    # 用户头像
    if user_ava:
        ava_img = BuildImage(200, 200, background=user_ava)
        ava_img.circle()
        ava_bk.paste(ava_img, alpha=True, center_type="center")
    else:
        ava_img = BuildImage(
            245,
            245,
            background=image_path
            / "chars_ava"
            / random.choice(os.listdir(image_path / "chars_ava")),
        )
        ava_bk.paste(ava_img, (12, 16), alpha=True)
    region.paste(uname_img, (int(170 + uid_img.w / 2 - uname_img.w / 2), 305), True)
    region.paste(uid_img, (170, 355), True)
    region.paste(ava_bk, (int(550 / 2 - ava_bk.w / 2), 40), True)
    data_img = BuildImage(
        800, 400, color="#E3DBD1", font="HYWenHei-85W.ttf", font_size=40
    )
    _height = 0
    keys = [
        ["活跃天数", "成就达成", "获得角色", "深境螺旋"],
        ["华丽宝箱", "珍贵宝箱", "精致宝箱", "普通宝箱"],
        ["奇馈宝箱", "风神瞳", "岩神瞳", "雷神瞳"],
    ]
    values = [
        [
            role_data["active_day_number"],
            role_data["achievement_number"],
            role_data["avatar_number"],
            role_data["spiral_abyss"],
        ],
        [
            role_data["luxurious_chest_number"],
            role_data["precious_chest_number"],
            role_data["exquisite_chest_number"],
            role_data["common_chest_number"],
        ],
        [
            role_data["magic_chest_number"],
            role_data["anemoculus_number"],
            role_data["geoculus_number"],
            role_data["electroculus_number"],
        ],
    ]
    for key, value in zip(keys, values):
        _tmp_data_img = BuildImage(
            800, 200, color="#E3DBD1", font="HYWenHei-85W.ttf", font_size=40
        )
        _width = 10
        for k, v in zip(key, value):
            t_ = BuildImage(
                0,
                0,
                plain_text=k,
                color=(255, 255, 255, 0),
                font_color=(138, 143, 143),
                font="HYWenHei-85W.ttf",
                font_size=30,
            )
            tmp_ = BuildImage(
                t_.w, t_.h + 70, color="#E3DBD1", font="HYWenHei-85W.ttf", font_size=40
            )
            tmp_.text((0, 0), str(v), center_type="by_width")
            tmp_.paste(t_, (0, 50), True, "by_width")
            _tmp_data_img.paste(tmp_, (_width if len(key) > 3 else _width + 15, 0))
            _width += 200
        data_img.paste(_tmp_data_img, (0, _height))
        _height += _tmp_data_img.h - 70
    region.paste(data_img, (510, 50))
    return region


def get_home_data_image(home_data_list: List[Dict]) -> BuildImage:
    """
    画出家园数据
    :param home_data_list: 家园列表
    """
    h = 130 + 300 * 4
    region = BuildImage(
        550, h, color="#E3DBD1", font="HYWenHei-85W.ttf", font_size=40
    )
    try:
        region.text(
            (0, 30), f'尘歌壶 Lv.{home_data_list[0]["level"]}', center_type="by_width"
        )
        region.text(
            (0, region.h - 70), f'仙力: {home_data_list[0]["comfort_num"]}', center_type="by_width"
        )
    except (IndexError, KeyError):
        region.text((0, 30), f"尘歌壶 Lv.0", center_type="by_width")
        region.text((0, region.h - 70), f"仙力: 0", center_type="by_width")
    region.circle_corner(30)
    height = 100
    homes = os.listdir(image_path / "homes")
    homes.remove("lock.png")
    homes.sort()
    unlock_home = [x["name"] for x in home_data_list]
    for i, file in enumerate(homes):
        home_img = image_path / "homes" / file
        x = BuildImage(500, 250, background=home_img)
        if file.split(".")[0] not in unlock_home:
            black_img = BuildImage(500, 250, color="black")
            lock_img = BuildImage(0, 0, background=image_path / "homes" / "lock.png")
            black_img.circle_corner(50)
            black_img.transparent(1)
            black_img.paste(lock_img, alpha=True, center_type="center")
            x.paste(black_img, alpha=True)
        else:
            black_img = BuildImage(
                500, 150, color="black", font="HYWenHei-85W.ttf", font_size=40
            )
            black_img.text((55, 55), file.split(".")[0], fill=(226, 211, 146))
            black_img.transparent(1)
            text_img = BuildImage(
                0,
                0,
                plain_text="洞天等级",
                font="HYWenHei-85W.ttf",
                font_color=(203, 200, 184),
                font_size=35,
                color=(255, 255, 255, 0),
            )
            level_img = BuildImage(
                0,
                0,
                plain_text=f'{home_data_list[0]["comfort_level_name"]}',
                font="HYWenHei-85W.ttf",
                font_color=(211, 213, 207),
                font_size=30,
                color=(255, 255, 255, 0),
            )
            black_img.paste(text_img, (270, 25), True)
            black_img.paste(level_img, (278, 85), True)
            x.paste(black_img, alpha=True, center_type="center")
        x.circle_corner(50)
        region.paste(x, (0, height), True, "by_width")
        height += 300
    return region


def get_country_data_image(world_data_dict: Dict) -> BuildImage:
    """
    画出国家探索供奉等图像
    :param world_data_dict: 国家数据字典
    """
    # 层岩巨渊 和 地下矿区 算一个
    region = BuildImage(790, 267 * (len(world_data_dict) - 1), color="#F9F6F2")
    height = 0
    for country in ["蒙德", "龙脊雪山", "璃月", "层岩巨渊", "稻妻", "渊下宫"]:
        if not world_data_dict.get(country):
            continue
        x = BuildImage(790, 250, color="#3A4467")
        logo = BuildImage(180, 180, background=image_path / "logo" / f"{country}.png")
        tmp_bk = BuildImage(770, 230, color="#606779")
        tmp_bk.circle_corner(10)
        content_bk = BuildImage(
            755, 215, color="#3A4467", font_size=40, font="HYWenHei-85W.ttf"
        )
        content_bk.paste(logo, (50, 0), True, "by_height")
        if country in ["蒙德", "璃月"]:
            content_bk.text((300, 40), "探索", fill=(239, 211, 114))
            content_bk.text(
                (450, 40),
                f"{world_data_dict[country]['exploration_percentage'] / 10}%",
                fill=(255, 255, 255),
            )
            content_bk.text((300, 120), "声望", fill=(239, 211, 114))
            content_bk.text(
                (450, 120),
                f"Lv.{world_data_dict[country]['level']}",
                fill=(255, 255, 255),
            )
        elif country in ["层岩巨渊"]:
            content_bk.text((300, 20), "层岩巨渊探索", fill=(239, 211, 114))
            content_bk.text(
                (570, 20),
                f"{world_data_dict['层岩巨渊']['exploration_percentage'] / 10}%",
                fill=(255, 255, 255),
            )
            content_bk.text((300, 85), "地下矿区探索", fill=(239, 211, 114))
            content_bk.text(
                (570, 85),
                f"{world_data_dict['层岩巨渊·地下矿区']['exploration_percentage'] / 10}%",
                fill=(255, 255, 255),
            )
            content_bk.text((300, 150), "流明石触媒", fill=(239, 211, 114))
            content_bk.text(
                (570, 150),
                f"LV.{world_data_dict['层岩巨渊·地下矿区']['offerings'][0]['level']}",
                fill=(255, 255, 255),
            )
        elif country in ["龙脊雪山"]:
            content_bk.text((300, 40), "探索", fill=(239, 211, 114))
            content_bk.text(
                (450, 40),
                f"{world_data_dict[country]['exploration_percentage'] / 10}%",
                fill=(255, 255, 255),
            )
            content_bk.text((300, 120), "供奉", fill=(239, 211, 114))
            content_bk.text(
                (450, 120),
                f"Lv.{world_data_dict[country]['offerings'][0]['level']}",
                fill=(255, 255, 255),
            )
        elif country in ["稻妻"]:
            content_bk.text((300, 20), "探索", fill=(239, 211, 114))
            content_bk.text(
                (450, 20),
                f"{world_data_dict[country]['exploration_percentage'] / 10}%",
                fill=(255, 255, 255),
            )
            content_bk.text((300, 85), "声望", fill=(239, 211, 114))
            content_bk.text(
                (450, 85),
                f"Lv.{world_data_dict[country]['level']}",
                fill=(255, 255, 255),
            )
            content_bk.text((300, 150), "神樱", fill=(239, 211, 114))
            content_bk.text(
                (450, 150),
                f"Lv.{world_data_dict[country]['offerings'][0]['level']}",
                fill=(255, 255, 255),
            )
        elif country in ["渊下宫"]:
            content_bk.text((300, 0), "探索", fill=(239, 211, 114), center_type="by_height")
            content_bk.text(
                (450, 20),
                f"{world_data_dict[country]['exploration_percentage'] / 10}%",
                fill=(255, 255, 255),
                center_type="by_height",
            )
        x.paste(tmp_bk, alpha=True, center_type="center")
        x.paste(content_bk, alpha=True, center_type="center")
        x.circle_corner(20)
        region.paste(x, (0, height), center_type="by_width")
        height += 267
    return region


def get_char_data_image(
    char_data_list: List[Dict], char_detailed_dict: dict
) -> "BuildImage, int":
    """
    画出角色列表
    :param char_data_list: 角色列表
    :param char_detailed_dict: 角色武器
    """
    lens = len(char_data_list) / 7 if len(char_data_list) % 7 == 0 else len(char_data_list) / 7 + 1
    x = 500
    _h = int(x * lens)
    region = BuildImage(
        1600,
        _h,
        color="#F9F6F2",
    )
    width = 120
    height = 0
    idx = 0
    for char in char_data_list:
        if width + 230 > 1550:
            width = 120
            height += 420
        idx += 1
        char_img = image_path / "chars" / f'{char["name"]}.png'
        char_bk = BuildImage(
            270,
            500,
            background=image_path / "element.png",
            font="HYWenHei-85W.ttf",
            font_size=35,
        )
        char_img = BuildImage(0, 0, background=char_img)
        actived_constellation_num = BuildImage(
            0,
            0,
            plain_text=f"命之座: {char['actived_constellation_num']}层",
            font="HYWenHei-85W.ttf",
            font_size=25,
            color=(255, 255, 255, 0),
        )
        level = BuildImage(
            0,
            0,
            plain_text=f"Lv.{char['level']}",
            font="HYWenHei-85W.ttf",
            font_size=30,
            color=(255, 255, 255, 0),
            font_color=(21, 167, 89),
        )
        love_log = BuildImage(
            0,
            0,
            plain_text="♥",
            font="HWZhongSong.ttf",
            font_size=40,
            color=(255, 255, 255, 0),
            font_color=(232, 31, 168),
        )
        fetter = BuildImage(
            0,
            0,
            plain_text=f'{char["fetter"]}',
            font="HYWenHei-85W.ttf",
            font_size=30,
            color=(255, 255, 255, 0),
            font_color=(232, 31, 168),
        )
        if char_detailed_dict.get(char["name"]):
            weapon = BuildImage(
                100,
                100,
                background=image_path
                / "weapons"
                / f'{char_detailed_dict[char["name"]]["weapon"]}.png',
            )
            weapon_name = BuildImage(
                0,
                0,
                plain_text=f"{char_detailed_dict[char['name']]['weapon']}",
                font="HYWenHei-85W.ttf",
                font_size=25,
                color=(255, 255, 255, 0),
            )
            weapon_affix_level = BuildImage(
                0,
                0,
                plain_text=f"精炼: {char_detailed_dict[char['name']]['affix_level']}",
                font="HYWenHei-85W.ttf",
                font_size=20,
                color=(255, 255, 255, 0),
            )
            weapon_level = BuildImage(
                0,
                0,
                plain_text=f"Lv.{char_detailed_dict[char['name']]['level']}",
                font="HYWenHei-85W.ttf",
                font_size=25,
                color=(255, 255, 255, 0),
                font_color=(21, 167, 89),
            )
            char_bk.paste(weapon, (20, 380), True)
            char_bk.paste(
                weapon_name,
                (100 + int((char_bk.w - 22 - weapon.w - weapon_name.w) / 2 - 10), 390),
                True,
            )
            char_bk.paste(
                weapon_affix_level,
                (
                    (
                        100
                        + int(
                            (char_bk.w - 10 - weapon.w - weapon_affix_level.w) / 2 - 10
                        ),
                        420,
                    )
                ),
                True,
            )
            char_bk.paste(
                weapon_level,
                (
                    (
                        100
                        + int((char_bk.w - 10 - weapon.w - weapon_level.w) / 2 - 10),
                        450,
                    )
                ),
                True,
            )
        char_bk.paste(char_img, (0, 5), alpha=True, center_type="by_width")
        char_bk.text((0, 270), char["name"], center_type="by_width")
        char_bk.paste(actived_constellation_num, (0, 310), True, "by_width")
        char_bk.paste(level, (60, 340), True)
        char_bk.paste(love_log, (155, 330), True)
        char_bk.paste(fetter, (180, 340), True)
        char_bk.resize(0.8)
        region.paste(char_bk, (width, height), True)
        width += 230
    region.crop((0, 0, region.w, height + 430))
    return region


async def init_image(world_data_dict: Dict[str, Dict[str, str]], char_data_list: List[Dict[str, str]], char_detailed_dict: dict, home_data_list: List[Dict]):
    """
    下载头像
    :param world_data_dict: 地图标志
    :param char_data_list: 角色列表
    :param char_detailed_dict: 角色武器
    :param home_data_list: 家园列表
    """
    for world in world_data_dict:
        file = image_path / "logo" / f'{world_data_dict[world]["name"]}.png'
        file.parent.mkdir(parents=True, exist_ok=True)
        if not file.exists():
            await AsyncHttpx.download_file(world_data_dict[world]["icon"], file)
    for char in char_data_list:
        file = image_path / "chars" / f'{char["name"]}.png'
        file.parent.mkdir(parents=True, exist_ok=True)
        if not file.exists():
            await AsyncHttpx.download_file(char["image"], file)
    for char in char_detailed_dict.keys():
        file = image_path / "weapons" / f'{char_detailed_dict[char]["weapon"]}.png'
        file.parent.mkdir(parents=True, exist_ok=True)
        if not file.exists():
            await AsyncHttpx.download_file(
                char_detailed_dict[char]["weapon_image"], file
            )
    for home in home_data_list:
        file = image_path / "homes" / f'{home["name"]}.png'
        file.parent.mkdir(parents=True, exist_ok=True)
        if not file.exists():
            await AsyncHttpx.download_file(
                home["icon"], file
            )
