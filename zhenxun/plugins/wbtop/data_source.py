from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import BuildImage

URL = "https://weibo.com/ajax/side/hotSearch"


async def get_data() -> list | str:
    """获取数据

    返回:
        list | str: 数据或消息
    """
    data_list = []
    for _ in range(3):
        try:
            response = await AsyncHttpx.get(URL, timeout=20)
            if response.status_code == 200:
                data_json = response.json()["data"]["realtime"]
                for item in data_json:
                    if "is_ad" in item:
                        """广告跳过"""
                        continue
                    data = {
                        "hot_word": item["note"],
                        "hot_word_num": str(item["num"]),
                        "url": "https://s.weibo.com/weibo?q=%23" + item["word"] + "%23",
                    }
                    data_list.append(data)
                if not data:
                    return "没有搜索到..."
                return data_list
        except Exception as e:
            logger.error("获取微博热搜错误", e=e)
    return "获取失败,请十分钟后再试..."


async def get_hot_image() -> tuple[BuildImage | str, list]:
    """构造图片

    返回:
        BuildImage | str: 热搜图片
    """
    data = await get_data()
    if isinstance(data, str):
        return data, []
    bk = BuildImage(700, 32 * 50 + 280, color="#797979")
    wbtop_bk = BuildImage(700, 280, background=f"{IMAGE_PATH}/other/webtop.png")
    await bk.paste(wbtop_bk)
    text_bk = BuildImage(700, 32 * 50, color="#797979")
    image_list = []
    for i, _data in enumerate(data):
        title = f"{i + 1}. {_data['hot_word']}"
        hot = str(_data["hot_word_num"])
        img = BuildImage(700, 30, font_size=20)
        _, h = img.getsize(title)
        await img.text((10, int((30 - h) / 2)), title)
        await img.text((580, int((30 - h) / 2)), hot)
        image_list.append(img)
    text_bk = await text_bk.auto_paste(image_list, 1, 2, 0)
    await bk.paste(text_bk, (0, 280))
    return bk, data
