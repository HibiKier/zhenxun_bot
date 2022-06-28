from asyncpg.exceptions import UniqueViolationError
from ._model.omega_pixiv_illusts import OmegaPixivIllusts
from asyncio.locks import Semaphore
from asyncio.exceptions import TimeoutError
from ._model.pixiv import Pixiv
from typing import List, Optional
from utils.utils import change_pixiv_image_links, change_img_md5
from utils.image_utils import BuildImage
from utils.http_utils import AsyncHttpx
from services.log import logger
from configs.config import Config
from configs.path_config import TEMP_PATH
import aiofiles
import platform
import asyncio
import math

try:
    import ujson as json
except ModuleNotFoundError:
    import json

# if str(platform.system()).lower() == "windows":
#     policy = asyncio.WindowsSelectorEventLoopPolicy()
#     asyncio.set_event_loop_policy(policy)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}

HIBIAPI = Config.get_config("hibiapi", "HIBIAPI")
if not HIBIAPI:
    HIBIAPI = "https://api.obfs.dev"
HIBIAPI = HIBIAPI[:-1] if HIBIAPI[-1] == "/" else HIBIAPI


async def start_update_image_url(
    current_keyword: List[str], black_pid: List[str]
) -> "int, int":
    """
    开始更新图片url
    :param current_keyword: 关键词
    :param black_pid: 黑名单pid
    :return: pid数量和图片数量
    """
    global HIBIAPI
    pid_count = 0
    pic_count = 0
    tasks = []
    semaphore = asyncio.Semaphore(10)
    for keyword in current_keyword:
        for page in range(1, 110):
            if keyword.startswith("uid:"):
                url = f"{HIBIAPI}/api/pixiv/member_illust"
                params = {"id": keyword[4:], "page": page}
                if page == 30:
                    break
            elif keyword.startswith("pid:"):
                url = f"{HIBIAPI}/api/pixiv/illust"
                params = {"id": keyword[4:]}
            else:
                url = f"{HIBIAPI}/api/pixiv/search"
                params = {"word": keyword, "page": page}
            tasks.append(
                asyncio.ensure_future(
                    search_image(
                        url, keyword, params, semaphore, page, black_pid
                    )
                )
            )
            if keyword.startswith("pid:"):
                break
    result = await asyncio.gather(*tasks)
    for x in result:
        pid_count += x[0]
        pic_count += x[1]
    return pid_count, pic_count


async def search_image(
    url: str,
    keyword: str,
    params: dict,
    semaphore: Semaphore,
    page: int = 1,
    black: List[str] = None,
) -> "int, int":
    """
    搜索图片
    :param url: 搜索url
    :param keyword: 关键词
    :param params: params参数
    :param semaphore: semaphore
    :param page: 页面
    :param black: pid黑名单
    :return: pid数量和图片数量
    """
    tmp_pid = []
    pic_count = 0
    pid_count = 0
    async with semaphore:
        try:
            data = (await AsyncHttpx.get(url, params=params)).json()
            if (
                not data
                or data.get("error")
                or (not data.get("illusts") and not data.get("illust"))
            ):
                return 0, 0
            if url != f"{HIBIAPI}/api/pixiv/illust":
                logger.info(f'{keyword}: 获取数据成功...数据总量：{len(data["illusts"])}')
                data = data["illusts"]
            else:
                logger.info(f'获取数据成功...PID：{params.get("id")}')
                data = [data["illust"]]
            img_data = {}
            for x in data:
                pid = x["id"]
                title = x["title"]
                width = x["width"]
                height = x["height"]
                view = x["total_view"]
                bookmarks = x["total_bookmarks"]
                uid = x["user"]["id"]
                author = x["user"]["name"]
                tags = []
                for tag in x["tags"]:
                    for i in tag:
                        if tag[i]:
                            tags.append(tag[i])
                img_urls = []
                if x["page_count"] == 1:
                    img_urls.append(x["meta_single_page"]["original_image_url"])
                else:
                    for urls in x["meta_pages"]:
                        img_urls.append(urls["image_urls"]["original"])
                if (
                    (
                        bookmarks
                        >= Config.get_config("pix", "SEARCH_HIBIAPI_BOOKMARKS")
                        or (
                            url == f"{HIBIAPI}/api/pixiv/member_illust"
                            and bookmarks >= 1500
                        )
                        or (url == f"{HIBIAPI}/api/pixiv/illust")
                    )
                    and len(img_urls) < 10
                    and _check_black(img_urls, black)
                ):
                    img_data[pid] = {
                        "pid": pid,
                        "title": title,
                        "width": width,
                        "height": height,
                        "view": view,
                        "bookmarks": bookmarks,
                        "img_urls": img_urls,
                        "uid": uid,
                        "author": author,
                        "tags": tags,
                    }
                else:
                    continue
            for x in img_data.keys():
                data = img_data[x]
                for img_url in data["img_urls"]:
                    img_p = img_url[img_url.rfind("_") + 1 : img_url.rfind(".")]
                    try:
                        if await Pixiv.add_image_data(
                            data["pid"],
                            data["title"],
                            data["width"],
                            data["height"],
                            data["view"],
                            data["bookmarks"],
                            img_url,
                            img_p,
                            data["uid"],
                            data["author"],
                            ",".join(data["tags"]),
                        ):
                            if data["pid"] not in tmp_pid:
                                pid_count += 1
                                tmp_pid.append(data["pid"])
                            pic_count += 1
                            logger.info(f'存储图片PID：{data["pid"]} IMG_P：{img_p}')
                    except UniqueViolationError:
                        logger.warning(f'{data["pid"]} | {img_url} 已存在...')
        except Exception as e:
            logger.warning(f"PIX在线搜索图片错误，已再次调用 {type(e)}：{e}")
            await search_image(url, keyword, params, semaphore, page, black)
    return pid_count, pic_count


async def get_image(img_url: str, user_id: int) -> Optional[str]:
    """
    下载图片
    :param img_url:
    :param user_id:
    :return: 图片名称
    """
    if "https://www.pixiv.net/artworks" in img_url:
        pid = img_url.rsplit("/", maxsplit=1)[-1]
        params = {"id": pid}
        for _ in range(3):
            try:
                response = await AsyncHttpx.get(f"{HIBIAPI}/api/pixiv/illust", params=params)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("illust"):
                        if data["illust"]["page_count"] == 1:
                            img_url = data["illust"]["meta_single_page"][
                                "original_image_url"
                            ]
                        else:
                            img_url = data["illust"]["meta_pages"][0][
                                "image_urls"
                            ]["original"]
                        break
            except TimeoutError:
                pass
    old_img_url = img_url
    img_url = change_pixiv_image_links(
        img_url, Config.get_config("pix", "PIX_IMAGE_SIZE"), Config.get_config("pixiv", "PIXIV_NGINX_URL")
    )
    old_img_url = change_pixiv_image_links(
        old_img_url, None, Config.get_config("pixiv", "PIXIV_NGINX_URL")
    )
    for _ in range(3):
        try:
            response = await AsyncHttpx.get(img_url, headers=headers, timeout=Config.get_config("pix", "TIMEOUT"),)
            if response.status_code == 404:
                img_url = old_img_url
                continue
            async with aiofiles.open(
                TEMP_PATH / f"pix_{user_id}_{img_url.split('/')[-1][:-4]}.jpg", "wb"
            ) as f:
                await f.write(response.content)
            change_img_md5(TEMP_PATH / f"pix_{user_id}_{img_url.split('/')[-1][:-4]}.jpg")
            return TEMP_PATH / f"pix_{user_id}_{img_url.split('/')[-1][:-4]}.jpg"
        except TimeoutError:
            logger.warning(f"PIX：{img_url} 图片下载超时...")
            pass
    return None


async def uid_pid_exists(id_: str) -> bool:
    """
    检测 pid/uid 是否有效
    :param id_: pid/uid
    """
    if id_.startswith("uid:"):
        url = f"{HIBIAPI}/api/pixiv/member"
    elif id_.startswith("pid:"):
        url = f"{HIBIAPI}/api/pixiv/illust"
    else:
        return False
    params = {"id": int(id_[4:])}
    data = (await AsyncHttpx.get(url, params=params)).json()
    if data.get("error"):
        return False
    return True


async def get_keyword_num(keyword: str) -> "int, int, int, int, int":
    """
    查看图片相关 tag 数量
    :param keyword: 关键词tag
    """
    count, r18_count = await Pixiv.get_keyword_num(keyword.split())
    count_, setu_count, r18_count_ = await OmegaPixivIllusts.get_keyword_num(
        keyword.split()
    )
    return count, r18_count, count_, setu_count, r18_count_


async def remove_image(pid: int, img_p: str) -> bool:
    """
    删除置顶图片
    :param pid: pid
    :param img_p: 图片 p 如 p0，p1 等
    """
    if img_p:
        if "p" not in img_p:
            img_p = f"p{img_p}"
    return await Pixiv.remove_image_data(pid, img_p)


def gen_keyword_pic(
    _pass_keyword: List[str], not_pass_keyword: List[str], is_superuser: bool
):
    """
    已通过或未通过的所有关键词/uid/pid
    :param _pass_keyword: 通过列表
    :param not_pass_keyword: 未通过列表
    :param is_superuser: 是否超级用户
    """
    _keyword = [
        x
        for x in _pass_keyword
        if not x.startswith("uid:")
        and not x.startswith("pid:")
        and not x.startswith("black:")
    ]
    _uid = [x for x in _pass_keyword if x.startswith("uid:")]
    _pid = [x for x in _pass_keyword if x.startswith("pid:")]
    _n_keyword = [
        x
        for x in not_pass_keyword
        if not x.startswith("uid:")
        and not x.startswith("pid:")
        and not x.startswith("black:")
    ]
    _n_uid = [
        x
        for x in not_pass_keyword
        if x.startswith("uid:") and not x.startswith("black:")
    ]
    _n_pid = [
        x
        for x in not_pass_keyword
        if x.startswith("pid:") and not x.startswith("black:")
    ]
    img_width = 0
    img_data = {
        "_keyword": {"width": 0, "data": _keyword},
        "_uid": {"width": 0, "data": _uid},
        "_pid": {"width": 0, "data": _pid},
        "_n_keyword": {"width": 0, "data": _n_keyword},
        "_n_uid": {"width": 0, "data": _n_uid},
        "_n_pid": {"width": 0, "data": _n_pid},
    }
    for x in list(img_data.keys()):
        img_data[x]["width"] = math.ceil(len(img_data[x]["data"]) / 40)
        img_width += img_data[x]["width"] * 200
    if not is_superuser:
        img_width = (
            img_width
            - (
                img_data["_n_keyword"]["width"]
                + img_data["_n_uid"]["width"]
                + img_data["_n_pid"]["width"]
            )
            * 200
        )
        del img_data["_n_keyword"]
        del img_data["_n_pid"]
        del img_data["_n_uid"]
    current_width = 0
    A = BuildImage(img_width, 1100)
    for x in list(img_data.keys()):
        if img_data[x]["data"]:
            img = BuildImage(img_data[x]["width"] * 200, 1100, 200, 1100, font_size=40)
            start_index = 0
            end_index = 40
            total_index = img_data[x]["width"] * 40
            for _ in range(img_data[x]["width"]):
                tmp = BuildImage(198, 1100, font_size=20)
                text_img = BuildImage(198, 100, font_size=50)
                key_str = "\n".join(
                    [key for key in img_data[x]["data"][start_index:end_index]]
                )
                tmp.text((10, 100), key_str)
                if x.find("_n") == -1:
                    text_img.text((24, 24), "已收录")
                else:
                    text_img.text((24, 24), "待收录")
                tmp.paste(text_img, (0, 0))
                start_index += 40
                end_index = (
                    end_index + 40 if end_index + 40 <= total_index else total_index
                )
                background_img = BuildImage(200, 1100, color="#FFE4C4")
                background_img.paste(tmp, (1, 1))
                img.paste(background_img)
            A.paste(img, (current_width, 0))
            current_width += img_data[x]["width"] * 200
    return A.pic2bs4()


def _check_black(img_urls: List[str], black: List[str]) -> bool:
    """
    检测pid是否在黑名单中
    :param img_urls: 图片img列表
    :param black: 黑名单
    :return:
    """
    for b in black:
        for img_url in img_urls:
            if b in img_url:
                return False
    return True



