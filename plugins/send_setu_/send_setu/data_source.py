from configs.path_config import IMAGE_PATH, TEMP_PATH
from utils.message_builder import image
from services.log import logger
from utils.image_utils import get_img_hash, compressed_image
from asyncpg.exceptions import UniqueViolationError
from asyncio.exceptions import TimeoutError
from typing import List, Optional
from configs.config import NICKNAME, Config
from utils.http_utils import AsyncHttpx
from .._model import Setu
import asyncio
import os
import random

try:
    import ujson as json
except ModuleNotFoundError:
    import json


url = "https://api.lolicon.app/setu/v2"
path = "_setu"
r18_path = "_r18"


# 获取url
async def get_setu_urls(
    tags: List[str], num: int = 1, r18: int = 0, command: str = ""
) -> "List[str], List[str], List[tuple], int":
    tags = tags[:3] if len(tags) > 3 else tags
    params = {
        "r18": r18,  # 添加r18参数 0为否，1为是，2为混合
        "tag": tags,  # 若指定tag
        "num": 100,  # 一次返回的结果数量
        "size": ["original"],
    }
    for count in range(3):
        logger.info(f"get_setu_url: count --> {count}")
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
        except TimeoutError:
            pass
        except Exception as e:
            logger.error(f"send_setu 访问页面错误 {type(e)}：{e}")
    return ["我网线被人拔了..QAQ"], [], [], 999


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}


async def search_online_setu(
    url_: str, id_: Optional[int] = None, path_: Optional[str] = None
) -> "MessageSegment, int":
    """
    下载色图
    :param url_: 色图url
    :param id_: 本地id
    :param path_: 存储路径
    """
    ws_url = Config.get_config("pixiv", "PIXIV_NGINX_URL")
    if ws_url:
        url_ = url_.replace("i.pximg.net", ws_url).replace("i.pixiv.cat", ws_url)
    index = random.randint(1, 100000) if id_ is None else id_
    path_ = IMAGE_PATH / path_ if path_ else TEMP_PATH
    file_name = f"{index}_temp_setu.jpg" if path_ == TEMP_PATH else f"{index}.jpg"
    path_.mkdir(parents=True, exist_ok=True)
    for i in range(3):
        logger.info(f"search_online_setu --> {i}")
        try:
            if not await AsyncHttpx.download_file(
                url_,
                path_ / file_name,
                timeout=Config.get_config("send_setu", "TIMEOUT"),
            ):
                continue
            if id_ is not None:
                if (
                    os.path.getsize(path_ / f"{index}.jpg")
                    > 1024 * 1024 * 1.5
                ):
                    compressed_image(
                        path_ / f"{index}.jpg",
                    )
            logger.info(f"下载 lolicon 图片 {url_} 成功， id：{index}")
            return image(path_ / file_name), index
        except TimeoutError:
            pass
        except Exception as e:
            logger.error(f"send_setu 下载图片错误 {type(e)}：{e}")
    return "图片被小怪兽恰掉啦..!QAQ", -1


# 检测本地是否有id涩图，无的话则下载
async def check_local_exists_or_download(setu_image: Setu) -> "MessageSegment, int":
    path_ = None
    id_ = None
    if Config.get_config("send_setu", "DOWNLOAD_SETU"):
        id_ = setu_image.local_id
        path_ = r18_path if setu_image.is_r18 else path
        file = IMAGE_PATH / path_ / f"{setu_image.local_id}.jpg"
        if file.exists():
            return image(f"{setu_image.local_id}.jpg", path_), 200
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
                r18 = 1 if "R-18" in x[5] else 0
                idx = await Setu.get_image_count(r18)
                await Setu.add_setu_data(
                    idx,
                    x[0],
                    x[1],
                    x[2],
                    x[3],
                    x[4],
                    x[5],
                )
            except UniqueViolationError:
                pass


# 拿到本地色图列表
async def get_setu_list(
    index: Optional[int] = None, tags: Optional[List[str]] = None, r18: int = 0
) -> "list, int":
    if index:
        image_count = await Setu.get_image_count(r18) - 1
        if index < 0 or index > image_count:
            return [f"超过当前上下限！({image_count})"], 999
        image_list = [await Setu.query_image(index, r18=r18)]
    elif tags:
        image_list = await Setu.query_image(tags=tags, r18=r18)
    else:
        image_list = await Setu.query_image(r18=r18)
    if not image_list:
        return ["没找到符合条件的色图..."], 998
    return image_list, 200


# 初始化消息
def gen_message(setu_image: Setu, img_msg: bool = False) -> str:
    local_id = setu_image.local_id
    title = setu_image.title
    author = setu_image.author
    pid = setu_image.pid
    if Config.get_config("send_setu", "SHOW_INFO"):
        return (
            f"id：{local_id}\n"
            f"title：{title}\n"
            f"author：{author}\n"
            f"PID：{pid}\n"
            f"{image(f'{local_id}', f'{r18_path if setu_image.is_r18 else path}') if img_msg else ''}"
        )
    return f"{image(f'{local_id}', f'{r18_path if setu_image.is_r18 else path}') if img_msg else ''}"


# 罗翔老师！
def get_luoxiang(impression):
    probability = (
        impression + Config.get_config("send_setu", "INITIAL_SETU_PROBABILITY") * 100
    )
    if probability < random.randint(1, 101):
        return (
            "我为什么要给你发这个？"
            + image(random.choice(os.listdir(IMAGE_PATH / "luoxiang")), "luoxiang")
            + f"\n(快向{NICKNAME}签到提升好感度吧！)"
        )
    return None


async def get_setu_count(r18: int) -> int:
    """
    获取色图数量
    :param r18: r18类型
    """
    return await Setu.get_image_count(r18)


async def find_img_index(img_url, user_id):
    if not await AsyncHttpx.download_file(
        img_url,
        TEMP_PATH / f"{user_id}_find_setu_index.jpg",
        timeout=Config.get_config("send_setu", "TIMEOUT"),
    ):
        return "检索图片下载上失败..."
    img_hash = str(get_img_hash(TEMP_PATH / f"{user_id}_find_setu_index.jpg"))
    setu_img = await Setu.get_image_in_hash(img_hash)
    if setu_img:
        return (
            f"id：{setu_img.local_id}\n"
            f"title：{setu_img.title}\n"
            f"author：{setu_img.author}\n"
            f"PID：{setu_img.pid}"
        )
    return "该图不在色图库中或色图库未更新！"


# 处理色图数据
def _setu_data_process(data: dict, command: str) -> "list, list, list":
    urls = []
    text_list = []
    add_databases_list = []
    for i in range(len(data)):
        img_url = data[i]["urls"]["original"]
        img_url = (
            img_url.replace("i.pixiv.cat", "i.pximg.net")
            if "i.pixiv.cat" in img_url
            else img_url
        )
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
