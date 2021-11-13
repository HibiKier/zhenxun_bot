from utils.user_agent import get_user_agent
import aiohttp
from configs.config import Config
from bs4 import BeautifulSoup
from utils.utils import get_local_proxy
import platform

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


url = "http://www.eclzz.world"


async def get_bt_info(keyword: str, page: str):
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        async with session.get(
            f"{url}/s/{keyword}_rel_{page}.html", proxy=get_local_proxy(), timeout=5
        ) as response:
            text = await response.text()
            if text.find("大约0条结果") != -1:
                return
            soup = BeautifulSoup(text, "lxml")
            item_lst = soup.find_all("div", {"class": "search-item"})
            bt_max_num = Config.get_config("bt", "BT_MAX_NUM")
            bt_max_num = bt_max_num if bt_max_num < len(item_lst) else len(item_lst)
            for item in item_lst[:bt_max_num]:
                divs = item.find_all("div")
                title = (
                    str(divs[0].find("a").text)
                    .replace("<em>", "")
                    .replace("</em>", "")
                    .strip()
                )
                spans = divs[2].find_all("span")
                itype = spans[0].text
                create_time = spans[1].find("b").text
                file_size = spans[2].find("b").text
                link = await get_download_link(divs[0].find("a")["href"], session)
                yield title, itype, create_time, file_size, link


async def get_download_link(_url: str, session) -> str:
    async with session.get(
        f"{url}{_url}", proxy=get_local_proxy(), timeout=30
    ) as response:
        soup = BeautifulSoup(await response.text(), "lxml")
        return soup.find("a", {"id": "down-url"})["href"]
