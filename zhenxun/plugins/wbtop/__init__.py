from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncPlaywright
from zhenxun.utils.message import MessageUtils

from .data_source import get_hot_image

__plugin_meta__ = PluginMetadata(
    name="微博热搜",
    description="刚买完瓜，在吃瓜现场",
    usage="""
    指令：
        微博热搜：发送实时热搜
        微博热搜 [id]：截图该热搜页面
        示例：微博热搜 5
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier & yajiwa",
        version="0.1",
    ).dict(),
)


_matcher = on_alconna(Alconna("微博热搜", Args["idx?", int]), priority=5, block=True)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma, idx: Match[int]):
    result, data_list = await get_hot_image()
    if isinstance(result, str):
        await MessageUtils.build_message(result).finish(reply_to=True)
    if idx.available:
        _idx = idx.result
        url = data_list[_idx - 1]["url"]
        file = IMAGE_PATH / "temp" / f"wbtop_{session.id1}.png"
        img = await AsyncPlaywright.screenshot(
            url,
            file,
            "#pl_feed_main",
            wait_time=12,
        )
        if img:
            await MessageUtils.build_message(file).send()
            logger.info(
                f"查询微博热搜 Id: {_idx}", arparma.header_result, session=session
            )
        else:
            await MessageUtils.build_message("获取图片失败...").send()
    else:
        await MessageUtils.build_message(result).send()
        logger.info(f"查询微博热搜", arparma.header_result, session=session)
