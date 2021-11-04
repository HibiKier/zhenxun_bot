from nonebot.adapters.cqhttp import MessageSegment
from utils.image_utils import CreateImg
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from typing import Optional
from configs.config import Config
import aiohttp


async def get_data(url: str, params: Optional[dict] = None) -> "Union[dict, str], int":
    """
    获取ALAPI数据
    :param url: 请求链接
    :param params: 参数
    """
    if not params:
        params = {}
    params["token"] = Config.get_config("alapi", "ALAPI_TOKEN")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=2, params=params) as response:
                data = await response.json()
                if data["code"] == 200:
                    if not data["data"]:
                        return "没有搜索到...", 997
                    return data, 200
                else:
                    return f'发生了错误...code：{data["code"]}', 999
        except TimeoutError:
            return "超时了....", 998


def gen_wbtop_pic(data: dict) -> MessageSegment:
    """
    生成微博热搜图片
    :param data: 微博热搜数据
    """
    bk = CreateImg(700, 32 * 50 + 280, 700, 32, color="#797979")
    wbtop_bk = CreateImg(700, 280, background=f"{IMAGE_PATH}/other/webtop.png")
    bk.paste(wbtop_bk)
    text_bk = CreateImg(700, 32 * 50, 700, 32, color="#797979")
    for i, data in enumerate(data):
        title = f"{i+1}. {data['hot_word']}"
        hot = data["hot_word_num"]
        img = CreateImg(700, 30, font_size=20)
        w, h = img.getsize(title)
        img.text((10, int((30 - h) / 2)), title)
        img.text((580, int((30 - h) / 2)), hot)
        text_bk.paste(img)
    bk.paste(text_bk, (0, 280))
    return image(b64=bk.pic2bs4())
