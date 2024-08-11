from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ._data_source import get_data

__plugin_meta__ = PluginMetadata(
    name="古诗",
    description="为什么突然文艺起来了！",
    usage="""
    平白无故念首诗
    示例：念诗/来首诗/念首诗
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).dict(),
)

_matcher = on_alconna(
    Alconna("念诗"),
    priority=5,
    block=True,
)

_matcher.shortcut(
    "(来首诗|念首诗)",
    command="念诗",
    arguments=[],
    prefix=True,
)


poetry_url = "https://v2.alapi.cn/api/shici"


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    data, code = await get_data(poetry_url)
    if code != 200 and isinstance(data, str):
        await MessageUtils.build_message(data).finish(reply_to=True)
    data = data["data"]  # type: ignore
    content = data["content"]  # type: ignore
    title = data["origin"]  # type: ignore
    author = data["author"]  # type: ignore
    await MessageUtils.build_message(f"{content}\n\t——{author}《{title}》").send(
        reply_to=True
    )
    logger.info(
        f" 发送古诗: f'{content}\n\t--{author}《{title}》'",
        arparma.header_result,
        session=session,
    )
