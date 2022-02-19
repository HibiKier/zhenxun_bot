from typing import Optional
from nonebot.log import logger
from playwright.async_api import Browser, async_playwright
import nonebot
from nonebot import Driver
from services.log import logger
import platform


driver: Driver = nonebot.get_driver()


_browser: Optional[Browser] = None


async def init(**kwargs) -> Optional[Browser]:
    if platform.system() == "Windows":
        return None
    try:
        global _browser
        browser = await async_playwright().start()
        _browser = await browser.chromium.launch(**kwargs)
        return _browser
    except NotImplementedError:
        logger.warning("win环境下 初始化playwright失败，相关功能将被限制....")
        return None


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


# @driver.on_startup
def install():
    """自动安装、更新 Chromium"""
    logger.info("正在检查 Chromium 更新")
    import sys
    from playwright.__main__ import main

    sys.argv = ["", "install", "chromium"]
    try:
        main()
    except SystemExit:
        pass
