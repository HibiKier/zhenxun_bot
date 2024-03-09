from nonebot import on_regex
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger

from ._data_source import get_data

comments_163 = on_regex(
    "^(网易云热评|网易云评论|到点了|12点了)$", priority=5, block=True
)


comments_163_url = "https://v2.alapi.cn/api/comment"

__plugin_meta__ = PluginMetadata(
    name="网易云热评",
    description="生了个人，我很抱歉",
    usage="""
    到点了，还是防不了下塔
    指令：
        网易云热评/到点了/12点了
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).dict(),
)

_matcher = on_alconna(
    Alconna("网易云热评"),
    priority=5,
    block=True,
)

_matcher.shortcut(
    "(到点了|12点了)",
    command="网易云热评",
    arguments=[],
    prefix=True,
)


@comments_163.handle()
async def _(session: EventSession, arparma: Arparma):
    data, code = await get_data(comments_163_url)
    if code != 200 and isinstance(data, str):
        await Text(data).finish(reply=True)
    data = data["data"]  # type: ignore
    comment = data["comment_content"]  # type: ignore
    song_name = data["title"]  # type: ignore
    await Text(f"{comment}\n\t——《{song_name}》").send(reply=True)
    logger.info(
        f" 发送网易云热评: {comment} \n\t\t————{song_name}",
        arparma.header_result,
        session=session,
    )
