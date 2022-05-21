from nonebot.adapters.onebot.v11 import MessageSegment
from utils.image_utils import BuildImage
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from typing import Optional, Tuple, Union
from configs.config import Config
from utils.http_utils import AsyncHttpx


async def get_data(url: str, params: Optional[dict] = None) -> Tuple[Union[dict, str], int]:
    """
    获取ALAPI数据
    :param url: 请求链接
    :param params: 参数
    """
    if not params:
        params = {}
    params["token"] = Config.get_config("alapi", "ALAPI_TOKEN")
    try:
        data = (await AsyncHttpx.get(url, params=params, timeout=5)).json()
        if data["code"] == 200:
            if not data["data"]:
                return "没有搜索到...", 997
            return data, 200
        else:
            if data["code"] == 101:
                return "缺失ALAPI TOKEN，请在配置文件中填写！", 999
            return f'发生了错误...code：{data["code"]}', 999
    except TimeoutError:
        return "超时了....", 998


def gen_wbtop_pic(data: dict) -> MessageSegment:
    """
    生成微博热搜图片
    :param data: 微博热搜数据
    """
    bk = BuildImage(700, 32 * 50 + 280, 700, 32, color="#797979")
    wbtop_bk = BuildImage(700, 280, background=f"{IMAGE_PATH}/other/webtop.png")
    bk.paste(wbtop_bk)
    text_bk = BuildImage(700, 32 * 50, 700, 32, color="#797979")
    for i, data in enumerate(data):
        title = f"{i+1}. {data['hot_word']}"
        hot = data["hot_word_num"]
        img = BuildImage(700, 30, font_size=20)
        w, h = img.getsize(title)
        img.text((10, int((30 - h) / 2)), title)
        img.text((580, int((30 - h) / 2)), hot)
        text_bk.paste(img)
    bk.paste(text_bk, (0, 280))
    return image(b64=bk.pic2bs4())
