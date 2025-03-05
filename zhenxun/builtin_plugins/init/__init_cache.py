import time
from typing import Any

import nonebot

from zhenxun.models.ban_console import BanConsole
from zhenxun.models.bot_console import BotConsole
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.level_user import LevelUser
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.user_console import UserConsole
from zhenxun.services.cache import CacheData, CacheRoot
from zhenxun.utils.enum import CacheType

driver = nonebot.get_driver()


@driver.on_startup
async def _():
    """开启cache检测"""
    CacheRoot.start_check()


def default_cleanup_expired(cache_data: CacheData) -> list[str]:
    """默认清理过期cache方法"""
    if not cache_data.data:
        return []
    now = time.time()
    expire_key = []
    for k, t in list(cache_data.expire_data.items()):
        if t < now:
            expire_key.append(k)
            cache_data.expire_data.pop(k)
    if expire_key:
        cache_data.data = {
            k: v for k, v in cache_data.data.items() if k not in expire_key
        }
    return expire_key


def default_with_expiration(
    data: dict[str, Any], expire_data: dict[str, int], expire: int
):
    """默认更新期时间cache方法"""
    keys = {k for k in data if k not in expire_data}
    return {k: time.time() + expire for k in keys} if keys else {}


@CacheRoot.new(CacheType.PLUGINS)
async def _():
    data_list = await PluginInfo.get_plugins()
    return {p.module: p for p in data_list}


@CacheRoot.new(CacheType.PLUGINS)
async def _():
    data_list = await PluginInfo.get_plugins()
    return {p.module: p for p in data_list}


@CacheRoot.updater(CacheType.PLUGINS)
async def _(data: dict[str, PluginInfo], key: str, value: Any):
    if value:
        data[key] = value
    elif plugin := await PluginInfo.get_plugin(module=key):
        data[key] = plugin


@CacheRoot.getter(CacheType.PLUGINS, result_model=PluginInfo)
async def _(cache_data: CacheData, module: str):
    cache_data.data = cache_data.data or {}
    result = cache_data.data.get(module, None)
    if not result:
        result = await PluginInfo.get_plugin(module=module)
        if result:
            cache_data.data[module] = result
    return result


@CacheRoot.with_refresh(CacheType.PLUGINS)
async def _(data: dict[str, PluginInfo]):
    plugins = await PluginInfo.filter(module__in=data.keys(), load_status=True)
    for plugin in plugins:
        data[plugin.module] = plugin


@CacheRoot.with_expiration(CacheType.PLUGINS)
def _(data: dict[str, PluginInfo], expire_data: dict[str, int], expire: int):
    return default_with_expiration(data, expire_data, expire)


@CacheRoot.cleanup_expired(CacheType.PLUGINS)
def _(cache_data: CacheData):
    return default_cleanup_expired(cache_data)


@CacheRoot.new(CacheType.GROUPS)
async def _():
    data_list = await GroupConsole.all()
    return {p.group_id: p for p in data_list if not p.channel_id}


@CacheRoot.updater(CacheType.GROUPS)
async def _(data: dict[str, GroupConsole], key: str, value: Any):
    if value:
        data[key] = value
    elif group := await GroupConsole.get_group(group_id=key):
        data[key] = group


@CacheRoot.getter(CacheType.GROUPS, result_model=GroupConsole)
async def _(data: dict[str, GroupConsole] | None, group_id: str):
    if not data:
        data = {}
    result = data.get(group_id, None)
    if not result:
        result = await GroupConsole.get_group(group_id=group_id)
        if result:
            data[group_id] = result
    return result


@CacheRoot.with_refresh(CacheType.GROUPS)
async def _(data: dict[str, GroupConsole]):
    groups = await GroupConsole.filter(
        group_id__in=data.keys(), channel_id__isnull=True, load_status=True
    )
    for group in groups:
        data[group.group_id] = group


@CacheRoot.with_expiration(CacheType.GROUPS)
def _(data: dict[str, GroupConsole], expire_data: dict[str, int], expire: int):
    return default_with_expiration(data, expire_data, expire)


@CacheRoot.cleanup_expired(CacheType.GROUPS)
def _(cache_data: CacheData):
    return default_cleanup_expired(cache_data)


@CacheRoot.new(CacheType.BOT)
async def _():
    data_list = await BotConsole.all()
    return {p.bot_id: p for p in data_list}


@CacheRoot.updater(CacheType.BOT)
async def _(data: dict[str, BotConsole], key: str, value: Any):
    if value:
        data[key] = value
    elif bot := await BotConsole.get_or_none(bot_id=key):
        data[key] = bot


@CacheRoot.getter(CacheType.BOT, result_model=BotConsole)
async def _(data: dict[str, BotConsole] | None, bot_id: str):
    if not data:
        data = {}
    result = data.get(bot_id, None)
    if not result:
        result = await BotConsole.get_or_none(bot_id=bot_id)
        if result:
            data[bot_id] = result
    return result


@CacheRoot.with_refresh(CacheType.BOT)
async def _(data: dict[str, BotConsole]):
    bots = await BotConsole.filter(bot_id__in=data.keys())
    for bot in bots:
        data[bot.bot_id] = bot


@CacheRoot.with_expiration(CacheType.BOT)
def _(data: dict[str, BotConsole], expire_data: dict[str, int], expire: int):
    return default_with_expiration(data, expire_data, expire)


@CacheRoot.cleanup_expired(CacheType.BOT)
def _(cache_data: CacheData):
    return default_cleanup_expired(cache_data)


@CacheRoot.new(CacheType.USERS)
async def _():
    data_list = await UserConsole.all()
    return {p.user_id: p for p in data_list}


@CacheRoot.updater(CacheType.USERS)
async def _(data: dict[str, UserConsole], key: str, value: Any):
    if value:
        data[key] = value
    elif user := await UserConsole.get_user(user_id=key):
        data[key] = user


@CacheRoot.getter(CacheType.USERS, result_model=UserConsole)
async def _(cache_data: CacheData, user_id: str):
    cache_data.data = cache_data.data or {}
    result = cache_data.data.get(user_id, None)
    if not result:
        result = await UserConsole.get_user(user_id=user_id)
        if result:
            cache_data.data[user_id] = result
    return result


@CacheRoot.with_refresh(CacheType.USERS)
async def _(data: dict[str, UserConsole]):
    users = await UserConsole.filter(user_id__in=data.keys())
    for user in users:
        data[user.user_id] = user


@CacheRoot.with_expiration(CacheType.USERS)
def _(data: dict[str, UserConsole], expire_data: dict[str, int], expire: int):
    return default_with_expiration(data, expire_data, expire)


@CacheRoot.cleanup_expired(CacheType.USERS)
def _(cache_data: CacheData):
    return default_cleanup_expired(cache_data)


@CacheRoot.new(CacheType.LEVEL)
async def _():
    return await LevelUser().all()


@CacheRoot.getter(CacheType.LEVEL, result_model=list[LevelUser])
async def _(cache_data: CacheData, user_id: str, group_id: str | None = None):
    cache_data.data = cache_data.data or []
    if not group_id:
        return [
            data
            for data in cache_data.data
            if data.user_id == user_id and not data.group_id
        ]
    else:
        return [
            data
            for data in cache_data.data
            if data.user_id == user_id and data.group_id == group_id
        ]


@CacheRoot.new(CacheType.BAN)
async def _():
    return await BanConsole.all()


@CacheRoot.getter(CacheType.BAN, result_model=list[BanConsole])
def _(cache_data: CacheData, user_id: str | None, group_id: str | None = None):
    if user_id:
        return (
            [
                data
                for data in cache_data.data
                if data.user_id == user_id and data.group_id == group_id
            ]
            if group_id
            else [
                data
                for data in cache_data.data
                if data.user_id == user_id and not data.group_id
            ]
        )
    if group_id:
        return [
            data
            for data in cache_data.data
            if not data.user_id and data.group_id == group_id
        ]
    return None
