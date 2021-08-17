from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from configs.config import ALAPI_TOKEN
from services.log import logger
from .data_source import get_data, gen_wbtop_pic
from utils.browser import get_browser
from utils.utils import get_message_text, is_number
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
import asyncio

__plugin_name__ = '微博热搜'
__plugin_usage__ = '用法： 无'


wbtop = on_command("wbtop", aliases={'微博热搜'}, priority=5, block=True)


wbtop_url = 'https://v2.alapi.cn/api/new/wbtop'

wbtop_data = []


@wbtop.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global wbtop_data
    msg = get_message_text(event.json())
    if not wbtop_data or not msg:
        params = {
            'token': ALAPI_TOKEN
        }
        data, code = await get_data(wbtop_url, params)
        if code != 200:
            await wbtop.finish(data, at_sender=True)
        wbtop_data = data['data']
        img = await asyncio.get_event_loop().run_in_executor(None, gen_wbtop_pic, wbtop_data)
        await wbtop.send(img)
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 查询微博热搜")
    if is_number(msg) and 0 < int(msg) <= 50:
        url = wbtop_data[int(msg) - 1]['url']
        browser = await get_browser()
        page = None
        try:
            if not browser:
                logger.warning('获取 browser 失败，请部署至 linux 环境....')
                await wbtop.finish('获取 browser 对象失败...')
            page = await browser.new_page()
            await page.goto(url, wait_until='networkidle', timeout=10000)
            await page.set_viewport_size({"width": 2560, "height": 1080})
            div = await page.query_selector("#pl_feedlist_index")
            await div.screenshot(path=f'{IMAGE_PATH}/temp/webtop_{event.user_id}.png', timeout=100000)
            await page.close()
            await wbtop.send(image(f'webtop_{event.user_id}.png', 'temp'))
        except Exception as e:
            logger.error(f'微博热搜截图出错... {type(e)}: {e}')
            if page:
                await page.close()
            await wbtop.send('发生了一些错误.....')

