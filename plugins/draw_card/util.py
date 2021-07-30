
import aiohttp
import aiofiles
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import InvalidURL
from nonebot.adapters.cqhttp import MessageSegment
from typing import List, Union, Set
from pathlib import Path
from .config import path_dict
from configs.path_config import IMAGE_PATH
import nonebot
import pypinyin
from utils.image_utils import CreateImg
import platform
from services.log import logger
import random
from dataclasses import dataclass
import os
import asyncio
from PIL import UnidentifiedImageError
try:
    import ujson as json
except ModuleNotFoundError:
    import json


driver: nonebot.Driver = nonebot.get_driver()


loop = asyncio.get_event_loop()


headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}


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
    path = path.split('_')[0]
    codename = cn2py(name)
    file = Path(IMAGE_PATH + f'/draw_card/{path}/{codename}.png')
    if not file.exists():
        file.parent.mkdir(exist_ok=True, parents=True)
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, timeout=7) as response:
                    async with aiofiles.open(IMAGE_PATH + f'/draw_card/{path}/{codename}.png', 'wb') as f:
                        await f.write(await response.read())
                        logger.info(f'下载 {path_dict[path]} 图片成功，名称：{name}，url：{url}')
                        return True
        except TimeoutError:
            logger.warning(f'下载 {path_dict[path]} 图片超时，名称：{name}，url：{url}')
            return False
        except InvalidURL:
            logger.warning(f'下载 {path_dict[path]} 链接错误，名称：{name}，url：{url}')
            return False
    else:
        # logger.info(f'{path_dict[path]} 图片 {name} 已存在')
        return False


@driver.on_startup
def _check_dir():
    for dir_name in path_dict.keys():
        _p = Path(IMAGE_PATH + f'/draw_card/' + dir_name)
        if not _p.exists():
            _p.mkdir(parents=True, exist_ok=True)


async def generate_img(card_set: Union[Set[BaseData], List[BaseData]], game_name: str, star_list: list) -> str:
    # try:
    img_list = []
    background_list = []
    for x in card_set:
        if game_name == 'prts':
            if x.star == 6:
                background_list.append('#FFD700')
            elif x.star == 5:
                background_list.append('#DAA520')
            elif x.star == 4:
                background_list.append('#9370D8')
            else:
                background_list.append('white')
        if game_name == 'azur':
            if os.path.exists(IMAGE_PATH + f'/draw_card/{game_name}/{x.star}_star.png'):
                background_list.append(IMAGE_PATH + f'/draw_card/{game_name}/{x.star}_star.png')
        pyname = cn2py(x.name)
        img_list.append(IMAGE_PATH + f'/draw_card/{game_name}/{pyname}.png')
    img_len = len(img_list)
    w = 100 * 10
    if img_len <= 10:
        w = 100 * img_len
        h = 100
    elif img_len % 10 == 0:
        h = 100 * int(img_len / 10)
    else:
        h = 100 * int(img_len / 10) + 100
    card_img = await asyncio.get_event_loop().run_in_executor(None, _pst, h, img_list, game_name, background_list)
    num = 0
    for n in star_list:
        num += n
    A = CreateImg(w, h)
    A.paste(card_img)
    return A.pic2bs4()


def _pst(h: int, img_list: list, game_name: str, background_list: list):
    card_img = CreateImg(100 * 10, h, 100, 100)
    idx = 0
    for img in img_list:
        try:
            if game_name == 'prts':
                bk = CreateImg(100, 100, color=background_list[idx])
                b = CreateImg(94, 94, background=img)
                bk.paste(b, (3, 3))
                b = bk
            elif game_name == 'azur' and background_list:
                bk = CreateImg(100, 100, background=background_list[idx])
                b = CreateImg(98, 90, background=img)
                bk.paste(b, (1, 5))
                b = bk
            else:
                try:
                    b = CreateImg(100, 100, background=img)
                except UnidentifiedImageError as e:
                    logger.warning(f'无法识别图片 已删除图片，下次更新重新下载... e：{e}')
                    if os.path.exists(img):
                        os.remove(img)
                    b = CreateImg(100, 100, color='black')
        except FileNotFoundError:
            logger.warning(f'{img} not exists')
            b = CreateImg(100, 100, color='black')
        card_img.paste(b)
        idx += 1
    return card_img


def init_star_rst(star_list: list, cnlist: list, max_star_list: list, max_star_index_list: list, up_list: list = None) -> str:
    if not up_list:
        up_list = []
    rst = ''
    for i in range(len(star_list)):
        if star_list[i]:
            rst += f'[{cnlist[i]}×{star_list[i]}] '
    rst += '\n'
    for i in range(len(max_star_list)):
        if max_star_list[i] in up_list:
            rst += f'第 {max_star_index_list[i]+1} 抽获取UP {max_star_list[i]}\n'
        else:
            rst += f'第 {max_star_index_list[i]+1} 抽获取 {max_star_list[i]}\n'
    return rst


def max_card(_dict: dict):
    _max_value = max(_dict.values())
    _max_user = list(_dict.keys())[list(_dict.values()).index(_max_value)]
    return f'抽取到最多的是{_max_user}，共抽取了{_max_value}次'
    # ThreeHighest = nlargest(3, operator_dict, key=operator_dict.get)
    # rst = '最喜欢你的前三位是干员是：\n'
    # for name in ThreeHighest:
    #     rst += f'{name} 共投了 {operator_dict[name]} 份简历\n'
    # return rst[:-1]


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


def cn2py(word) -> str:
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        temp += ''.join(i)
    return temp


def set_list(lst: List[BaseData]) -> list:
    tmp = []
    name_lst = []
    for x in lst:
        if x.name not in name_lst:
            tmp.append(x)
            name_lst.append(x.name)
    return tmp


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


# 获取up和概率
async def init_up_char(announcement):
    UP_CHAR = []
    UP_ARMS = []
    tmp = ''
    up_char_dict = await announcement.update_up_char()
    for x in list(up_char_dict.keys()):
        tmp += up_char_dict[x]['title'] + '[\n]'
    tmp = tmp.split('[\n]')
    _CURRENT_CHAR_POOL_TITLE = tmp[0]
    if len(up_char_dict) > 1:
        _CURRENT_ARMS_POOL_TITLE = tmp[1]
    else:
        _CURRENT_ARMS_POOL_TITLE = ''
    POOL_IMG = ''
    x = [x for x in list(up_char_dict.keys())]
    if _CURRENT_CHAR_POOL_TITLE:
        POOL_IMG += MessageSegment.image(up_char_dict[x[0]]['pool_img'])
    try:
        if _CURRENT_ARMS_POOL_TITLE:
            POOL_IMG += MessageSegment.image(up_char_dict[x[1]]['pool_img'])
    except (IndexError, KeyError):
        pass
    logger.info(f'成功获取{announcement.game_name}当前up信息...当前up池: {_CURRENT_CHAR_POOL_TITLE} & {_CURRENT_ARMS_POOL_TITLE}')
    for key in up_char_dict.keys():
        for star in up_char_dict[key]['up_char'].keys():
            up_char_lst = []
            for char in up_char_dict[key]['up_char'][star].keys():
                up_char_lst.append(char)
            if up_char_lst:
                if key == 'char':
                    UP_CHAR.append(UpEvent(star=int(star), operators=up_char_lst, zoom=0))
                else:
                    UP_ARMS.append(UpEvent(star=int(star), operators=up_char_lst, zoom=0))
    return _CURRENT_CHAR_POOL_TITLE, _CURRENT_ARMS_POOL_TITLE, POOL_IMG, UP_CHAR, UP_ARMS


# 整理数据
def format_card_information(count: int, star_list: List[int], func, pool_name: str = '', guaranteed: bool = True):
    max_star_lst = []       # 获取的最高星级角色列表
    max_index_lst = []      # 获取最高星级角色的次数
    obj_list = []           # 获取所有角色
    obj_dict = {}           # 获取角色次数字典
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
def check_num(num: str, max_num: int) -> 'str, bool':
    if is_number(num):
        try:
            num = int(num)
        except ValueError:
            return '必！须！是！数！字！', False
    if num > max_num:
        return '一井都满不足不了你嘛！快爬开！', False
    if num < 1:
        return '虚空抽卡？？？', False
    else:
        return str(num), True


# 移除windows和linux下特殊字符
def remove_prohibited_str(name: str):
    if platform.system().lower() == 'windows':
        tmp = ''
        for i in name:
            if i not in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                tmp += i
        name = tmp
    else:
        name = name.replace('/', '\\')
    return name
