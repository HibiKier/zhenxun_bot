# -*- coding: utf-8 -*-
import io
from typing import List, Tuple, Union
import aiofiles
from utils.utils import get_local_proxy
from utils.user_agent import get_user_agent
from configs.path_config import IMAGE_PATH
from asyncio.exceptions import TimeoutError
from utils.message_builder import image

import aiohttp
from lxml.html import fromstring
from nonebot.adapters.cqhttp import Message

from .formdata import FormData

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryPpuR3EZ1Ap2pXv8W",
    'Connection': 'keep-alive',
    'Host': 'saucenao.com', 'Origin': 'https://saucenao.com', 'Referer': 'https://saucenao.com/index.php',
    'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}


def parse_html(html: str):
    """
    解析nao返回的html
    :param html:
    :return:
    """
    selector = fromstring(html)
    for tag in selector.xpath('//div[@class="result"]/table'):
        pic_url = tag.xpath('./tr/td/div/a/img/@src')
        if pic_url:
            pic_url = pic_url[0]
        else:
            pic_url = None  # 相似度
        xsd: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultmatchinfo"]/div[@class="resultsimilarityinfo"]/text()')
        if xsd:
            xsd = xsd[0]
        else:
            xsd = "没有写"  # 相似度
        title: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resulttitle"]/strong/text()')
        if title:
            title = title[0]
        else:
            title = "没有写"  # 标题
        # pixiv id
        pixiv_id: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resultcontentcolumn"]/a[1]/@href')
        if pixiv_id:
            pixiv_id = pixiv_id[0]
        else:
            pixiv_id = "没有说"
        member: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resultcontentcolumn"]/a[2]/@href')
        if member:
            member = member[0]
        else:
            member = "没有说"
        yield pic_url, xsd, title, pixiv_id, member


async def get_pic_from_url(url: str):
    """
    从url搜图
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = io.BytesIO(await resp.read())
        data = FormData(boundary="----WebKitFormBoundaryPpuR3EZ1Ap2pXv8W")
        data.add_field(name="file", value=content, content_type="image/jpeg",
                       filename="blob")
        async with session.post("https://saucenao.com/search.php", data=data, headers=header) as res:
            html = await res.text()
            image_data = [each for each in parse_html(html)]
    return image_data


async def get_des(url: str, user_id: int):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: Union[str, Message] = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        # print(pic)
        if int(str(pic[1]).split('.')[0]) > 80:
            msg = await download_img(pic[0], user_id) \
                  + f"\n相似度:{pic[1]}" \
                    f"\n标题:{pic[2] if (str(pic[2]).strip() != 'Creator:' and len(str(pic[2]).split('-')) < 3) else '未知'}" \
                    f"\nPID:{pic[3]}" \
                    f"\nmember:{pic[4]}\n"
            yield msg
    pass


async def download_img(url, user_id):
    try:
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, proxy=get_local_proxy(), timeout=7) as response:
                async with aiofiles.open(IMAGE_PATH + f'temp/{user_id}_pic_find.png', 'wb') as f:
                    await f.write(await response.read())
                    return image(f'{user_id}_pic_find.png', 'temp')
    except TimeoutError:
        return image(url)



