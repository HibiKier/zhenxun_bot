from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ._data_source import get_data

url = "https://v2.alapi.cn/api/soul"

__plugin_meta__ = PluginMetadata(
    name="鸡汤",
    description="喏，亲手为你煮的鸡汤",
    usage="""
    不喝点什么感觉有点不舒服
    指令：
        鸡汤
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).dict(),
)

_matcher = on_alconna(
    Alconna("鸡汤"),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    try:
        data, code = await get_data(url)
        if code != 200 and isinstance(data, str):
            await MessageUtils.build_message(data).finish(reply_to=True)
        await MessageUtils.build_message(data["data"]["content"]).send(reply_to=True)  # type: ignore
        logger.info(
            f" 发送鸡汤:" + data["data"]["content"],  # type:ignore
            arparma.header_result,
            session=session,
        )
    except Exception as e:
        await MessageUtils.build_message("鸡汤煮坏掉了...").send()
        logger.error(f"鸡汤煮坏掉了", e=e)
