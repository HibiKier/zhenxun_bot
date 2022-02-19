from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from services.log import logger
from ._data_source import get_data

__zx_plugin_name__ = "古诗"
__plugin_usage__ = """usage：
    平白无故念首诗
    示例：念诗/来首诗/念首诗
"""
__plugin_des__ = "为什么突然文艺起来了！"
__plugin_cmd__ = ["念诗/来首诗/念首诗"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["念诗", "来首诗", "念首诗"],
}

poetry = on_command("念诗", aliases={"来首诗", "念首诗"}, priority=5, block=True)


poetry_url = "https://v2.alapi.cn/api/shici"


@poetry.handle()
async def _(event: MessageEvent):
    data, code = await get_data(poetry_url)
    if code != 200:
        await poetry.finish(data, at_sender=True)
    data = data["data"]
    content = data["content"]
    title = data["origin"]
    author = data["author"]
    await poetry.send(f"{content}\n\t——{author}《{title}》")
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送古诗: f'{content}\n\t--{author}《{title}》'"
    )
