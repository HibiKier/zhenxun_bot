# -*- coding: utf-8 -*-
import asyncio
from typing import List, Tuple
import io

from urllib.parse import urljoin
from lxml.html import fromstring
import aiohttp
from nonebot.adapters.cqhttp import MessageSegment

from .formdata import FormData

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryuwjSiBcpPag4k159',
    'Cookie': 'Hm_lvt_765ecde8c11b85f1ac5f168fa6e6821f=1602471368; Hm_lpvt_765ecde8c11b85f1ac5f168fa6e6821f=1602472300',
    'Host': 'iqdb.org', 'Origin': 'http://iqdb.org', 'Referer': 'http://iqdb.org/', 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


def parse_html(html: str):
    selector = fromstring(html)
    for tag in selector.xpath('//div[@id="pages"]/div[position()>1]/table'):
        # 第一个是bestmatch
        if pic_url := tag.xpath('./tr[2]/td/a/img/@src'):
            pic_url = urljoin("http://iqdb.org/", pic_url[0])  # 缩略图
        else:
            pic_url = "没有最相似的"
        similarity = tag.xpath('./tr[last()]/td/text()')[0]  # 相似度
        href: List[str] = tag.xpath('./tr/td/a/@href')  # 第一个href
        href.extend(tag.xpath('./tr/td/span/a/@href'))  # 第二个  可能是空
        href = list(map(lambda x: "https:" + x if not x.startswith("https") else x, href))
        yield pic_url, similarity, href

    pass


async def get_pic_from_url(url: str):
    """
    返回信息元祖
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = io.BytesIO(await resp.read())
        data = FormData(boundary="----WebKitFormBoundaryuwjSiBcpPag4k159")
        data.add_field(name="MAX_FILE_SIZE", value="")
        for i in range(1, 7):
            data.add_field(name="service[]", value=str(i))
        data.add_field(name="service[]", value="11")
        data.add_field(name="service[]", value="13")
        data.add_field(name="file", value=content, content_type="application/octet-stream", filename="0.jpg")
        data.add_field(name="url", value="")
        async with session.post("http://iqdb.org/", data=data, headers=headers) as res:
            html = await res.text()
        return [i for i in parse_html(html)]
    pass


async def get_des(url: str):
    """
    返回详细简介  cq码转义
    :param url:
    :return:
    """
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = MessageSegment.image(file=pic[0]) + f"\n{pic[1]}\n"
        for i in pic[2]:
            msg = msg + f"{i}\n"
        yield msg

