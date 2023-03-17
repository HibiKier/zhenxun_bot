import asyncio
import os
import random
import re
from asyncio.exceptions import TimeoutError
from typing import Any, List, Optional, Tuple, Union

from asyncpg.exceptions import UniqueViolationError
from nonebot.adapters.onebot.v11 import MessageSegment

from configs.config import NICKNAME, Config
from configs.path_config import IMAGE_PATH, TEMP_PATH
from services.log import logger
from utils.http_utils import AsyncHttpx
from utils.image_utils import compressed_image, get_img_hash
from utils.message_builder import image
from utils.utils import change_img_md5, change_pixiv_image_links

from .._model import Setu

url = "https://api.lolicon.app/setu/v2"
path = "_setu"
r18_path = "_r18"
host_pattern = re.compile(r"https?://([^/]+)")


# 获取url
async def get_setu_urls(
    tags: List[str], num: int = 1, r18: bool = False, command: str = ""
) -> Tuple[List[str], List[str], List[tuple], int]:
    tags = tags[:3] if len(tags) > 3 else tags
    params = {
        "r18": 1 if r18 else 0,  # 添加r18参数 0为否，1为是，2为混合
        "tag": tags,  # 若指定tag
        "num": 20,  # 一次返回的结果数量
        "size": ["original"],
    }
    for count in range(3):
        logger.debug(f"尝试获取图片URL第 {count+1} 次", "色图")
        try:
            response = await AsyncHttpx.get(
                url, timeout=Config.get_config("send_setu", "TIMEOUT"), params=params
            )
            if response.status_code == 200:
                data = response.json()
                if not data["error"]:
                    data = data["data"]
                    (
                        urls,
                        text_list,
                        add_databases_list,
                    ) = await asyncio.get_event_loop().run_in_executor(
                        None, _setu_data_process, data, command
                    )
                    num = num if num < len(data) else len(data)
                    random_idx = random.sample(range(len(data)), num)
                    x_urls = []
                    x_text_lst = []
                    for x in random_idx:
                        x_urls.append(urls[x])
                        x_text_lst.append(text_list[x])
                    if not x_urls:
                        return ["没找到符合条件的色图..."], [], [], 401
                    return x_urls, x_text_lst, add_databases_list, 200
                else:
                    return ["没找到符合条件的色图..."], [], [], 401
        except TimeoutError as e:
            logger.error(f"获取图片URL超时", "色图", e=e)
        except Exception as e:
            logger.error(f"访问页面错误", "色图", e=e)
    return ["我网线被人拔了..QAQ"], [], [], 999


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}


async def search_online_setu(
    url_: str, id_: Optional[int] = None, path_: Optional[str] = None
) -> Tuple[Union[MessageSegment, str], int]:
    """
    下载色图
    :param url_: 色图url
    :param id_: 本地id
    :param path_: 存储路径
    """
    url_ = change_pixiv_image_links(url_)
    index = random.randint(1, 100000) if id_ is None else id_
    base_path = IMAGE_PATH / path_ if path_ else TEMP_PATH
    file_name = f"{index}_temp_setu.jpg" if path_ == TEMP_PATH else f"{index}.jpg"
    file = base_path / file_name
    base_path.mkdir(parents=True, exist_ok=True)
    for i in range(3):
        logger.debug(f"尝试在线搜索第 {i+1} 次", "色图")
        try:
            if not await AsyncHttpx.download_file(
                url_,
                file,
                timeout=Config.get_config("send_setu", "TIMEOUT"),
            ):
                continue
            if id_ is not None:
                if os.path.getsize(base_path / f"{index}.jpg") > 1024 * 1024 * 1.5:
                    compressed_image(
                        base_path / f"{index}.jpg",
                    )
            logger.info(f"下载 lolicon 图片 {url_} 成功， id：{index}")
            change_img_md5(file)
            return image(file), index
        except TimeoutError as e:
            logger.error(f"下载图片超时", "色图", e=e)
        except Exception as e:
            logger.error(f"下载图片错误", "色图", e=e)
    return "图片被小怪兽恰掉啦..!QAQ", -1


# 检测本地是否有id涩图，无的话则下载
async def check_local_exists_or_download(
    setu_image: Setu,
) -> Tuple[Union[MessageSegment, str], int]:
    path_ = None
    id_ = None
    if Config.get_config("send_setu", "DOWNLOAD_SETU"):
        id_ = setu_image.local_id
        path_ = r18_path if setu_image.is_r18 else path
        file = IMAGE_PATH / path_ / f"{setu_image.local_id}.jpg"
        if file.exists():
            change_img_md5(file)
            return image(file), 200
    return await search_online_setu(setu_image.img_url, id_, path_)


# 添加涩图数据到数据库
async def add_data_to_database(lst: List[tuple]):
    tmp = []
    for x in lst:
        if x not in tmp:
            tmp.append(x)
    if tmp:
        for x in tmp:
            try:
                idx = await Setu.filter(is_r18="R-18" in x[5]).count()
                if not await Setu.exists(pid=x[2], img_url=x[4]):
                    await Setu.create(
                        local_id=idx,
                        title=x[0],
                        author=x[1],
                        pid=x[2],
                        img_hash=x[3],
                        img_url=x[4],
                        tags=x[5],
                        is_r18="R-18" in x[5],
                    )
            except UniqueViolationError:
                pass


# 拿到本地色图列表
async def get_setu_list(
    index: Optional[int] = None, tags: Optional[List[str]] = None, r18: bool = False
) -> Tuple[list, int]:
    if index:
        image_count = await Setu.filter(is_r18=r18).count() - 1
        if index < 0 or index > image_count:
            return [f"超过当前上下限！({image_count})"], 999
        image_list = [await Setu.query_image(index, r18=r18)]
    elif tags:
        image_list = await Setu.query_image(tags=tags, r18=r18)
    else:
        image_list = await Setu.query_image(r18=r18)
    if not image_list:
        return ["没找到符合条件的色图..."], 998
    return image_list, 200  # type: ignore


# 初始化消息
def gen_message(setu_image: Setu) -> str:
    """判断是否获取图片信息

    Args:
        setu_image (Setu): Setu

    Returns:
        str: 图片信息
    """
    local_id = setu_image.local_id
    title = setu_image.title
    author = setu_image.author
    pid = setu_image.pid
    if Config.get_config("send_setu", "SHOW_INFO"):
        return f"id：{local_id}\n" f"title：{title}\n" f"author：{author}\n" f"PID：{pid}\n"
    return ""


# 罗翔老师！
def get_luoxiang(impression):
    initial_setu_probability = Config.get_config(
        "send_setu", "INITIAL_SETU_PROBABILITY"
    )
    if initial_setu_probability:
        probability = float(impression) + initial_setu_probability * 100
        if probability < random.randint(1, 101):
            return (
                "我为什么要给你发这个？"
                + image(
                    IMAGE_PATH
                    / "luoxiang"
                    / random.choice(os.listdir(IMAGE_PATH / "luoxiang"))
                )
                + f"\n(快向{NICKNAME}签到提升好感度吧！)"
            )
    return None


async def find_img_index(img_url, user_id):
    if not await AsyncHttpx.download_file(
        img_url,
        TEMP_PATH / f"{user_id}_find_setu_index.jpg",
        timeout=Config.get_config("send_setu", "TIMEOUT"),
    ):
        return "检索图片下载上失败..."
    img_hash = str(get_img_hash(TEMP_PATH / f"{user_id}_find_setu_index.jpg"))
    if setu_img := await Setu.get_or_none(img_hash=img_hash):
        return (
            f"id：{setu_img.local_id}\n"
            f"title：{setu_img.title}\n"
            f"author：{setu_img.author}\n"
            f"PID：{setu_img.pid}"
        )
    return "该图不在色图库中或色图库未更新！"


# 处理色图数据
def _setu_data_process(
    data: dict, command: str
) -> Tuple[List[str], List[str], List[Tuple[Any, ...]]]:
    urls = []
    text_list = []
    add_databases_list = []
    for i in range(len(data)):
        img_url = data[i]["urls"]["original"]
        img_url = change_pixiv_image_links(img_url)
        title = data[i]["title"]
        author = data[i]["author"]
        pid = data[i]["pid"]
        urls.append(img_url)
        text_list.append(f"title：{title}\nauthor：{author}\nPID：{pid}")
        tags = []
        for j in range(len(data[i]["tags"])):
            tags.append(data[i]["tags"][j])
        if command != "色图r":
            if "R-18" in tags:
                tags.remove("R-18")
        add_databases_list.append(
            (
                title,
                author,
                pid,
                "",
                img_url,
                ",".join(tags),
            )
        )
    return urls, text_list, add_databases_list
