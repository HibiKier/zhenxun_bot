from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import BaseBlock, PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from .data_source import from_anime_get_info

__plugin_meta__ = PluginMetadata(
    name="搜番",
    description="找不到想看的动漫吗？",
    usage="""
    搜索动漫资源
    指令：
        搜番  [番剧名称或者关键词]
        示例：搜番 刀剑神域
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="一些工具",
        limits=[BaseBlock(result="搜索还未完成，不要重复触发！")],
        configs=[
            RegisterConfig(
                key="SEARCH_ANIME_MAX_INFO",
                value=20,
                help="搜索动漫返回的最大数量",
                default_value=20,
                type=int,
            )
        ],
    ).dict(),
)

_matcher = on_alconna(Alconna("搜番", Args["name?", str]), priority=5, block=True)


@_matcher.handle()
async def _(name: Match[str]):
    if name.available:
        _matcher.set_path_arg("name", name.result)


@_matcher.got_path("name", prompt="是不是少了番名？")
async def _(session: EventSession, arparma: Arparma, name: str):
    gid = session.id3 or session.id2
    await MessageUtils.build_message(f"开始搜番 {name}...").send()
    anime_report = await from_anime_get_info(
        name,
        Config.get_config("search_anime", "SEARCH_ANIME_MAX_INFO"),
    )
    if anime_report:
        if isinstance(anime_report, str):
            await MessageUtils.build_message(anime_report).finish()
        await MessageUtils.build_message("\n\n".join(anime_report)).send()
        logger.info(
            f"搜索番剧 {name} 成功: {anime_report}",
            arparma.header_result,
            session=session,
        )
    else:
        logger.info(f"未找到番剧 {name}...")
        await MessageUtils.build_message(
            f"未找到番剧 {name}（也有可能是超时，再尝试一下？）"
        ).send()
