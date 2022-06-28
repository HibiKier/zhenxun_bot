from nonebot.adapters.onebot.v11 import MessageSegment
from utils.image_utils import BuildImage
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from typing import Tuple, Union
from utils.http_utils import AsyncHttpx
import datetime


async def get_wbtop(url: str) -> Tuple[Union[dict, str], int]:
    """
    :param url: 请求链接
    """
    n = 0
    while True:
        try:
            data = []
            get_response = (await AsyncHttpx.get(url, timeout=20))
            if get_response.status_code == 200:
                data_json = get_response.json()['data']['realtime']
                for data_item in data_json:
                    # 如果是广告，则不添加
                    if 'is_ad' in data_item:
                        continue
                    dic = {
                        'hot_word': data_item['note'],
                        'hot_word_num': str(data_item['num']),
                        'url': 'https://s.weibo.com/weibo?q=%23' + data_item['word'] + '%23',
                    }
                    data.append(dic)
                if not data:
                    return "没有搜索到...", 997
                return {'data': data, 'time': datetime.datetime.now()}, 200
            else:
                if n > 2:
                    return f'获取失败,请十分钟后再试', 999
                else:
                    n += 1
                    continue
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
        title = f"{i + 1}. {data['hot_word']}"
        hot = str(data["hot_word_num"])
        img = BuildImage(700, 30, font_size=20)
        w, h = img.getsize(title)
        img.text((10, int((30 - h) / 2)), title)
        img.text((580, int((30 - h) / 2)), hot)
        text_bk.paste(img)
    bk.paste(text_bk, (0, 280))
    return image(b64=bk.pic2bs4())
