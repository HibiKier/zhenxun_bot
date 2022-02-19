from utils.message_builder import image
from datetime import datetime
from pathlib import Path
from utils.http_utils import AsyncPlaywright
from nonebot.adapters.onebot.v11 import MessageSegment
from typing import Optional
import os

url = "https://genshin.pub"


async def get_alc_image(path: Path) -> Optional[MessageSegment]:
    """
    截取黄历
    :param path: 存储路径
    """
    date = datetime.now().date()
    for file in os.listdir(path):
        if f"{date}.png" != file:
            file = path / file
            file.unlink()
    if f"{date}.png" in os.listdir(path):
        return image(f"{date}.png", "genshin/alc")
    return await AsyncPlaywright.screenshot(
        url, path / f"{date}.png", ".GSAlmanacs_gs_almanacs__3qT_A"
    )
