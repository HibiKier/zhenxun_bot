from asyncio.exceptions import TimeoutError
from pathlib import Path

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.utils import change_img_md5

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6;"
    " rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Referer": "https://www.pixiv.net/",
}


async def get_pixiv_urls(
    mode: str, num: int = 10, page: int = 1, date: str | None = None
) -> tuple[list[tuple[str, str, list[str]] | str], int]:
    """获取排行榜图片url

    参数:
        mode: 模式类型
        num: 数量.
        page: 页数.
        date: 日期.

    返回:
        tuple[list[tuple[str, str, list[str]] | str], int]: 图片标题作者url数据，请求状态
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
) -> tuple[list[tuple[str, str, list[str]] | str], int]:
    """搜图图片url

    参数:
        keyword: 关键词
        num: 数量
        page: 页数
        r18: 是否r18

    返回:
        tuple[list[tuple[str, str, list[str]] | str], int]: 图片标题作者url数据，请求状态
    """
    params = {"word": keyword, "page": page}
    hibiapi = Config.get_config("hibiapi", "HIBIAPI")
    hibiapi = hibiapi[:-1] if hibiapi[-1] == "/" else hibiapi
    search_url = f"{hibiapi}/api/pixiv/search"
    return await parser_data(search_url, num, params, "search", r18)


async def parser_data(
    url: str, num: int, params: dict, type_: str, r18: int = 0
) -> tuple[list[tuple[str, str, list[str]] | str], int]:
    """解析数据搜索

    参数:
        url: 访问URL
        num: 数量
        params: 请求参数
        type_: 类型，rank或search
        r18: 是否r18.

    返回:
        tuple[list[tuple[str, str, list[str]] | str], int]: 图片标题作者url数据，请求状态
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
            logger.error(f"P站排行/搜图解析数据发生错误", e=e)
            return ["发生了一些些错误..."], 995
    else:
        return ["网络不太好？没有该页数？也许过一会就好了..."], 998
    num = num if num < 30 else 30
    _data = []
    for x in data:
        if x["page_count"] < Config.get_config("pixiv_rank_search", "MAX_PAGE_LIMIT"):
            if type_ == "search" and r18 == 1:
                if "R-18" in str(x["tags"]):
                    continue
            _data.append(x)
        if len(_data) == num:
            break
    for x in _data:
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
    urls: list[str], user_id: str, forward_msg_index: int | None = None
) -> list[Path]:
    """下载图片

    参数:
        urls: 图片链接
        user_id: 用户id
        forward_msg_index: 转发消息中的图片排序.

    返回:
        MessageFactory: 图片
    """
    result_list = []
    index = 0
    for url in urls:
        ws_url = Config.get_config("pixiv", "PIXIV_NGINX_URL")
        url = url.replace("_webp", "")
        if ws_url:
            url = url.replace("i.pximg.net", ws_url).replace("i.pixiv.cat", ws_url)
        try:
            file = (
                TEMP_PATH / f"{user_id}_{forward_msg_index}_{index}_pixiv.jpg"
                if forward_msg_index is not None
                else TEMP_PATH / f"{user_id}_{index}_pixiv.jpg"
            )
            file = Path(file)
            try:
                if await AsyncHttpx.download_file(
                    url,
                    file,
                    timeout=Config.get_config("pixiv_rank_search", "TIMEOUT"),
                    headers=headers,
                ):
                    change_img_md5(file)
                    image = None
                    if forward_msg_index is not None:
                        image = (
                            TEMP_PATH
                            / f"{user_id}_{forward_msg_index}_{index}_pixiv.jpg"
                        )
                    else:
                        image = TEMP_PATH / f"{user_id}_{index}_pixiv.jpg"
                    if image:
                        result_list.append(image)
                index += 1
            except OSError:
                if file.exists():
                    file.unlink()
        except Exception as e:
            logger.error(f"P站排行/搜图下载图片错误", e=e)
    return result_list
