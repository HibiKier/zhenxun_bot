import asyncio
import os
import time
from datetime import datetime, timedelta
from typing import List

import nonebot
from nonebot import Driver, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageEvent
from nonebot.permission import SUPERUSER

from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.browser import get_browser
from utils.image_utils import BuildImage
from utils.message_builder import image

__zx_plugin_name__ = "今日素材"
__plugin_usage__ = """
usage：
    看看原神今天要刷什么
    指令：
        今日素材/今天素材
""".strip()
__plugin_superuser_usage__ = """
usage：
    更新原神今日素材
    指令：
        更新原神今日素材
""".strip()
__plugin_des__ = "看看原神今天要刷什么"
__plugin_cmd__ = ["今日素材/今天素材", "更新原神今日素材 [_superuser]"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["今日素材", "今天素材"],
}

driver: Driver = nonebot.get_driver()

material = on_command("今日素材", aliases={"今日材料", "今天素材", "今天材料"}, priority=5, block=True)

super_cmd = on_command("更新原神今日素材", permission=SUPERUSER, priority=1, block=True)


@material.handle()
async def _(event: MessageEvent):
    if time.strftime("%w") == "0":
        await material.send("今天是周日，所有材料副本都开放了。")
        return
    file_name = str((datetime.now() - timedelta(hours=4)).date())
    if not (IMAGE_PATH / "genshin" / "material" / f"{file_name}.png").exists():
        await update_image()
    await material.send(
        Message(
            image(IMAGE_PATH / "genshin" / "material" / f"{file_name}.png")
            + "\n※ 每日素材数据来源于米游社"
        )
    )
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送查看今日素材"
    )


@super_cmd.handle()
async def _():
    if await update_image():
        await super_cmd.send("更新成功...")
        logger.info(f"更新每日天赋素材成功...")
    else:
        await super_cmd.send(f"更新失败...")


async def update_image():
    page = None
    try:
        if not os.path.exists(f"{IMAGE_PATH}/genshin/material"):
            os.mkdir(f"{IMAGE_PATH}/genshin/material")
        for file in os.listdir(f"{IMAGE_PATH}/genshin/material"):
            os.remove(f"{IMAGE_PATH}/genshin/material/{file}")
        browser = get_browser()
        if not browser:
            logger.warning("获取 browser 失败，请部署至 linux 环境....")
            return False
        # url = "https://genshin.pub/daily"
        url = "https://bbs.mihoyo.com/ys/obc/channel/map/193"
        page = await browser.new_page(viewport={"width": 860, "height": 3000})
        await page.goto(url)
        await page.wait_for_timeout(3000)
        file_name = str((datetime.now() - timedelta(hours=4)).date())
        # background_img.save(f"{IMAGE_PATH}/genshin/material/{file_name}.png")
        await page.locator(
            '//*[@id="__layout"]/div/div[2]/div[2]/div/div[1]/div[2]/div/div'
        ).screenshot(path=f"{IMAGE_PATH}/genshin/material/{file_name}.png")
        await page.close()
        return True
    except Exception as e:
        logger.error(f"原神每日素材更新出错... {type(e)}: {e}")
        if page:
            await page.close()
        return False
