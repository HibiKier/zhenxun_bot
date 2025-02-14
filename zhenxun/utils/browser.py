import os
import sys

from nonebot import get_driver
from playwright.__main__ import main
from playwright.async_api import Browser, Playwright, async_playwright

from zhenxun.configs.config import BotConfig
from zhenxun.services.log import logger

driver = get_driver()

_playwright: Playwright | None = None
_browser: Browser | None = None


# @driver.on_startup
# async def start_browser():
#     global _playwright
#     global _browser
#     install()
#     await check_playwright_env()
#     _playwright = await async_playwright().start()
#     _browser = await _playwright.chromium.launch()


# @driver.on_shutdown
# async def shutdown_browser():
#     if _browser:
#         await _browser.close()
#     if _playwright:
#         await _playwright.stop()  # type: ignore


# def get_browser() -> Browser:
#     if not _browser:
#         raise RuntimeError("playwright is not initalized")
#     return _browser


def install():
    """自动安装、更新 Chromium"""

    def set_env_variables():
        os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = (
            "https://npmmirror.com/mirrors/playwright/"
        )
        if BotConfig.system_proxy:
            os.environ["HTTPS_PROXY"] = BotConfig.system_proxy

    def restore_env_variables():
        os.environ.pop("PLAYWRIGHT_DOWNLOAD_HOST", None)
        if BotConfig.system_proxy:
            os.environ.pop("HTTPS_PROXY", None)
        if original_proxy is not None:
            os.environ["HTTPS_PROXY"] = original_proxy

    def try_install_chromium():
        try:
            sys.argv = ["", "install", "chromium"]
            main()
        except SystemExit as e:
            return e.code == 0
        return False

    logger.info("检查 Chromium 更新")

    original_proxy = os.environ.get("HTTPS_PROXY")
    set_env_variables()

    success = try_install_chromium()

    if not success:
        logger.info("Chromium 更新失败，尝试从原始仓库下载，速度较慢")
        os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = ""
        success = try_install_chromium()

    restore_env_variables()

    if not success:
        raise RuntimeError("未知错误，Chromium 下载失败")


async def check_playwright_env():
    """检查 Playwright 依赖"""
    logger.info("检查 Playwright 依赖")
    try:
        async with async_playwright() as p:
            await p.chromium.launch()
    except Exception as e:
        raise ImportError("加载失败，Playwright 依赖不全，") from e
