from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma
from nonebot_plugin_alconna import Image as alcImg
from nonebot_plugin_alconna import Match, on_alconna
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger

from .data_source import get_anime

__plugin_meta__ = PluginMetadata(
    name="识番",
    description="以图识番",
    usage="""
    usage：
        api.trace.moe 以图识番
        指令：
            识番 [图片]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", menu_type="一些工具"
    ).dict(),
)


_matcher = on_alconna(Alconna("识番", Args["image?", alcImg]), block=True, priority=5)


@_matcher.handle()
async def _(image: Match[alcImg]):
    if image.available:
        _matcher.set_path_arg("image", image.result)


@_matcher.got_path("image", prompt="图来！")
async def _(
    session: EventSession,
    arparma: Arparma,
    image: alcImg,
):
    if not image.url:
        await Text("图片url为空...").finish()
    await Text("开始识别...").send()
    anime_data_report = await get_anime(image.url)
    if anime_data_report:
        await Text(anime_data_report).send(reply=True)
        logger.info(
            f" 识番 {image.url} --> {anime_data_report}",
            arparma.header_result,
            session=session,
        )
    else:
        logger.info(
            f"识番 {image.url} 未找到...", arparma.header_result, session=session
        )
        await Text(f"没有寻找到该番剧，果咩..").send(reply=True)
