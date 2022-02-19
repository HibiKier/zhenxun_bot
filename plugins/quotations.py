from nonebot import on_command
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.http_utils import AsyncHttpx


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
    data = (await AsyncHttpx.get(url, timeout=5)).json()
    result = f'{data["hitokoto"]}\t——{data["from"]}'
    await quotations.send(result)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送语录:"
        + result
    )
