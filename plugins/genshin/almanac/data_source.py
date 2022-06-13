from utils.message_builder import image
from datetime import datetime
from pathlib import Path
from utils.http_utils import AsyncPlaywright
from nonebot.adapters.onebot.v11 import MessageSegment
from typing import Optional
import os
from services.log import logger


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
    alc_image = None
    i = 1
    max_try = 20
    while i <= max_try:
        alc_image =  await AsyncPlaywright.screenshot(
            url, path / f"{date}.png", ".GSAlmanacs_gs_almanacs__3qT_A"
        )
        if alc_image:
            return alc_image
        logger.info(f'第{i}次尝试获取黄历失败,剩余{max_try - i}次...')
        i += 1
    return alc_image
