from aiohttp.client_exceptions import (
    ClientOSError,
    ServerDisconnectedError,
    ClientConnectorError,
)
from asyncpg.exceptions import UniqueViolationError
from models.omega_pixiv_illusts import OmegaPixivIllusts
from asyncio.locks import Semaphore
from aiohttp import ClientPayloadError
from aiohttp.client import ClientSession
from asyncio.exceptions import TimeoutError
from models.pixiv import Pixiv
from typing import List
from utils.utils import get_local_proxy, change_picture_links
from utils.image_utils import CreateImg
from services.log import logger
from configs.config import HIBIAPI_BOOKMARKS, HIBIAPI, PIX_IMAGE_SIZE
from configs.path_config import TEMP_PATH
import platform
import aiohttp
import asyncio
import aiofiles
import math

try:
    import ujson as json
except ModuleNotFoundError:
    import json

if str(platform.system()).lower() == "windows":
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

search_url = f"{HIBIAPI}/api/pixiv/search"
member_illust_url = f"{HIBIAPI}/api/pixiv/member_illust"
illust_url = f"{HIBIAPI}/api/pixiv/illust"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}


# 开始更新
async def start_update_image_url(current_keyword: List[str], black_pid: List[str]):
    pid_count = 0
    pic_count = 0
    tasks = []
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(headers=headers) as session:
        for keyword in current_keyword:
            for page in range(1, 110):
                if keyword.startswith("uid:"):
                    url = member_illust_url
                    params = {"id": keyword[4:], "page": page}
                    if page == 30:
                        break
                elif keyword.startswith("pid:"):
                    url = illust_url
                    params = {"id": keyword[4:]}
                else:
                    url = search_url
                    params = {"word": keyword, "page": page}
                tasks.append(
                    asyncio.ensure_future(
                        search_image(
                            url, keyword, params, semaphore, session, page, black_pid
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
    session: ClientSession,
    page: int = 1,
    black: List[str] = None,
):
    tmp_pid = []
    pic_count = 0
    pid_count = 0
    async with semaphore:
        try:
            async with session.get(
                url,
                params=params,
                proxy=get_local_proxy(),
            ) as response:
                data = await response.json()
                if (
                    not data
                    or data.get("error")
                    or (not data.get("illusts") and not data.get("illust"))
                ):
                    return 0, 0
                if url != illust_url:
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
                            bookmarks >= HIBIAPI_BOOKMARKS
                            or (url == member_illust_url and bookmarks >= 1500)
                            or (url == illust_url)
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
                                # await download_image(img_url, session)
                        except UniqueViolationError:
                            logger.warning(f'{data["pid"]} | {img_url} 已存在...')
                    # 下载图片
                    #  if not os.path.exists(f'{image_path}/
                    # {img_url[img_url.rfind("/") + 1:]}'):
                    #     await download_image(img_url, session)
        except (ServerDisconnectedError, ClientConnectorError, ClientOSError):
            logger.warning("搜索图片服务被关闭，再次调用....")
            await search_image(url, keyword, params, semaphore, session, page, black)
    return pid_count, pic_count


# 下载图片
async def download_image(img_url: str, session: ClientSession, _count: int = 1):
    try:
        async with session.get(img_url, proxy=get_local_proxy()) as response:
            logger.info(f"下载图片 --> {img_url}")
            async with aiofiles.open(f'tmp/{img_url.split("/")[-1]}', "wb") as f:
                await f.write(await response.read())
            # async with semaphore:
            #    await asyncio.get_event_loop().run_in_executor(None,
            # upload_image, img_url[img_url.rfind("/")+1:])
    except ServerDisconnectedError:
        logger.warning(f"下载图片服务被关闭，第 {_count} 次调用....")
        await download_image(img_url, session, _count + 1)
    except ClientOSError:
        logger.warning(f"远程连接被关闭，第 {_count} 次调用....")
        await download_image(
            img_url.replace("i.pximg.net", "i.pixiv.cat"), session, _count + 1
        )
    except TimeoutError:
        logger.warning(f"下载或写入超时，第 {_count} 次调用....")
        await download_image(img_url, session, _count + 1)
    except ClientPayloadError:
        pass


async def get_image(img_url: str, user_id: int) -> str:
    async with aiohttp.ClientSession(headers=headers) as session:
        if 'https://www.pixiv.net/artworks' in img_url:
            pid = img_url.rsplit('/', maxsplit=1)[-1]
            params = {"id": pid}
            for _ in range(3):
                try:
                    async with session.get(
                        illust_url,
                        params=params,
                        proxy=get_local_proxy(),
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get('illust'):
                                if data['illust']['page_count'] == 1:
                                    img_url = data['illust']['meta_single_page']['original_image_url']
                                else:
                                    img_url = data['illust']["meta_pages"][0]["image_urls"]["original"]
                                break
                except (ClientConnectorError, TimeoutError):
                    pass
        old_img_url = img_url
        img_url = change_picture_links(img_url, PIX_IMAGE_SIZE)
        for _ in range(3):
            try:
                async with session.get(
                    img_url,
                    proxy=get_local_proxy(),
                ) as response:
                    if response.status == 404:
                        img_url = old_img_url
                        continue
                    async with aiofiles.open(
                        f"{TEMP_PATH}/pix_{user_id}_{img_url[-10:-4]}.jpg", "wb"
                    ) as f:
                        await f.write(await response.read())
                    return f"pix_{user_id}_{img_url[-10:-4]}.jpg"
            except (ClientConnectorError, TimeoutError):
                pass


# 检测UID或PID是否有效
async def uid_pid_exists(id_: str) -> bool:
    if id_.startswith("uid:"):
        url = f"{HIBIAPI}/api/pixiv/member"
    elif id_.startswith("pid:"):
        url = illust_url
    else:
        return False
    params = {"id": int(id_[4:])}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params, proxy=get_local_proxy()) as response:
            data = await response.json()
            if data.get("error"):
                return False
    return True


async def get_keyword_num(keyword: str) -> "int , int":
    count, r18_count = await Pixiv.get_keyword_num(keyword.split())
    count_, setu_count, r18_count_ = await OmegaPixivIllusts.get_keyword_num(keyword.split())
    return count, r18_count, count_, setu_count, r18_count_


async def remove_image(pid: int, img_p: str) -> bool:
    if img_p:
        if "p" not in img_p:
            img_p = f"p{img_p}"
    return await Pixiv.remove_image_data(pid, img_p)


def gen_keyword_pic(
    _pass_keyword: List[str], not_pass_keyword: List[str], is_superuser: bool
):
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
    A = CreateImg(img_width, 1100)
    for x in list(img_data.keys()):
        if img_data[x]["data"]:
            img = CreateImg(img_data[x]["width"] * 200, 1100, 200, 1100, font_size=40)
            start_index = 0
            end_index = 40
            total_index = img_data[x]["width"] * 40
            for _ in range(img_data[x]["width"]):
                tmp = CreateImg(198, 1100, font_size=20)
                text_img = CreateImg(198, 100, font_size=50)
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
                background_img = CreateImg(200, 1100, color="#FFE4C4")
                background_img.paste(tmp, (1, 1))
                img.paste(background_img)
            A.paste(img, (current_width, 0))
            current_width += img_data[x]["width"] * 200
    return A.pic2bs4()


def _check_black(img_urls: List[str], black: List[str]):
    for b in black:
        for img_url in img_urls:
            # img_url = img_url[img_url.rfind('/')+1: img_url.rfind('.')]
            if b in img_url:
                return False
    return True
