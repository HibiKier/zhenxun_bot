import asyncio

from nonebot_plugin_alconna import Match, AlconnaMatch

from zhenxun.utils.message import MessageUtils
from zhenxun.models.bot_console import BotConsole
from zhenxun.builtin_plugins.superuser.bot_manage.command import bot_manage


@bot_manage.assign("status.tasks")
async def handle_tasks_status(bot_id: Match[str] = AlconnaMatch("bot_id")):
    if not bot_id.available:
        await MessageUtils.build_message("bot_id 不能为空").finish()

    result = await asyncio.gather(
        BotConsole.get_tasks(bot_id.result),
        BotConsole.get_tasks(bot_id.result, False),
    )

    await MessageUtils.build_message(
        f"可用被动: {result[0]}\n禁用被动: {result[1]}"
    ).finish()


@bot_manage.assign("status.plugins")
async def handle_plugins_status(bot_id: Match[str] = AlconnaMatch("bot_id")):
    if not bot_id.available:
        await MessageUtils.build_message("bot_id 不能为空").finish()

    result = await asyncio.gather(
        BotConsole.get_plugins(bot_id.result),
        BotConsole.get_plugins(bot_id.result, False),
    )

    await MessageUtils.build_message(
        f"可用插件: {result[0]}\n禁用插件: {result[1]}"
    ).finish()
