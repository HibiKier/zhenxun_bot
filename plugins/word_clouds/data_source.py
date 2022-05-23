import asyncio
import os
import random
import jieba.analyse
import re
from typing import List
from PIL import Image as IMG
import jieba
from emoji import replace_emoji  # type: ignore
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from configs.path_config import IMAGE_PATH, FONT_PATH
from services import logger
from utils.http_utils import AsyncHttpx
from models.chat_history import ChatHistory
from configs.config import Config


async def pre_precess(msg: List[str], config) -> str:
    return await asyncio.get_event_loop().run_in_executor(
        None, _pre_precess, msg, config
    )


def _pre_precess(msg: List[str], config) -> str:
    """对消息进行预处理"""
    # 过滤掉命令
    command_start = tuple([i for i in config.command_start if i])
    msg = " ".join([m for m in msg if not m.startswith(command_start)])

    # 去除网址
    msg = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", msg)

    # 去除 \u200b
    msg = re.sub(r"[\u200b]", "", msg)

    # 去除cq码
    msg = re.sub(r"\[CQ:.*?]", "", msg)

    # 去除&#91&#93
    msg = re.sub("[&#9(1|3);]", "", msg)

    # 去除 emoji
    # https://github.com/carpedm20/emoji
    msg = replace_emoji(msg)
    return msg


async def draw_word_cloud(messages, config):
    wordcloud_dir = IMAGE_PATH / "wordcloud"
    wordcloud_dir.mkdir(exist_ok=True, parents=True)
    # 默认用真寻图片
    zx_logo_path = wordcloud_dir / "default.png"
    wordcloud_ttf = FONT_PATH / "STKAITI.TTF"
    if not os.listdir(wordcloud_dir):
        url = "https://ghproxy.com/https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/resources/image/wordcloud/default.png"
        try:
            await AsyncHttpx.download_file(url, zx_logo_path)
        except Exception as e:
            logger.error(f"词云图片资源下载发生错误 {type(e)}：{e}")
            return False
    if not wordcloud_ttf.exists():
        ttf_url = "https://ghproxy.com/https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/resources/font/STKAITI.TTF"
        try:
            await AsyncHttpx.download_file(ttf_url, wordcloud_ttf)
        except Exception as e:
            logger.error(f"词云字体资源下载发生错误 {type(e)}：{e}")
            return False

    topK = min(int(len(messages)), 100000)
    read_name = jieba.analyse.extract_tags(
        await pre_precess(messages, config), topK=topK, withWeight=True, allowPOS=()
    )
    name = []
    value = []
    for t in read_name:
        name.append(t[0])
        value.append(t[1])
    for i in range(len(name)):
        name[i] = str(name[i])
    dic = dict(zip(name, value))
    if Config.get_config("word_clouds", "WORD_CLOUDS_TEMPLATE") == 1:

        def random_pic(base_path: str) -> str:
            path_dir = os.listdir(base_path)
            path = random.sample(path_dir, 1)[0]
            return str(base_path) + "/" + str(path)

        mask = np.array(IMG.open(random_pic(wordcloud_dir)))
        wc = WordCloud(
            font_path=f"{wordcloud_ttf}",
            background_color="white",
            max_font_size=100,
            width=1920,
            height=1080,
            mask=mask,
        )
        wc.generate_from_frequencies(dic)
        image_colors = ImageColorGenerator(mask, default_color=(255, 255, 255))
        wc.recolor(color_func=image_colors)
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
    else:
        wc = WordCloud(
            font_path=str(wordcloud_ttf),
            width=1920,
            height=1200,
            background_color="black",
        )
        wc.generate_from_frequencies(dic)
    bytes_io = BytesIO()
    img = wc.to_image()
    img.save(bytes_io, format="PNG")
    return bytes_io.getvalue()


async def get_list_msg(user_id, group_id, days):
    messages_list = (
        await ChatHistory()
        ._get_msg(uid=user_id, gid=group_id, type_="group", days=days)
        .gino.all()
    )
    if messages_list:
        messages = [i.text for i in messages_list]
        return messages
    else:
        return False
