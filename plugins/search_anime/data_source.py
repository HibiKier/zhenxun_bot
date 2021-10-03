from lxml import etree
import feedparser
from urllib import parse
from services.log import logger
import aiohttp
import time
from utils.utils import get_local_proxy


async def from_anime_get_info(key_word: str, max_: int) -> str:
    s_time = time.time()
    repass = ""
    url = "https://share.dmhy.org/topics/rss/rss.xml?keyword=" + parse.quote(key_word)
    try:
        repass = await get_repass(url, max_)
    except Exception as e:
        logger.error("Timeout! {}".format(e))

    return f"搜索 {key_word} 结果（耗时 {int(time.time() - s_time)} 秒）：\n" + repass


async def get_repass(url: str, max_: int) -> str:
    putline = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=20) as response:
            d = feedparser.parse(await response.text())
            url_list = [e.link for e in d.entries][:max_]
            for u in url_list:
                try:
                    async with session.get(
                        u, proxy=get_local_proxy(), timeout=20
                    ) as res:
                        html = etree.HTML(await res.text())
                        magent = html.xpath('.//a[@id="a_magnet"]/text()')[0]
                        title = html.xpath(".//h3/text()")[0]
                        item = html.xpath(
                            '//div[@class="info resource-info right"]/ul/li'
                        )
                        class_a = (
                            item[0]
                            .xpath("string(.)")[5:]
                            .strip()
                            .replace("\xa0", "")
                            .replace("\t", "")
                        )
                        size = item[3].xpath("string(.)")[5:].strip()
                        putline.append(
                            "【{}】| {}\n【{}】| {}".format(class_a, title, size, magent)
                        )
                except Exception as e:
                    logger.warning(f"搜番超时 e：{e}")

        repass = "\n\n".join(putline)

        return repass


# print(asyncio.get_event_loop().run_until_complete(from_anime_get_info('进击的巨人', 1234556)))
