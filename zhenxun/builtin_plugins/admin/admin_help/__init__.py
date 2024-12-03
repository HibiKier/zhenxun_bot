from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna

from zhenxun.services.log import logger
from zhenxun.configs.config import Config
from zhenxun.utils.enum import PluginType
from zhenxun.utils.exception import EmptyError
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.rules import admin_check, ensure_group
from zhenxun.configs.utils import RegisterConfig, PluginExtraData

from .normal_help import build_help
from .config import ADMIN_HELP_IMAGE
from .html_help import build_html_help

__plugin_meta__ = PluginMetadata(
    name="群组管理员帮助",
    description="管理员帮助列表",
    usage="""
    管理员帮助
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=1,
        configs=[
            RegisterConfig(
                key="type",
                value="zhenxun",
                help="管理员帮助样式，normal, zhenxun",
                default_value="zhenxun",
            )
        ],
    ).dict(),
)

_matcher = on_alconna(
    Alconna("管理员帮助"),
    rule=admin_check(1) & ensure_group,
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(
    session: EventSession,
    arparma: Arparma,
):
    if not ADMIN_HELP_IMAGE.exists():
        try:
            if Config.get_config("admin_help", "type") == "zhenxun":
                await build_html_help()
            else:
                await build_help()
        except EmptyError:
            await MessageUtils.build_message("当前管理员帮助为空...").finish(
                reply_to=True
            )
    await MessageUtils.build_message(ADMIN_HELP_IMAGE).send()
    logger.info("查看管理员帮助", arparma.header_result, session=session)
