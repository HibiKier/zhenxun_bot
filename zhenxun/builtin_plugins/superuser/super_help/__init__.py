from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.exception import EmptyError
from zhenxun.utils.message import MessageUtils

from .config import SUPERUSER_HELP_IMAGE
from .normal_help import build_help
from .zhenxun_help import build_html_help

__plugin_meta__ = PluginMetadata(
    name="超级用户帮助",
    description="超级用户帮助",
    usage="""
    超级用户帮助
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
        configs=[
            RegisterConfig(
                key="type",
                value="zhenxun",
                help="超级用户帮助样式，normal, zhenxun",
                default_value="zhenxun",
            )
        ],
    ).to_dict(),
)

_matcher = on_alconna(
    Alconna("超级用户帮助"),
    permission=SUPERUSER,
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    if not SUPERUSER_HELP_IMAGE.exists():
        try:
            if Config.get_config("admin_help", "type") == "zhenxun":
                await build_html_help()
            else:
                await build_help()
        except EmptyError:
            await MessageUtils.build_message("当前超级用户帮助为空...").finish(
                reply_to=True
            )
    await MessageUtils.build_message(SUPERUSER_HELP_IMAGE).send()
    logger.info("查看超级用户帮助", arparma.header_result, session=session)
