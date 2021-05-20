# -*- coding: utf-8 -*-
from typing import List, Tuple

import nonebot
from nonebot.adapters.cqhttp import MessageSegment
from lxml.html import fromstring
import aiohttp

"""
http://yandex.com/clck/jsredir?from=yandex.com%3Bimages%2Fsearch%3Bimages%3B%3B&text=&etext=9185.K4iyzsNBG9xrJrSJCUTF4i-XPMAfmBQYR_Igss1ESRc.65568e796f3375fae39da91273ae8a1a82410929&uuid=&state=iric5OQ0sS2054x1_o8yG9mmGMT8WeQxqpuwa4Ft4KVzd9aE_Y4Dfw,,&data=eEwyM2lDYU9Gd1VROE1ZMXhZYkJTYW5fZC1TWjIzaFh5TmR1Z09fQm5DdDB3bFJSSUpVdUxfZmUzcVhfaXhTN1BCU2dINGxmdkY4NFVNcHYyUmw0emFKT2pnOWJoVmlPVzAzX1FIbWh6aXVFV3F0YWFaMGdxeGFtY2dxTzFZZl9VY1huZmlLaGVGOFZleUthZXBlM1pxUGM2elVDLXdvZEo3OGJwdVFqYmVkTDJxWElHSzFZR2NVQUhVcTdzelJwSXlrTjhlS0txdHpYY1RMMHRLOU5HSTYtT0VDb0hpdll6YjVYRXNVcUhCRFJaeDExNTQwZlhMdjh4M2YtTVFUbVJ5ZzBxMTVJcG9DNW51UWhvRzE0WjlFS19uS0VUZWhNRGxOZWlPUkFlRUUs&sign=7ba9ee25d3716868ec8464fb766c9e25&keyno=IMGS_0&b64e=2&l10n=en
"""

driver = nonebot.get_driver()
proxy: str = driver.config.proxy


def parse_html(html: str):
    selector = fromstring(html)
    for item in selector.xpath('//li[@class="other-sites__item"]'):
        pic_url = item.xpath('./a[@class="other-sites__preview-link"]/img/@src')[0].lstrip("//")  # 图床
        des = item.xpath(
            './div[@class="other-sites__snippet"]/div[@class="other-sites__snippet-title"]/a/text()')[0]  # 简介
        url = item.xpath(
            './div[@class="other-sites__snippet"]/div[@class="other-sites__snippet-site"]/a/@href')[0]  # 链接
        yield pic_url, des, url


async def get_pic_from_url(url: str):
    real_url = f"https://yandex.com/images/search?rpt=imageview&url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(real_url, proxy=proxy) as resp:
            html: str = await resp.text()
        return [i for i in parse_html(html)]


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = MessageSegment.image(file=pic[0]) + "\n"
        for i in pic[1:]:
            msg = msg + f"{i}\n"
        yield msg


if __name__ == "__main__":
    with open("yandex.html", "r", encoding="utf-8") as f:
        data = f.read()
    for item in parse_html(data):
        print(item)
