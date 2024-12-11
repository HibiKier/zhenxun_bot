from nonebot_plugin_alconna import AlconnaMatch, Match
from nonebot_plugin_uninfo import Uninfo

from zhenxun.builtin_plugins.superuser.bot_manage.command import bot_manage
from zhenxun.models.bot_console import BotConsole
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils


@bot_manage.assign("full_function.enable")
async def enable_full_function(
    session: Uninfo,
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if not bot_id.available:
        await MessageUtils.build_message("bot_id 不能为空").finish()

    else:
        logger.info(
            f"开启 {bot_id.result} 的所有可用插件及被动",
            "bot_manage.full_function.enable",
            session=session,
        )
        await BotConsole.enable_all(bot_id.result, "tasks")
        await BotConsole.enable_all(bot_id.result, "plugins")

        await MessageUtils.build_message(
            f"已开启 {bot_id.result} 的所有插件及被动"
        ).finish()


@bot_manage.assign("full_function.disable")
async def diasble_full_function(
    session: Uninfo,
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if not bot_id.available:
        await MessageUtils.build_message("bot_id 不能为空").finish()

    else:
        logger.info(
            f"禁用 {bot_id.result} 的所有可用插件及被动",
            "bot_manage.full_function.disable",
            session=session,
        )
        await BotConsole.disable_all(bot_id.result, "tasks")
        await BotConsole.disable_all(bot_id.result, "plugins")

        await MessageUtils.build_message(
            f"已禁用 {bot_id.result} 的所有插件及被动"
        ).finish()
