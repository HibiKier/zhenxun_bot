from utils.message_builder import image
from datetime import datetime
from pathlib import Path
# from utils.http_utils import AsyncPlaywright
from utils.browser import get_browser
from services.log import logger
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
        
    page = None
    browser = await get_browser()
    if not browser:
        logger.warning("获取 browser 失败，请部署至 linux 环境....")
        return False
    i = 1
    max = 20
    while i <= max:  # 重新尝试的次数,往往需要很多次
        try:
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_timeout(2000)
            await page.locator('//*[@id="next"]/a/button').click()
            await page.locator('.GSAlmanacs_gs_almanacs__3qT_A').screenshot(path=f"{path}/{date}.png")
            await page.close()
            return image(f"{date}.png", "genshin/alc")
        except Exception as e:
            logger.error(f"原神黄历更新出错{i}次...重新尝试中...最大尝试次数:{max} {type(e)}: {e}")
            i += 1
            if page:
                await page.close()
    return False
