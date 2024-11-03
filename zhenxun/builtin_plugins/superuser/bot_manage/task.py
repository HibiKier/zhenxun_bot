from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_alconna import Match, Query, AlconnaMatch, AlconnaQuery

from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.models.bot_console import BotConsole
from zhenxun.builtin_plugins.superuser.bot_manage.command import bot_manage


@bot_manage.assign("task")
async def bot_task(
    session: Uninfo,
    task_list: Query[bool] = AlconnaQuery("task.list.value", default=False),
):
    if task_list:
        logger.info("获取全部 bot 的所有可用被动", "bot_manage.task", session=session)
        data = await BotConsole.get_tasks()
        for bot in data:
            await MessageUtils.build_message(f"{bot[0]} : {bot[1]}").finish()


@bot_manage.assign("task.enable")
async def enable_task(
    session: Uninfo,
    all_flag: Query[bool] = AlconnaQuery("task.enable.all.value", default=False),
    task_name: Match[str] = AlconnaMatch("plugin_name"),
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if all_flag and task_name.available:
        await logger.info(
            "启用全部 bot 的所有可用被动", "bot_manage.task.enable", session=session
        )
        await BotConsole.enable_task(None, task_name.result)
        await MessageUtils.build_message("已启用全部 bot 的所有可用被动").finish()

    if bot_id.available and task_name.available:
        await logger.info(
            f"启用 {bot_id.result} 的 {task_name.result}",
            "bot_manage.task.enable",
            session=session,
        )
        await BotConsole.enable_task(bot_id.result, task_name.result)
        await MessageUtils.build_message(
            f"已启用 {bot_id.result} 的 {task_name.result}"
        ).finish()

    await MessageUtils.build_message("缺失参数").finish()


@bot_manage.assign("task.disable")
async def disable_task(
    session: Uninfo,
    all_flag: Query[bool] = AlconnaQuery("task.disable.all.value", default=False),
    task_name: Match[str] = AlconnaMatch("plugin_name"),
    bot_id: Match[str] = AlconnaMatch("bot_id"),
):
    if all_flag and task_name.available:
        await logger.info(
            "禁用全部 bot 的所有可用被动", "bot_manage.task.disable", session=session
        )
        await BotConsole.disable_task(None, task_name.result)
        await MessageUtils.build_message("已禁用全部 bot 的所有可用被动").finish()

    if bot_id.available and task_name.available:
        logger.info(
            f"禁用 {bot_id.result} 的 {task_name.result}",
            "bot_manage.task.disable",
            session=session,
        )
        await BotConsole.disable_task(bot_id.result, task_name.result)
        await MessageUtils.build_message(
            f"已禁用 {bot_id.result} 的 {task_name.result}"
        ).finish()

    await MessageUtils.build_message("缺失参数").finish()
