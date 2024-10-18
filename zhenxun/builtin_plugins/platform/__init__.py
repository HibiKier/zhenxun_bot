from pathlib import Path

import nonebot

from zhenxun.services.log import logger

path = Path(__file__).parent


try:
    from nonebot.adapters.onebot.v11 import Bot

    nonebot.load_plugins(str((path / "qq").resolve()))
except ImportError:
    logger.warning("未安装 onebot-adapter，无法加载QQ平台专用插件...")
