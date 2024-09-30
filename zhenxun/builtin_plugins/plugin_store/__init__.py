from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import Args, Alconna, Subcommand, on_alconna

from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.configs.utils import PluginExtraData

from .data_source import ShopManage

__plugin_meta__ = PluginMetadata(
    name="插件商店",
    description="插件商店",
    usage="""
    插件商店        : 查看当前的插件商店
    添加插件 id     : 添加插件
    移除插件 id     : 移除插件
    搜索插件 name or author     : 搜索插件
    更新插件 id     : 更新插件
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
        Subcommand("search", Args["plugin_name_or_author", str]),
        Subcommand("update", Args["plugin_id", int]),
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

_matcher.shortcut(
    r"搜索插件",
    command="插件商店",
    arguments=["search", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    r"更新插件",
    command="插件商店",
    arguments=["update", "{%0}"],
    prefix=True,
)


@_matcher.assign("$main")
async def _(session: EventSession):
    try:
        result = await ShopManage.get_plugins_info()
        logger.info("查看插件列表", "插件商店", session=session)
        await MessageUtils.build_message(result).send()
    except Exception as e:
        logger.error(f"查看插件列表失败 e: {e}", "插件商店", session=session, e=e)
        await MessageUtils.build_message("获取插件列表失败...").send()


@_matcher.assign("add")
async def _(session: EventSession, plugin_id: int):
    try:
        await MessageUtils.build_message(f"正在添加插件 Id: {plugin_id}").send()
        result = await ShopManage.add_plugin(plugin_id)
    except Exception as e:
        logger.error(f"添加插件 Id: {plugin_id}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"添加插件 Id: {plugin_id} 失败 e: {e}"
        ).finish()
    logger.info(f"添加插件 Id: {plugin_id}", "插件商店", session=session)
    await MessageUtils.build_message(result).send()


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
    await MessageUtils.build_message(result).send()


@_matcher.assign("search")
async def _(session: EventSession, plugin_name_or_author: str):
    try:
        result = await ShopManage.search_plugin(plugin_name_or_author)
    except Exception as e:
        logger.error(
            f"搜索插件 name: {plugin_name_or_author}失败",
            "插件商店",
            session=session,
            e=e,
        )
        await MessageUtils.build_message(
            f"搜索插件 name: {plugin_name_or_author} 失败 e: {e}"
        ).finish()
    logger.info(f"搜索插件 name: {plugin_name_or_author}", "插件商店", session=session)
    await MessageUtils.build_message(result).send()


@_matcher.assign("update")
async def _(session: EventSession, plugin_id: int):
    try:
        await MessageUtils.build_message(f"正在更新插件 Id: {plugin_id}").send()
        result = await ShopManage.update_plugin(plugin_id)
    except Exception as e:
        logger.error(f"更新插件 Id: {plugin_id}失败", "插件商店", session=session, e=e)
        await MessageUtils.build_message(
            f"更新插件 Id: {plugin_id} 失败 e: {e}"
        ).finish()
    logger.info(f"更新插件 Id: {plugin_id}", "插件商店", session=session)
    await MessageUtils.build_message(result).send()
