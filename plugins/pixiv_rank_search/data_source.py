from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from asyncio.exceptions import TimeoutError
from configs.config import Config
from utils.http_utils import AsyncHttpx
from typing import Optional
from services.log import logger
from pathlib import Path
import platform

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net",
}


async def get_pixiv_urls(
    mode: str, num: int = 10, page: int = 1, date: Optional[str] = None
) -> "list, int":
    """
    拿到pixiv rank图片url
    :param mode: 模式
    :param num: 数量
    :param page: 页数
    :param date: 日期
    """
    params = {"mode": mode, "page": page}
    if date:
        params["date"] = date
    hibiapi = Config.get_config("hibiapi", "HIBIAPI")
    hibiapi = hibiapi[:-1] if hibiapi[-1] == "/" else hibiapi
    rank_url = f"{hibiapi}/api/pixiv/rank"
    return await parser_data(rank_url, num, params, "rank")


async def search_pixiv_urls(
    keyword: str, num: int, page: int, r18: int
) -> "list, list":
    """
    搜图图片的url
    :param keyword: 关键词
    :param num: 数量
    :param page: 页数
    :param r18: 是否r18
    """
    params = {"word": keyword, "page": page}
    hibiapi = Config.get_config("hibiapi", "HIBIAPI")
    hibiapi = hibiapi[:-1] if hibiapi[-1] == "/" else hibiapi
    search_url = f"{hibiapi}/api/pixiv/search"
    return await parser_data(search_url, num, params, "search", r18)


async def parser_data(
    url: str, num: int, params: dict, type_: str, r18: int = 0
) -> "list, int":
    """
    解析数据
    :param url: hibiapi搜索url
    :param num: 数量
    :param params: 参数
    :param type_: 类型，rank或search
    :param r18: 是否r18
    """
    info_list = []
    for _ in range(3):
        try:
            response = await AsyncHttpx.get(
                url,
                params=params,
                timeout=Config.get_config("pixiv_rank_search", "TIMEOUT"),
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("illusts"):
                    data = data["illusts"]
                    break
        except TimeoutError:
            pass
        except Exception as e:
            logger.error(f"P站排行/搜图解析数据发生错误 {type(e)}：{e}")
            return ["发生了一些些错误..."], 995
    else:
        return ["网络不太好？没有该页数？也许过一会就好了..."], 998
    num = num if num < 30 else 30
    _data = []
    for x in data:
        if x["page_count"] < Config.get_config("pixiv_rank_search", "MAX_PAGE_LIMIT"):
            _data.append(x)
        if len(_data) == num:
            break
    for x in _data:
        if type_ == "search" and r18 == 1:
            if "R-18" in str(x["tags"]):
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
    """
    下载图片
    :param urls: 图片链接
    :param user_id: 用户id
    :param forward_msg_index: 转发消息中的图片排序
    """
    result = ""
    index = 0
    for url in urls:
        ws_url = Config.get_config("pixiv", "PIXIV_NGINX_URL")
        if ws_url:
            url = (
                url.replace("i.pximg.net", ws_url)
                .replace("i.pixiv.cat", ws_url)
                .replace("_webp", "")
            )
            try:
                file = (
                    f"{IMAGE_PATH}/temp/{user_id}_{forward_msg_index}_{index}_pixiv.jpg"
                    if forward_msg_index is not None
                    else f"{IMAGE_PATH}/temp/{user_id}_{index}_pixiv.jpg"
                )
                file = Path(file)
                try:
                    if await AsyncHttpx.download_file(
                        url,
                        file,
                        timeout=Config.get_config("pixiv_rank_search", "TIMEOUT"),
                    ):
                        if forward_msg_index is not None:
                            result += image(
                                f"{user_id}_{forward_msg_index}_{index}_pixiv.jpg",
                                "temp",
                            )
                        else:
                            result += image(f"{user_id}_{index}_pixiv.jpg", "temp")
                    index += 1
                except OSError:
                    if file.exists():
                        file.unlink()
            except Exception as e:
                logger.error(f"P站排行/搜图下载图片错误 {type(e)}：{e}")
    return result
