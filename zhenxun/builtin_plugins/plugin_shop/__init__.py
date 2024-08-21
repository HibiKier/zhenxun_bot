from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Subcommand, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from .data_source import ShopManage

__plugin_meta__ = PluginMetadata(
    name="插件商店",
    description="插件商店",
    usage="""
    插件商店        : 查看当前的插件商店
    添加插件 id     : 添加插件
    移除插件 id     : 移除插件
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)

_matcher = on_alconna(
    Alconna(
        "插件商店",
        Subcommand("add", Args["plugin_id", int]),
        Subcommand("remove", Args["plugin_id", int]),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)


_matcher.shortcut(
    r"添加插件",
    command="插件商店",
    arguments=["add", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    r"移除插件",
    command="插件商店",
    arguments=["remove", "{%0}"],
    prefix=True,
)


@_matcher.assign("$main")
async def _(session: EventSession):
    try:
        result = await ShopManage.get_plugins_info()
        logger.info("查看插件列表", "插件商店", session=session)
        await MessageUtils.build_message(result).finish()
    except Exception as e:
        logger.error(f"查看插件列表失败 e: {e}", "插件商店", session=session, e=e)


@_matcher.assign("add")
async def _(session: EventSession, plugin_id: int):
    try:
        result = await ShopManage.add_plugin(plugin_id)
    except Exception as e:
        logger.error(f"添加插件 Id: {plugin_id}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"添加插件 Id: {plugin_id} 失败 e: {e}"
        ).finish()
    logger.info(f"添加插件 Id: {plugin_id}", "插件商店", session=session)
    await MessageUtils.build_message(result).finish()


@_matcher.assign("remove")
async def _(session: EventSession, plugin_id: int):
    try:
        result = await ShopManage.remove_plugin(plugin_id)
    except Exception as e:
        logger.error(f"移除插件 Id: {plugin_id}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"移除插件 Id: {plugin_id} 失败 e: {e}"
        ).finish()
    logger.info(f"移除插件 Id: {plugin_id}", "插件商店", session=session)
    await MessageUtils.build_message(result).finish()
