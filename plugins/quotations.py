from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import aiohttp
from utils.utils import get_local_proxy


__zx_plugin_name__ = "一言二次元语录"
__plugin_usage__ = """
usage：
    一言二次元语录
    指令：
        语录/二次元
""".strip()
__plugin_des__ = "二次元语录给你力量"
__plugin_cmd__ = ["语录/二次元"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["语录", "二次元"],
}


quotations = on_command("语录", aliases={"二次元", "二次元语录"}, priority=5, block=True)

url = "https://international.v1.hitokoto.cn/?c=a"


@quotations.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=get_local_proxy(), timeout=5) as response:
            data = await response.json()
    result = f'{data["hitokoto"]}\t——{data["from"]}'
    await quotations.send(result)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送语录:"
        + result
    )
