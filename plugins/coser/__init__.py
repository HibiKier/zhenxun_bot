from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from services.log import logger
from asyncio.exceptions import TimeoutError
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
import aiohttp
import aiofiles
import re

__plugin_name__ = "coser"

__plugin_usage__ = "用法：发送‘coser’"


coser = on_command(
    "cos", aliases={"coser", "括丝", "COS", "Cos", "cOS", "coS"}, priority=5, block=True
)


url = "http://81.70.100.130/api/cosplay.php"


@coser.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    async with aiohttp.ClientSession() as session:
        try:
            for _ in range(3):
                try:
                    async with session.get(url, timeout=2) as response:
                        r = re.search(r'±img=(.*)±', await response.text())
                        if r:
                            async with session.get(r.group(1), timeout=5, verify_ssl=False) as res:
                                async with aiofiles.open(f'{IMAGE_PATH}/temp/{event.user_id}_coser.jpg', 'wb') as f:
                                    await f.write(await res.read())
                            logger.info(
                                f"(USER {event.user_id}, "
                                f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                                f" 发送COSER"
                            )
                            await coser.send(image(f'{event.user_id}_coser.jpg', 'temp'))
                            break
                except TimeoutError:
                    pass
        except Exception as e:
            await coser.send('发生了预料之外的错误..请稍后再试或联系管理员修复...')
            logger.error(f'coser 发送了未知错误 {type(e)}：{e}')

