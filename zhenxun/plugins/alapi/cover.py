from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Image, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ._data_source import get_data

cover_url = "https://v2.alapi.cn/api/bilibili/cover"

__plugin_meta__ = PluginMetadata(
    name="b封面",
    description="快捷的b站视频封面获取方式",
    usage="""
    b封面 [链接/av/bv/cv/直播id]
    示例:b封面 av86863038
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", menu_type="一些工具"
    ).dict(),
)

_matcher = on_alconna(
    Alconna("b封面", Args["url", str]),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma, url: str):
    params = {"c": url}
    data, code = await get_data(cover_url, params)
    if code != 200 and isinstance(data, str):
        await MessageUtils.build_message(data).finish(reply_to=True)
    data = data["data"]  # type: ignore
    title = data["title"]  # type: ignore
    img = data["cover"]  # type: ignore
    await MessageUtils.build_message([f"title：{title}\n", Image(url=img)]).send(
        reply_to=True
    )
    logger.info(
        f" 获取b站封面: {title} url：{img}", arparma.header_result, session=session
    )
