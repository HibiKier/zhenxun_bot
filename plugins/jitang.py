from nonebot import on_command
from utils.user_agent import get_user_agent
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import aiohttp
from asyncio.exceptions import TimeoutError
from configs.config import NICKNAME

__plugin_name__ = "鸡汤"
__plugin_usage__ = f"用法： 发送’鸡汤‘，{NICKNAME}亲自为你喝鸡汤"


url = "https://v2.alapi.cn/api/soul"


jitang = on_command("鸡汤", aliases={"毒鸡汤"}, priority=5, block=True)


@jitang.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    params = {"format": "json", "token": "h0KuF6qNniMHGUtA"}
    try:
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            async with session.get(url, timeout=7, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    await jitang.send(data["data"]["content"])
                    logger.info(
                        f"(USER {event.user_id}, GROUP "
                        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                        f" 发送鸡汤:" + data["data"]["content"]
                    )
                else:
                    await jitang.send("鸡汤煮坏掉了...")
    except TimeoutError:
        await jitang.send("鸡汤煮超时了##", at_sender=True)
