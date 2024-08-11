from bs4 import BeautifulSoup

from zhenxun.configs.config import Config
from zhenxun.utils.http_utils import AsyncHttpx, AsyncPlaywright

url = "http://www.eclzz.ink"


async def get_bt_info(keyword: str, page: int):
    """获取资源信息

    参数:
        keyword: 关键词
        page: 页数
    """
    global url
    text = (await AsyncHttpx.get(f"{url}/s/{keyword}_rel_{page}.html", timeout=30)).text
    if "301 Moved Permanently" in text:
        async with AsyncPlaywright.new_page() as _page:
            await _page.goto(url)
            url = _page.url
        text = (
            await AsyncHttpx.get(f"{url}/s/{keyword}_rel_{page}.html", timeout=30)
        ).text
    if "大约0条结果" in text:
        return
    soup = BeautifulSoup(text, "lxml")
    item_lst = soup.find_all("div", {"class": "search-item"})
    bt_max_num = Config.get_config("bt", "BT_MAX_NUM") or 10
    bt_max_num = bt_max_num if bt_max_num < len(item_lst) else len(item_lst)
    for item in item_lst[:bt_max_num]:
        divs = item.find_all("div")
        title = (
            str(divs[0].find("a").text).replace("<em>", "").replace("</em>", "").strip()
        )
        spans = divs[2].find_all("span")
        type_ = spans[0].text
        create_time = spans[1].find("b").text
        file_size = spans[2].find("b").text
        link = await get_download_link(divs[0].find("a")["href"])
        yield title, type_, create_time, file_size, link


async def get_download_link(_url: str) -> str | None:
    """获取资源下载地址

    参数:
        _url: 链接
    """
    text = (await AsyncHttpx.get(f"{url}{_url}")).text
    soup = BeautifulSoup(text, "lxml")
    if fd := soup.find("a", {"id": "down-url"}):
        return fd["href"]  # type: ignore
    return None
