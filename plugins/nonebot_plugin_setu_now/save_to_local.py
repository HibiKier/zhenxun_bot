import os
from pathlib import Path

from anyio import open_file
from nonebot import get_driver
from nonebot.log import logger

from configs.config import Config
from .models import Setu


setu_path = Config.get_config("nonebot_plugin_setu_now", "SETU_PATH")

if not setu_path:
    setu_path = Path("./data/setu").absolute()
if os.path.exists(setu_path):
    logger.success(f"setu将保存到 {setu_path}")
else:
    os.makedirs(setu_path, exist_ok=True)
    logger.success(f"创建文件夹 {setu_path}")
    logger.info(f"setu将保存到 {setu_path}")


async def save_img(setu: Setu):
    path = Path(
        f"{setu_path}{'r18' if setu.r18 else '' }/{setu.pid}_{setu.p}_{setu.title}_{setu.author}.jpg"
    )
    async with await open_file(str(path), "wb+") as f:
        await f.write(setu.img)  # type: ignore
    logger.info(f"图片已保存 {path}")
