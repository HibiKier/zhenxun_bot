from typing import Optional
import shutil
from nonebot.log import logger
from playwright.async_api import Browser, async_playwright
import nonebot
from nonebot import Driver
from appdirs import AppDirs
from pathlib import Path
from services.log import logger


driver: Driver = nonebot.get_driver()


_browser: Optional[Browser] = None


async def init(**kwargs) -> Optional[Browser]:
    try:
        global _browser
        browser = await async_playwright().start()
        _browser = await browser.chromium.launch(**kwargs)
        return _browser
    except NotImplemented:
        logger.warning('win环境下 初始化playwright失败....请替换环境至linux')
        return None


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


@driver.on_startup
def install():
    """自动安装、更新 Chromium"""
    logger.info("正在检查 Chromium 更新")
    import sys
    from playwright.__main__ import main
    sys.argv = ['', 'install', 'chromium']
    main()


@driver.on_startup
def delete_pyppeteer():
    """删除 Pyppeteer 遗留的 Chromium"""

    dir = Path(AppDirs('pyppeteer').user_data_dir)
    if not dir.exists():
        return

    # if not config.haruka_delete_pyppeteer:
    #     logger.info("检测到 Pyppeteer 依赖（约 300 M)，"
    #                 "新版 HarukaBot 已经不需要这些文件了。"
    #                 "如果没有其他程序依赖 Pyppeteer，请在 '.env.*' 中设置"
    #                 " 'HARUKA_DELETE_PYPPETEER=True' 并重启 Bot 后，将自动清除残留")
    # else:
    shutil.rmtree(dir)
    logger.info("已清理 Pyppeteer 依赖残留")

