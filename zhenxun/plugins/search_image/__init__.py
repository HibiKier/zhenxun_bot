from pathlib import Path

from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma
from nonebot_plugin_alconna import Image as alcImg
from nonebot_plugin_alconna import Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

from .saucenao import get_saucenao_image

__plugin_meta__ = PluginMetadata(
    name="识图",
    description="以图搜图，看破本源",
    usage="""
    识别图片 [二次元图片]
    指令：
        识图 [图片]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="一些工具",
        configs=[
            RegisterConfig(
                key="MAX_FIND_IMAGE_COUNT",
                value=3,
                help="搜索动漫返回的最大数量",
                default_value=3,
                type=int,
            ),
            RegisterConfig(
                key="API_KEY",
                value=None,
                help="Saucenao的API_KEY，通过 https://saucenao.com/user.php?page=search-api 注册获取",
            ),
        ],
    ).dict(),
)


_matcher = on_alconna(
    Alconna("识图", Args["mode?", str]["image?", alcImg]), block=True, priority=5
)


async def get_image_info(mod: str, url: str) -> str | list[str | Path] | None:
    if mod == "saucenao":
        return await get_saucenao_image(url)


@_matcher.handle()
async def _(mode: Match[str], image: Match[alcImg]):
    if mode.available:
        _matcher.set_path_arg("mode", mode.result)
    else:
        _matcher.set_path_arg("mode", "saucenao")
    if image.available:
        _matcher.set_path_arg("image", image.result)


@_matcher.got_path("image", prompt="图来！")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    mode: str,
    image: alcImg,
):
    gid = session.id3 or session.id2
    if not image.url:
        await MessageUtils.build_message("图片url为空...").finish()
    await MessageUtils.build_message("开始处理图片...").send()
    info_list = await get_image_info(mode, image.url)
    if isinstance(info_list, str):
        await MessageUtils.build_message(info_list).finish(at_sender=True)
    if not info_list:
        await MessageUtils.build_message("未查询到...").finish()
    platform = PlatformUtils.get_platform(bot)
    if "qq" == platform and gid:
        forward = MessageUtils.template2forward(info_list[1:], bot.self_id)  # type: ignore
        await bot.send_group_forward_msg(
            group_id=int(gid),
            messages=forward,  # type: ignore
        )
    else:
        for info in info_list[1:]:
            await MessageUtils.build_message(info).send()
    logger.info(f" 识图: {image.url}", arparma.header_result, session=session)
