# -*- coding: utf-8 -*-
import io
from copy import deepcopy

from base64 import b64encode
from typing import List, Tuple

import aiohttp
from nonebot.adapters.cqhttp import MessageSegment

header = {':authority': 'api.trace.moe',
          'accept': '*/*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'zh-CN,zh;q=0.9',
          'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary9cyjY8YBBN8SGdG4',
          'origin': 'https://trace.moe',
          'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/84.0.4147.105 Safari/537.36'}


async def parse_json(session: aiohttp.ClientSession, data: dict):
    count = 0
    for i in data["result"]:
        title: dict = i["anilist"]["title"]
        similarity = i["similarity"]
        from_ = i["from"]
        to = i["to"]
        file = i["filename"]  # 名字
        is_adult = i["anilist"]["isAdult"]
        episode = i["episode"]  # 集
        header_new = deepcopy(header)
        del header_new["content-type"]
        header_new[":method"] = 'GET'
        header_new["accept"] = "image/webp,image/apng,image/*,*/*;q=0.8"
        header_new["sec-fetch-dest"] = "image"
        header_new["sec-fetch-mode"] = "no-cors"
        async with session.get(i["image"], headers=header_new) as resp:
            pic = "base64://" + b64encode(await resp.read()).decode()
        yield pic, similarity, file, is_adult, from_, to, title, episode
        count += 1
        if count > 4:
            break


# POST https://api.trace.moe/search?cutBorders=1&anilistID=
async def get_pic_from_url(url: str):
    """
    从url搜图
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = io.BytesIO(await resp.read())
        # with open("F:\elu.PNG", "rb") as f:
        #     content = io.BytesIO(f.read())
        data = aiohttp.FormData(boundary="----WebKitFormBoundary9cyjY8YBBN8SGdG4")
        data.add_field(name="image", value=content, content_type="image/jpeg",
                       filename="blob")
        # data.add_field(name="filter", value="")
        # data.add_field(name="trial", value="0")
        async with session.post("https://api.trace.moe/search?cutBorders=1&anilistID=", data=data,
                                headers=header) as res:
            data: dict = await res.json()
            image_data = [each async for each in parse_json(session, data)]
    return image_data


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = MessageSegment.image(
            file=pic[
                0]) + f"\n相似度:{pic[1]}%\n标题:{pic[6]['native'] + ' ' + pic[6]['chinese']}\n第{pic[7]}集\nR18:{pic[3]}\n开始时间:{pic[4]}s\n结束时间{pic[5]}s"
        yield msg
    pass


if __name__ == "__main__":
    import asyncio

    data = asyncio.run(get_pic_from_url(
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1606681978562&di=6d6c90aef5ff1f9f8915bbc2e18e3c98&imgtype=0&src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fblog%2F202011%2F15%2F20201115190356_c5b95.thumb.1000_0.jpg"))
    pass
