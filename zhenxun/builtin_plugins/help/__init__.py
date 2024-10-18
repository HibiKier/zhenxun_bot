from nonebot.rule import to_me
from nonebot.adapters import Bot
from nonebot_plugin_uninfo import Uninfo
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Args,
    Match,
    Query,
    Option,
    Alconna,
    AlconnaQuery,
    on_alconna,
    store_true,
)

from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.configs.utils import RegisterConfig, PluginExtraData
from zhenxun.builtin_plugins.help._config import GROUP_HELP_PATH, SIMPLE_HELP_IMAGE

from ._data_source import create_help_img, get_plugin_help

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="帮助",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.DEPENDANT,
        configs=[
            RegisterConfig(
                key="type",
                value="normal",
                help="帮助图片样式 ['normal', 'HTML', 'zhenxun']",
                default_value="zhenxun",
            )
        ],
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "功能",
        Args["name?", str],
        Option("-s|--superuser", action=store_true, help_text="超级用户帮助"),
    ),
    aliases={"help", "帮助", "菜单"},
    rule=to_me(),
    priority=1,
    block=True,
)


@_matcher.handle()
async def _(
    bot: Bot,
    name: Match[str],
    session: Uninfo,
    is_superuser: Query[bool] = AlconnaQuery("superuser.value", False),
):
    _is_superuser = is_superuser.result if is_superuser.available else False
    if name.available:
        if _is_superuser and session.user.id not in bot.config.superusers:
            _is_superuser = False
        if result := await get_plugin_help(session.user.id, name.result, _is_superuser):
            await MessageUtils.build_message(result).send(reply_to=True)
        else:
            await MessageUtils.build_message("没有此功能的帮助信息...").send(
                reply_to=True
            )
        logger.info(f"查看帮助详情: {name.result}", "帮助", session=session)
    elif session.group and (gid := session.group.id):
        _image_path = GROUP_HELP_PATH / f"{gid}.png"
        if not _image_path.exists():
            await create_help_img(session, gid)
        await MessageUtils.build_message(_image_path).finish()
    else:
        if not SIMPLE_HELP_IMAGE.exists():
            await create_help_img(session, None)
        await MessageUtils.build_message(SIMPLE_HELP_IMAGE).finish()
