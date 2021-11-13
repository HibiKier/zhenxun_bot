from lxml import etree
import feedparser
from urllib import parse
from services.log import logger
from typing import List
import aiohttp
import time
from utils.utils import get_local_proxy


async def from_anime_get_info(key_word: str, max_: int) -> List[str]:
    s_time = time.time()
    repass = ""
    url = "https://share.dmhy.org/topics/rss/rss.xml?keyword=" + parse.quote(key_word)
    try:
        repass = await get_repass(url, max_)
    except Exception as e:
        logger.error("Timeout! {}".format(e))
    repass.insert(0, f"搜索 {key_word} 结果（耗时 {int(time.time() - s_time)} 秒）：\n")
    return repass


async def get_repass(url: str, max_: int) -> List[str]:
    put_line = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=20) as response:
            d = feedparser.parse(await response.text())
            max_ = max_ if max_ < len([e.link for e in d.entries]) else len([e.link for e in d.entries])
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
                        put_line.append(
                            "【{}】| {}\n【{}】| {}".format(class_a, title, size, magent)
                        )
                except Exception as e:
                    logger.warning(f"搜番超时 e：{e}")
    return put_line


