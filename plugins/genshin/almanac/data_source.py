from utils.browser import get_browser
from utils.message_builder import image
from datetime import datetime
from services.log import logger
from pathlib import Path
import os

url = "https://genshin.pub"


async def get_alc_image(path: Path):
    date = datetime.now().date()
    for file in os.listdir(path):
        if f'{date}.png' != file:
            file = path / file
            file.unlink()
    if f'{date}.png' in os.listdir(path):
        return image(f'{date}.png', 'genshin/alc')
    page = None
    try:
        browser = await get_browser()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle", timeout=10000)
        await page.set_viewport_size({"width": 2560, "height": 1080})
        card = await page.query_selector('.GSAlmanacs_gs_almanacs__3qT_A')
        await card.screenshot(path=path / f'{date}.png', timeout=100000)
    except Exception as e:
        logger.error(f'获取原神黄历发生错误..{type(e)}: {e}')
    finally:
        if page:
            await page.close()
    return image(f'{date}.png', 'genshin/alc')











