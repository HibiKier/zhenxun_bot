import platform
from asyncio.exceptions import TimeoutError
from utils.utils import cn2py
from utils.http_utils import AsyncHttpx
from typing import List, Tuple, Union, Set
from .config import draw_config, DRAW_IMAGE_PATH
import nonebot
from PIL import UnidentifiedImageError
from utils.image_utils import BuildImage
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
import random
from dataclasses import dataclass
import os
import asyncio


driver = nonebot.get_driver()


loop = asyncio.get_event_loop()


@dataclass
class BaseData:
    name: str
    star: int
    limited: bool  # 限定


@dataclass
class UpEvent:
    star: int  # 对应up星级
    operators: List[BaseData]  # 干员列表
    zoom: float  # up提升倍率


async def download_img(url: str, path: str, name: str) -> bool:
    path = path.split("_")[0]
    codename = cn2py(name)
    img_path = DRAW_IMAGE_PATH / f"{path}" / f"{codename}.png"
    if not img_path.exists():
        try:
            if await AsyncHttpx.download_file(url, img_path):
                logger.info(
                    f"下载 {draw_config.path_dict[path]} 图片成功，名称：{name}，url：{url}"
                )
                return True
        except TimeoutError:
            logger.warning(f"下载 {draw_config.path_dict[path]} 图片超时，名称：{name}，url：{url}")
        # logger.info(f'{path_dict[path]} 图片 {name} 已存在')
    return False


@driver.on_startup
def _check_dir():
    for dir_name in draw_config.path_dict.keys():
        dir_path = DRAW_IMAGE_PATH / f"{dir_name}"
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)


async def generate_img(
    card_set: Union[Set[BaseData], List[BaseData]], game_name: str, star_list: list
) -> str:
    # try:
    img_list = []
    background_list = []
    for x in card_set:
        if game_name == "prts":
            if x.star == 6:
                background_list.append("#FFD700")
            elif x.star == 5:
                background_list.append("#DAA520")
            elif x.star == 4:
                background_list.append("#9370D8")
            else:
                background_list.append("white")
        img_path = DRAW_IMAGE_PATH / f"{game_name}" / f"{x.star}_star.png"
        if game_name == "azur":
            if img_path.exists():
                background_list.append(str(img_path))
        py_name = cn2py(x.name)
        img_list.append(str(DRAW_IMAGE_PATH / f"{game_name}" / f"{py_name}.png"))
    img_len = len(img_list)
    w = 100 * 10
    if img_len <= 10:
        w = 100 * img_len
        h = 100
    elif img_len % 10 == 0:
        h = 100 * int(img_len / 10)
    else:
        h = 100 * int(img_len / 10) + 100
    card_img = await asyncio.get_event_loop().run_in_executor(
        None, _pst, h, img_list, game_name, background_list
    )
    num = 0
    for n in star_list:
        num += n
    A = BuildImage(w, h)
    A.paste(card_img)
    return A.pic2bs4()


def _pst(h: int, img_list: list, game_name: str, background_list: list):
    card_img = BuildImage(100 * 10, h, 100, 100)
    idx = 0
    for img in img_list:
        try:
            if game_name == "prts":
                bk = BuildImage(100, 100, color=background_list[idx])
                b = BuildImage(94, 94, background=img)
                bk.paste(b, (3, 3))
                b = bk
            elif game_name == "azur" and background_list:
                bk = BuildImage(100, 100, background=background_list[idx])
                b = BuildImage(98, 90, background=img)
                bk.paste(b, (1, 5))
                b = bk
            else:
                try:
                    b = BuildImage(100, 100, background=img)
                except UnidentifiedImageError as e:
                    logger.warning(f"无法识别图片 已删除图片，下次更新重新下载... e：{e}")
                    if os.path.exists(img):
                        os.remove(img)
                    b = BuildImage(100, 100, color="black")
        except FileNotFoundError:
            logger.warning(f"{img} not exists")
            b = BuildImage(100, 100, color="black")
        card_img.paste(b)
        idx += 1
    return card_img


# 初始化输出数据
def init_star_rst(
    star_list: list,
    cnlist: list,
    max_star_list: list,
    max_star_index_list: list,
    up_list: list = None,
) -> str:
    if not up_list:
        up_list = []
    rst = ""
    for i in range(len(star_list)):
        if star_list[i]:
            rst += f"[{cnlist[i]}×{star_list[i]}] "
    rst += "\n"
    for i in range(len(max_star_list)):
        if max_star_list[i] in up_list:
            rst += f"第 {max_star_index_list[i]+1} 抽获取UP {max_star_list[i]}\n"
        else:
            rst += f"第 {max_star_index_list[i]+1} 抽获取 {max_star_list[i]}\n"
    return rst


# 更好的初始化
def init_rst(
    max_star_char_dict: dict,
    star_num_list: List[int],
    star: List[str],
    up_list: list = None,
):
    # print(max_star_char_dict)
    # print(star_num_list)
    # print(up_list)
    up_list = up_list if up_list else []
    rst = ""
    for i in range(len(star_num_list)):
        if star_num_list[i]:
            rst += f"[{star[i]}×{star_num_list[i]}] "
    rst += "\n"
    _tmp = []
    for name in max_star_char_dict.keys():
        _tmp += max_star_char_dict[name]
    for index in sorted(_tmp):
        for name in max_star_char_dict.keys():
            if index in max_star_char_dict[name]:
                if name in up_list:
                    rst += f"第 {index} 抽获取UP {name}\n"
                else:
                    rst += f"第 {index} 抽获取 {name}\n"
    return rst[:-1] if rst else ""


def max_card(_dict: dict):
    _max_value = max(_dict.values())
    _max_user = list(_dict.keys())[list(_dict.values()).index(_max_value)]
    return f"抽取到最多的是{_max_user}，共抽取了{_max_value}次"
    # ThreeHighest = nlargest(3, operator_dict, key=operator_dict.get)
    # rst = '最喜欢你的前三位是干员是：\n'
    # for name in ThreeHighest:
    #     rst += f'{name} 共投了 {operator_dict[name]} 份简历\n'
    # return rst[:-1]


# 获取up和概率
async def init_up_char(announcement):
    UP_CHAR = []
    UP_ARMS = []
    tmp = ""
    up_char_dict = await announcement.update_up_char()
    for x in list(up_char_dict.keys()):
        tmp += up_char_dict[x]["title"] + "[\n]"
    tmp = tmp.split("[\n]")
    _CURRENT_CHAR_POOL_TITLE = tmp[0]
    if len(up_char_dict) > 1:
        _CURRENT_ARMS_POOL_TITLE = tmp[1]
    else:
        _CURRENT_ARMS_POOL_TITLE = ""
    POOL_IMG = ""
    x = [x for x in list(up_char_dict.keys())]
    if _CURRENT_CHAR_POOL_TITLE:
        POOL_IMG += MessageSegment.image(up_char_dict[x[0]]["pool_img"])
    try:
        if _CURRENT_ARMS_POOL_TITLE:
            POOL_IMG += MessageSegment.image(up_char_dict[x[1]]["pool_img"])
    except (IndexError, KeyError):
        pass
    logger.info(
        f"成功获取{announcement.game_name}当前up信息...当前up池: {_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_ARMS_POOL_TITLE}"
    )
    for key in up_char_dict.keys():
        for star in up_char_dict[key]["up_char"].keys():
            up_char_lst = []
            for char in up_char_dict[key]["up_char"][star].keys():
                up_char_lst.append(char)
            if up_char_lst:
                if key == "char":
                    UP_CHAR.append(
                        UpEvent(star=int(star), operators=up_char_lst, zoom=0)
                    )
                else:
                    UP_ARMS.append(
                        UpEvent(star=int(star), operators=up_char_lst, zoom=0)
                    )
    return (
        _CURRENT_CHAR_POOL_TITLE,
        _CURRENT_ARMS_POOL_TITLE,
        POOL_IMG,
        UP_CHAR,
        UP_ARMS,
    )


def is_number(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def set_list(lst: List[BaseData]) -> list:
    tmp = []
    name_lst = []
    for x in lst:
        if x.name not in name_lst:
            tmp.append(x)
            name_lst.append(x.name)
    return tmp


# 获取星级
def get_star(star_lst: List[int], probability_lst: List[float]) -> int:
    rand = random.random()
    add = 0
    tmp_lst = [(0, probability_lst[0])]
    for i in range(1, len(probability_lst) - 1):
        add += probability_lst[i - 1]
        tmp_lst.append((tmp_lst[i - 1][1], probability_lst[i] + add))
    tmp_lst.append((tmp_lst[-1][1], 1))
    for i in range(len(tmp_lst)):
        if tmp_lst[i][0] <= rand <= tmp_lst[i][1]:
            return star_lst[i]


# 整理数据
def format_card_information(
    count: int, star_list: List[int], func, pool_name: str = "", guaranteed: bool = True
):
    max_star_lst = []  # 获取的最高星级角色列表
    max_index_lst = []  # 获取最高星级角色的次数
    obj_list = []  # 获取所有角色
    obj_dict = {}  # 获取角色次数字典
    _count = -1
    if guaranteed:
        _count = 0
    for i in range(count):
        if guaranteed:
            _count += 1
        if pool_name:
            if _count == 10:
                obj, code = func(pool_name, 2)
                _count = 0
            else:
                obj, code = func(pool_name)
        else:
            if _count == 10:
                obj, code = func(mode=2)
                _count = 0
            else:
                obj, code = func()
        star_list[code] += 1
        if code == 0:
            max_star_lst.append(obj.name)
            max_index_lst.append(i)
            if guaranteed:
                _count = 0
        if code == 1:
            if guaranteed:
                _count = 0
        try:
            obj_dict[obj.name] += 1
        except KeyError:
            obj_dict[obj.name] = 1
        obj_list.append(obj)
    return obj_list, obj_dict, max_star_lst, star_list, max_index_lst


# 检测次数是否合法
def check_num(num: str, max_num: int) -> Tuple[str, bool]:
    if is_number(num):
        try:
            num = int(num)
        except ValueError:
            return "必！须！是！数！字！", False
    if num > max_num:
        return "一井都满不足不了你嘛！快爬开！", False
    if num < 1:
        return "虚空抽卡？？？", False
    else:
        return str(num), True


# 移除windows和linux下特殊字符
def remove_prohibited_str(name: str) -> str:
    if platform.system().lower() == "windows":
        tmp = ""
        for i in name:
            if i not in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
                tmp += i
        name = tmp
    else:
        name = name.replace("/", "\\")
    return name
