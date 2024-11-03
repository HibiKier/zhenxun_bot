from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_alconna import Match, Query, AlconnaMatch, AlconnaQuery

from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.models.bot_console import BotConsole
from zhenxun.builtin_plugins.superuser.bot_manage.command import bot_manage


@bot_manage.assign("plugin")
async def bot_plugin(
    session: Uninfo,
    plugin_list: Query[bool] = AlconnaQuery("plugin.list.value", default=False),
):
    if plugin_list:
        logger.info("获取全部 bot 的所有可用插件", "bot_manage.plugin", session=session)
        data = await BotConsole.get_plugins()
        for bot in data:
            await MessageUtils.build_message(f"{bot[0]} : {bot[1]}").finish()


@bot_manage.assign("plugin.enable")
async def enable_plugin(
    session: Uninfo,
    all_flag: Query[bool] = AlconnaQuery("plugin.enable.all.value", default=False),
    plugin_name: Match[str] = AlconnaMatch("plugin_name"),
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if all_flag and plugin_name.available:
        await logger.info(
            f"启用全部 bot 的 {plugin_name.result} ",
            "bot_manage.plugin.enable",
            session=session,
        )
        await BotConsole.enable_plugin(None, plugin_name.result)
        await MessageUtils.build_message(
            f"已启用全部 bot 的 {plugin_name.result} "
        ).finish()

    if bot_id.available and plugin_name.available:
        logger.info(
            f"启用 {bot_id.result} 的 {plugin_name.result}",
            "bot_manage.plugin.enable",
            session=session,
        )
        await BotConsole.enable_plugin(bot_id.result, plugin_name.result)
        await MessageUtils.build_message(
            f"已启用 {bot_id.result} 的 {plugin_name.result}"
        ).finish()

    await MessageUtils.build_message("缺失参数").finish()


@bot_manage.assign("plugin.disable")
async def disable_plugin(
    session: Uninfo,
    all_flag: Query[bool] = AlconnaQuery("plugin.disable.all.value", default=False),
    plugin_name: Match[str] = AlconnaMatch("plugin_name"),
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if all_flag and plugin_name.available:
        await logger.info(
            f"禁用全部 bot 的 {plugin_name.result} ",
            "bot_manage.plugin.disable",
            session=session,
        )
        await BotConsole.disable_plugin(None, plugin_name.result)
        await MessageUtils.build_message(
            f"已禁用全部 bot 的 {plugin_name.result} "
        ).finish()

    if bot_id.available and plugin_name.available:
        logger.info(
            f"禁用 {bot_id.result} 的 {plugin_name.result}",
            "bot_manage.plugin.disable",
            session=session,
        )
        await BotConsole.disable_plugin(bot_id.result, plugin_name.result)
        await MessageUtils.build_message(
            f"已禁用 {bot_id.result} 的 {plugin_name.result}"
        ).finish()

    await MessageUtils.build_message("缺失参数").finish()
