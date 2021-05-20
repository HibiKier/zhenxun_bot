import os
import aiohttp
import aiofiles
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import InvalidURL
from typing import List, Union, Set
import asyncio
from pathlib import Path
from .config import path_dict
import nonebot
from util.utils import cn2py
from util.img_utils import CreateImg
from util.user_agent import get_user_agent
from configs.path_config import IMAGE_PATH
from dataclasses import dataclass
from services.log import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json


driver: nonebot.Driver = nonebot.get_driver()


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
    # if not _p.exists():
    #     _p.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(IMAGE_PATH + f'/draw_card/{path}/{codename}.png'):
        try:
            async with aiohttp.ClientSession(headers=get_user_agent()) as session:
                async with session.get(url, timeout=7) as response:
                    async with aiofiles.open(IMAGE_PATH + f'/draw_card/{path}/{codename}.png', 'wb') as f:
                        await f.write(await response.read())
                        logger.info(f'下载 {path_dict[path]} 图片成功，名称：{name}，url：{url}')
                        return True
        except TimeoutError:
            logger.info(f'下载 {path_dict[path]} 图片超时，名称：{name}，url：{url}')
            return False
        except InvalidURL:
            logger.info(f'下载 {path_dict[path]} 链接错误，名称：{name}，url：{url}')
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
    color_list = []
    for x in card_set:
        if game_name == 'prts':
            if x.star == 6:
                color_list.append('#FFD700')
            elif x.star == 5:
                color_list.append('#DAA520')
            elif x.star == 4:
                color_list.append('#9370D8')
            else:
                color_list.append('white')
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
    card_img = await asyncio.get_event_loop().run_in_executor(None, _pst, h, img_list, game_name, color_list)
    num = 0
    for n in star_list:
        num += n
    A = CreateImg(w, h)
    A.paste(card_img)
    return A.pic2bs4()


def _pst(h: int, img_list: list, game_name: str, color_list: list):
    card_img = CreateImg(100 * 10, h, 100, 100)
    idx = 0
    for img in img_list:
        try:
            if game_name == 'prts':
                bk = CreateImg(100, 100, color=color_list[idx])
                b = CreateImg(94, 94, background=img)
                bk.paste(b, (3, 3))
                b = bk
                idx += 1
            else:
                b = CreateImg(100, 100, background=img)
        except FileNotFoundError:
            print(f'{img} not exists')
            b = CreateImg(100, 100, color='black')
        card_img.paste(b)
    return card_img


def init_star_rst(star_list: list, cnlist: list, max_star_list: list, max_star_olist: list, up_list: list = None) -> str:
    if not up_list:
        up_list = []
    rst = ''
    for i in range(len(star_list)):
        if star_list[i]:
            rst += f'[{cnlist[i]}×{star_list[i]}] '
    rst += '\n'
    for i in range(len(max_star_list)):
        if max_star_list[i] in up_list:
            rst += f'第 {max_star_olist[i]+1} 抽获取UP {max_star_list[i]}\n'
        else:
            rst += f'第 {max_star_olist[i]+1} 抽获取 {max_star_list[i]}\n'
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


def set_list(lst: List[BaseData]) -> list:
    tmp = []
    name_lst = []
    for x in lst:
        if x.name not in name_lst:
            tmp.append(x)
            name_lst.append(x.name)
    return tmp

