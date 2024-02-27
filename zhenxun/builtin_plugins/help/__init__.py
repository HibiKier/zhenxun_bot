from pathlib import Path

from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Args, Match, on_alconna
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import DATA_PATH, IMAGE_PATH
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.image_utils import BuildImage

from ._data_source import create_help_img, get_plugin_help
from ._utils import GROUP_HELP_PATH

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="帮助",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        configs=[
            RegisterConfig(
                key="type",
                value="normal",
                help="帮助图片样式 ['normal', 'HTML']",
                default_value="normal",
            )
        ],
    ).dict(),
)


SIMPLE_HELP_IMAGE = IMAGE_PATH / "SIMPLE_HELP.png"
if SIMPLE_HELP_IMAGE.exists():
    SIMPLE_HELP_IMAGE.unlink()

_matcher = on_alconna(
    Alconna(
        "功能",
        Args["name?", str],
    ),
    aliases={"help", "帮助"},
    rule=to_me(),
    priority=1,
    block=True,
)


@_matcher.handle()
async def _(
    name: Match[str],
    session: EventSession,
):
    if name.available:
        if result := await get_plugin_help(name.result):
            if isinstance(result, BuildImage):
                await Image(result.pic2bytes()).send(reply=True)
            else:
                await Text(result).send(reply=True)
        else:
            await Text("没有此功能的帮助信息...").send(reply=True)
        logger.info(
            f"查看帮助详情: {name.result}",
            "帮助",
            session=session,
        )
    else:
        if gid := session.id3 or session.id2:
            _image_path = GROUP_HELP_PATH / f"{gid}.png"
            if not _image_path.exists():
                await create_help_img(gid)
            await Image(_image_path).finish()
        else:
            if not SIMPLE_HELP_IMAGE.exists():
                if SIMPLE_HELP_IMAGE.exists():
                    SIMPLE_HELP_IMAGE.unlink()
                await create_help_img(None)
            await Image(SIMPLE_HELP_IMAGE).finish()
