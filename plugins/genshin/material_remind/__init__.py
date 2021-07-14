from nonebot import on_command, Driver
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message
from utils.init_result import image
from utils.browser import get_browser
from configs.path_config import IMAGE_PATH
import nonebot
from services.log import logger
from utils.utils import scheduler
from nonebot.permission import SUPERUSER
import os

import time

driver: Driver = nonebot.get_driver()

material = on_command('今日素材', aliases={'今日材料', '今天素材', '今天材料'}, priority=5, block=True)

super_cmd = on_command('更新原神今日素材', permission=SUPERUSER, priority=1, block=True)


@material.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if time.strftime("%w") == "0":
        await material.send("今天是周日，所有材料副本都开放了。")
        return
    await material.send(Message(image('daily_material.png', 'genshin') + '\n※ 黄历数据来源于 genshin.pub'))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 发送查看今日素材")


@super_cmd.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if await update_image():
        await super_cmd.send('更新成功...')
        logger.info(f'更新每日天赋素材成功...')
    else:
        await super_cmd.send(f'更新失败...')


@driver.on_startup
async def update_image():
    try:
        if os.path.exists(f'{IMAGE_PATH}/genshin/daily_material.png'):
            os.remove(f'{IMAGE_PATH}/genshin/daily_material.png')
        browser = await get_browser()
        if not browser:
            logger.warning('获取 browser 失败，请部署至 linux 环境....')
            return False
        url = 'https://genshin.pub/daily'
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle', timeout=10000)
        await page.set_viewport_size({"width": 2560, "height": 1080})
        await page.click("button")
        card = await page.query_selector(".GSContainer_inner_border_box__21_vs")
        card = await card.bounding_box()
        await page.screenshot(path=f'{IMAGE_PATH}/genshin/daily_material.png', clip=card, timeout=100000)
        await page.close()
        return True
    except Exception as e:
        logger.error(f'原神每日素材更新出错... {type(e)}: {e}')
        return False


@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    for _ in range(5):
        try:
            await update_image()
            logger.info(f'更新每日天赋素材成功...')
            break
        except Exception as e:
            logger.error(f'更新每日天赋素材出错 e：{e}')




