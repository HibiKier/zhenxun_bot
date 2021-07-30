# -*- coding: utf-8 -*-
from typing import List, Tuple
from urllib.parse import urljoin
import aiofiles
from utils.utils import get_local_proxy
from utils.user_agent import get_user_agent
from configs.path_config import IMAGE_PATH
from asyncio.exceptions import TimeoutError
from utils.message_builder import image

from lxml.html import fromstring
import aiohttp


def parse_html(html: str):
    selector = fromstring(html)
    for tag in selector.xpath('//div[@class="container"]/div[@class="row"]/div/div[@class="row item-box"]')[1:5]:
        if pic_url := tag.xpath('./div/img[@loading="lazy"]/@src'):  # 缩略图url
            pic_url = urljoin("https://ascii2d.net/", pic_url[0])
        if description := tag.xpath('./div/div/h6/a[1]/text()'):  # 名字
            description = description[0]
        if author := tag.xpath('./div/div/h6/a[2]/text()'):  # 作者
            author = author[0]
        if origin_url := tag.xpath('./div/div/h6/a[1]/@href'):  # 原图地址
            origin_url = origin_url[0]
        if author_url := tag.xpath('./div/div/h6/a[2]/@href'):  # 作者地址
            author_url = author_url[0]
        yield pic_url, description, author, origin_url, author_url

    pass


async def get_pic_from_url(url: str):
    real_url = "https://ascii2d.net/search/url/" + url
    async with aiohttp.ClientSession() as session:
        async with session.get(real_url) as resp:
            html: str = await resp.text()
        return [i for i in parse_html(html)]


async def get_des(url: str, user_id):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = await download_img(pic[0], user_id) + "\n"
        for i in pic[1:]:
            msg = msg + f"{i}\n"
        yield msg


async def download_img(url, user_id):
    try:
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, proxy=get_local_proxy(), timeout=7) as response:
                async with aiofiles.open(IMAGE_PATH + f'temp/{user_id}_pic_find.png', 'wb') as f:
                    await f.write(await response.read())
                    return image(f'{user_id}_pic_find.png', 'temp')
    except TimeoutError:
        return image(url)

