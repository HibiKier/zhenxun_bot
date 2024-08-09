from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ._data_source import gen_keyword_pic, get_keyword_num
from ._model.pixiv_keyword_user import PixivKeywordUser

__plugin_meta__ = PluginMetadata(
    name="查看pix图库",
    description="让我看看管理员私藏了多少货",
    usage="""
    指令：
        我的pix关键词
        显示pix关键词
        查看pix图库 ?[tag]: 查看指定tag图片数量，为空时查看整个图库
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).dict(),
)

_my_matcher = on_alconna(Alconna("我的pix关键词"), priority=5, block=True)

_show_matcher = on_alconna(Alconna("显示pix关键词"), priority=5, block=True)

_pix_matcher = on_alconna(
    Alconna("查看pix图库", Args["keyword?", str]), priority=5, block=True
)


@_my_matcher.handle()
async def _(arparma: Arparma, session: EventSession):
    data = await PixivKeywordUser.filter(user_id=session.id1).values_list(
        "keyword", flat=True
    )
    if not data:
        await MessageUtils.build_message("您目前没有提供任何Pixiv搜图关键字...").finish(
            reply_to=True
        )
    await MessageUtils.build_message(f"您目前提供的如下关键字：\n\t" + "，".join(data)).send()  # type: ignore
    logger.info("查看我的pix关键词", arparma.header_result, session=session)


@_show_matcher.handle()
async def _(bot: Bot, arparma: Arparma, session: EventSession):
    _pass_keyword, not_pass_keyword = await PixivKeywordUser.get_current_keyword()
    if _pass_keyword or not_pass_keyword:
        image = await gen_keyword_pic(
            _pass_keyword, not_pass_keyword, session.id1 in bot.config.superusers
        )
        await MessageUtils.build_message(image).send()  # type: ignore
    else:
        if session.id1 in bot.config.superusers:
            await MessageUtils.build_message(
                f"目前没有已收录或待收录的搜索关键词..."
            ).send()
        else:
            await MessageUtils.build_message(f"目前没有已收录的搜索关键词...").send()


@_pix_matcher.handle()
async def _(bot: Bot, arparma: Arparma, session: EventSession, keyword: Match[str]):
    _keyword = ""
    if keyword.available:
        _keyword = keyword.result
    count, r18_count, count_, setu_count, r18_count_ = await get_keyword_num(_keyword)
    await MessageUtils.build_message(
        f"PIX图库：{_keyword}\n"
        f"总数：{count + r18_count}\n"
        f"美图：{count}\n"
        f"R18：{r18_count}\n"
        f"---------------\n"
        f"Omega图库：{_keyword}\n"
        f"总数：{count_ + setu_count + r18_count_}\n"
        f"美图：{count_}\n"
        f"色图：{setu_count}\n"
        f"R18：{r18_count_}"
    ).send()
    logger.info("查看pix图库", arparma.header_result, session=session)
