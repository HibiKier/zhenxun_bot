from pathlib import Path

import nonebot
from nonebot.adapters import Bot

from zhenxun.models.ban_console import BanConsole
from zhenxun.models.bot_console import BotConsole
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.cache_utils import Cache
from zhenxun.utils.enum import CacheType
from zhenxun.utils.platform import PlatformUtils

nonebot.load_plugins(str(Path(__file__).parent.resolve()))


driver = nonebot.get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    """将bot已存在的群组添加群认证

    参数:
        bot: Bot
    """
    if PlatformUtils.get_platform(bot) != "qq":
        return
    logger.debug(f"更新Bot: {bot.self_id} 的群认证...")
    group_list, _ = await PlatformUtils.get_group_list(bot)
    db_group_list = await GroupConsole.all().values_list("group_id", flat=True)
    create_list = []
    update_id = []
    for group in group_list:
        if group.group_id not in db_group_list:
            group.group_flag = 1
            create_list.append(group)
        else:
            update_id.append(group.group_id)
    if create_list:
        await GroupConsole.bulk_create(create_list, 10)
    else:
        await GroupConsole.filter(group_id__in=update_id).update(group_flag=1)
    logger.debug(
        f"更新Bot: {bot.self_id} 的群认证完成，共创建 {len(create_list)} 条数据，"
        f"共修改 {len(update_id)} 条数据..."
    )


@Cache.listener(CacheType.PLUGINS)
async def _():
    data_list = await PluginInfo.get_plugins()
    return {p.module: p for p in data_list}


@Cache.getter(CacheType.PLUGINS, result_model=PluginInfo)
def _(data: dict[str, PluginInfo], module: str):
    return data.get(module, None)


@Cache.listener(CacheType.GROUPS)
async def _():
    data_list = await GroupConsole.all()
    return {p.group_id: p for p in data_list}


@Cache.getter(CacheType.GROUPS, result_model=GroupConsole)
def _(data: dict[str, GroupConsole], module: str):
    return data.get(module, None)


@Cache.listener(CacheType.BOT)
async def _():
    data_list = await BotConsole.all()
    return {p.bot_id: p for p in data_list}


@Cache.getter(CacheType.BOT, result_model=BotConsole)
def _(data: dict[str, BotConsole], module: str):
    return data.get(module, None)


@Cache.listener(CacheType.BAN)
async def _():
    return await BanConsole.all()


@Cache.getter(CacheType.BAN, result_model=list[BanConsole])
def _(data_list: list[BanConsole], user_id: str, group_id: str):
    if user_id:
        if group_id:
            return [
                data
                for data in data_list
                if data.user_id == user_id and data.group_id == group_id
            ]
        else:
            return [
                data
                for data in data_list
                if data.user_id == user_id and not data.group_id
            ]
    else:
        if group_id:
            return [
                data
                for data in data_list
                if not data.user_id and data.group_id == group_id
            ]
    return None
