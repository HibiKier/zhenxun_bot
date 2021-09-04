from configs.path_config import IMAGE_PATH
from utils.utils import get_local_proxy
from utils.message_builder import image
from asyncio.exceptions import TimeoutError
from configs.config import HIBIAPI
from aiohttp.client_exceptions import ClientConnectorError
from typing import Optional
from pathlib import Path
import aiohttp
import aiofiles
import platform

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


rank_url = f"{HIBIAPI}/api/pixiv/rank"
search_url = f"{HIBIAPI}/api/pixiv/search"


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}


async def get_pixiv_urls(
    mode: str, num: int = 10, page: int = 1, date: Optional[str] = None
) -> "list, int":
    params = {"mode": mode, "page": page}
    if date:
        params["date"] = date
    return await parser_data(rank_url, num, params, 'rank')


async def search_pixiv_urls(
    keyword: str, num: int, page: int, r18: int
) -> "list, list":
    params = {"word": keyword, 'page': page}
    return await parser_data(search_url, num, params, 'search', r18)


async def parser_data(url: str, num: int, params: dict, type_: str, r18: int = 0) -> "list, int":
    info_list = []
    async with aiohttp.ClientSession() as session:
        for _ in range(3):
            try:
                async with session.get(
                    url, params=params, proxy=get_local_proxy(), timeout=5
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("illusts"):
                            data = data["illusts"]
                            break
            except (TimeoutError, ClientConnectorError):
                pass
        else:
            return ["网络不太好？没有该页数？也许过一会就好了..."], 998
        num = num if num < 30 else 30
        data = data[:num]
        for x in data:
            if type_ == 'search' and r18 == 1:
                if 'R-18' in str(x['tags']):
                    continue
            title = x["title"]
            author = x["user"]["name"]
            urls = []
            if x["page_count"] == 1:
                urls.append(x["image_urls"]["large"])
            else:
                for j in x["meta_pages"]:
                    urls.append(j["image_urls"]["large"])
            info_list.append((title, author, urls))
        return info_list, 200


async def download_pixiv_imgs(
    urls: list, user_id: int, forward_msg_index: int = None
) -> str:
    result = ""
    index = 0
    for url in urls:
        async with aiohttp.ClientSession(headers=headers) as session:
            for _ in range(3):
                try:
                    async with session.get(
                        url, proxy=get_local_proxy(), timeout=3
                    ) as response:
                        if response.status == 200:
                            try:
                                file = (
                                    f"{IMAGE_PATH}/temp/{user_id}_{forward_msg_index}_{index}_pixiv.jpg"
                                    if forward_msg_index is not None
                                    else f"{IMAGE_PATH}/temp/{user_id}_{index}_pixiv.jpg"
                                )
                                file = Path(file)
                                if forward_msg_index is not None:
                                    async with aiofiles.open(
                                        file,
                                        "wb",
                                    ) as f:
                                        await f.write(await response.read())
                                        result += image(
                                            f"{user_id}_{forward_msg_index}_{index}_pixiv.jpg",
                                            "temp",
                                        )
                                else:
                                    async with aiofiles.open(
                                        file,
                                        "wb",
                                    ) as f:
                                        await f.write(await response.read())
                                        result += image(
                                            f"{user_id}_{index}_pixiv.jpg", "temp"
                                        )
                                index += 1
                                break
                            except OSError:
                                file.unlink()
                except (TimeoutError, ClientConnectorError):
                    # result += '\n这张图下载失败了..\n'
                    pass
            else:
                result += "\n这张图下载失败了..\n"
    return result

