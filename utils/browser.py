import asyncio
from typing import Optional

from nonebot import get_driver
from nonebot.log import logger
from playwright.async_api import Browser, Playwright, async_playwright

from services.log import logger

driver = get_driver()

_playwright: Optional[Playwright] = None
_browser: Optional[Browser] = None


@driver.on_startup
async def start_browser():
    global _playwright
    global _browser
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch()


@driver.on_shutdown
async def shutdown_browser():
    if _browser:
        await _browser.close()
    if _playwright:
        _playwright.stop()


def get_browser() -> Browser:
    if not _browser:
        raise RuntimeError("playwright is not initalized")
    return _browser


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
