from nonebot_plugin_alconna import AlconnaMatch, Match
from nonebot_plugin_uninfo import Uninfo

from zhenxun.builtin_plugins.superuser.bot_manage.command import bot_manage
from zhenxun.models.bot_console import BotConsole
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils


@bot_manage.assign("bot_switch.enable")
async def enable_bot_switch(
    session: Uninfo,
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if not bot_id.available:
        await MessageUtils.build_message("bot_id 不能为空").finish()

    else:
        logger.info(
            f"开启 {bot_id.result} ",
            "bot_manage.bot_switch.enable",
            session=session,
        )
        try:
            await BotConsole.set_bot_status(True, bot_id.result)
        except ValueError:
            await MessageUtils.build_message(f"bot_id {bot_id.result} 不存在").finish()

        await MessageUtils.build_message(f"已开启 {bot_id.result} ").finish()


@bot_manage.assign("bot_switch.disable")
async def diasble_bot_switch(
    session: Uninfo,
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if not bot_id.available:
        await MessageUtils.build_message("bot_id 不能为空").finish()

    else:
        logger.info(
            f"禁用 {bot_id.result} ",
            "bot_manage.bot_switch.disable",
            session=session,
        )
        try:
            await BotConsole.set_bot_status(False, bot_id.result)
        except ValueError:
            await MessageUtils.build_message(f"bot_id {bot_id.result} 不存在").finish()

        await MessageUtils.build_message(f"已禁用 {bot_id.result} ").finish()
