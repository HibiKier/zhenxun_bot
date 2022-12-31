import os
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Union

import ujson as json
from configs.path_config import DATA_PATH, IMAGE_PATH
from utils.image_utils import BuildImage

CONFIG_PATH = DATA_PATH / "genshin_alc" / "config.json"

ALC_PATH = IMAGE_PATH / "genshin" / "alc"

ALC_PATH.mkdir(exist_ok=True, parents=True)

BACKGROUND_PATH = ALC_PATH / "back.png"

chinese = {
    "0": "十",
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
}


@dataclass
class Fortune:
    title: str
    desc: str


def random_fortune() -> Tuple[List[Fortune], List[Fortune]]:
    """
    说明:
        随机运势
    """
    data = json.load(CONFIG_PATH.open("r", encoding="utf8"))
    fortune_data = {}
    good_fortune = []
    bad_fortune = []
    while len(fortune_data) < 6:
        r = random.choice(list(data.keys()))
        if r not in fortune_data:
            fortune_data[r] = data[r]
    for i, k in enumerate(fortune_data):
        if i < 3:
            good_fortune.append(
                Fortune(title=k, desc=random.choice(fortune_data[k]["buff"]))
            )
        else:
            bad_fortune.append(
                Fortune(title=k, desc=random.choice(fortune_data[k]["debuff"]))
            )
    return good_fortune, bad_fortune


def int2cn(v: Union[str, int]):
    """
    说明:
        数字转中文
    参数:
        :param v: str
    """
    return "".join([chinese[x] for x in str(v)])


async def build_alc_image() -> str:
    """
    说明:
        构造今日运势图片
    """
    for file in os.listdir(ALC_PATH):
        if file not in ["back.png", f"{datetime.now().date()}.png"]:
            (ALC_PATH / file).unlink()
    path = ALC_PATH / f"{datetime.now().date()}.png"
    if path.exists():
        return BuildImage(0, 0, background=path).pic2bs4()
    good_fortune, bad_fortune = random_fortune()
    background = BuildImage(
        0, 0, background=BACKGROUND_PATH, font="HYWenHei-85W.ttf", font_size=30
    )
    now = datetime.now()
    await background.atext((78, 145), str(now.year), fill="#8d7650ff")
    month = str(now.month)
    month_w = 358
    if now.month < 10:
        month_w = 373
    elif now.month != 10:
        month = "0" + month[-1]
    await background.atext((month_w, 145), f"{int2cn(month)}月", fill="#8d7650ff")
    day = str(now.day)
    if now.day > 10 and day[-1] != "0":
        day = day[0] + "0" + day[-1]
    day_str = f"{int2cn(day)}日"
    day_w = 193
    if (n := len(day_str)) == 3:
        day_w = 207
    elif n == 2:
        day_w = 228
    await background.atext(
        (day_w, 145), f"{int2cn(day)}日", fill="#f7f8f2ff", font_size=35
    )
    fortune_h = 230
    for fortune in good_fortune:
        await background.atext(
            (150, fortune_h), fortune.title, fill="#756141ff", font_size=25
        )
        await background.atext(
            (150, fortune_h + 28), fortune.desc, fill="#b5b3acff", font_size=19
        )
        fortune_h += 55
    fortune_h += 4
    for fortune in bad_fortune:
        await background.atext(
            (150, fortune_h), fortune.title, fill="#756141ff", font_size=25
        )
        await background.atext(
            (150, fortune_h + 28), fortune.desc, fill="#b5b3acff", font_size=19
        )
        fortune_h += 55
    await background.asave(path)
    return background.pic2bs4()
