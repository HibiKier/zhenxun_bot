from configs.config import Config
from services.log import logger
from .model.omega_pixiv_illusts import OmegaPixivIllusts
from pathlib import Path
from nonebot import Driver
from typing import List
from datetime import datetime
import nonebot
import asyncio
import os


__zx_plugin_name__ = "更新扩展图库Omega [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


Config.add_plugin_config(
    "hibiapi",
    "HIBIAPI",
    "https://api.obfs.dev",
    help_="如果没有自建或其他hibiapi请不要修改",
    default_value="https://api.obfs.dev",
)
Config.add_plugin_config(
    "pixiv",
    "PIXIV_NGINX_URL",
    "i.pixiv.re",
    help_="Pixiv反向代理"
)
Config.add_plugin_config(
    "pix",
    "PIX_IMAGE_SIZE",
    "master",
    name="PIX图库",
    help_="PIX图库下载的画质 可能的值：original：原图，master：缩略图（加快发送速度）",
    default_value="master"
)
Config.add_plugin_config(
    "pix",
    "SEARCH_HIBIAPI_BOOKMARKS",
    5000,
    help_="最低收藏，PIX使用HIBIAPI搜索图片时达到最低收藏才会添加至图库",
    default_value=5000
)
Config.add_plugin_config(
    "pix",
    "WITHDRAW_PIX_MESSAGE",
    (0, 1),
    help_="自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
    default_value=(0, 1)
)
Config.add_plugin_config(
    "pix",
    "PIX_OMEGA_PIXIV_RATIO",
    (10, 0),
    help_="PIX图库 与 额外图库OmegaPixivIllusts 混合搜索的比例 参1：PIX图库 参2：OmegaPixivIllusts扩展图库（没有此图库请设置为0）",
    default_value=(10, 0)
)
Config.add_plugin_config(
    "pix",
    "TIMEOUT",
    10,
    help_="下载图片超时限制（秒）",
    default_value=10
)

nonebot.load_plugins("plugins/pix_gallery")

driver: Driver = nonebot.get_driver()


@driver.on_startup
async def _init_omega_pixiv_illusts():
    omega_pixiv_illusts = None
    for file in os.listdir("."):
        if "omega_pixiv_illusts" in file and ".sql" in file:
            omega_pixiv_illusts = Path() / file
    if omega_pixiv_illusts:
        with open(omega_pixiv_illusts, "r", encoding="utf8") as f:
            lines = f.readlines()
        tasks = []
        length = len([x for x in lines if "INSERT INTO" in x.upper()])
        all_pid = await OmegaPixivIllusts.get_all_pid()
        index = 0
        logger.info("检测到OmegaPixivIllusts数据库，准备开始更新....")
        for line in lines:
            if "INSERT INTO" in line.upper():
                index += 1
                tasks.append(
                    asyncio.ensure_future(_tasks(line, all_pid, length, index))
                )
        await asyncio.gather(*tasks)
        omega_pixiv_illusts.unlink()


async def _tasks(line: str, all_pid: List[int], length: int, index: int):
    data = line.split("VALUES", maxsplit=1)[-1].strip()
    if data.startswith("("):
        data = data[1:]
    if data.endswith(");"):
        data = data[:-2]
    x = data.split(maxsplit=3)
    pid = int(x[1][:-1].strip())
    if pid in all_pid:
        logger.info(f"添加OmegaPixivIllusts图库数据已存在 ---> pid：{pid}")
        return
    uid = int(x[2][:-1].strip())
    x = x[3].split(", '")
    title = x[0].strip()[1:-1]
    tmp = x[1].split(", ")
    author = tmp[0].strip()[:-1]
    nsfw_tag = int(tmp[1])
    width = int(tmp[2])
    height = int(tmp[3])
    tags = x[2][:-1]
    url = x[3][:-1]
    if await OmegaPixivIllusts.add_image_data(
        pid,
        title,
        width,
        height,
        url,
        uid,
        author,
        nsfw_tag,
        tags,
        datetime.min,
        datetime.min,
    ):
        logger.info(
            f"成功添加OmegaPixivIllusts图库数据 pid：{pid} 本次预计存储 {length} 张，已更新第 {index} 张"
        )
    else:
        logger.info(f"添加OmegaPixivIllusts图库数据已存在 ---> pid：{pid}")
