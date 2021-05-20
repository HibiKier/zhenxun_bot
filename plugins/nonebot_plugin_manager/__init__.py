from nonebot.plugin import on_shell_command, get_loaded_plugins, export
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot, GroupMessageEvent, PrivateMessageEvent
from configs.config import plugins2name_dict
from models.ban_user import BanUser
from .data import (
    block_plugin,
    unblock_plugin,
    get_group_plugin_list,
    auto_update_plugin_list,
)
from .parser import npm_parser

# 导出给其他插件使用
export = export()
export.block_plugin = block_plugin
export.unblock_plugin = unblock_plugin
export.unblock_plugin = unblock_plugin
export.get_group_plugin_list = get_group_plugin_list

# 注册 shell_like 事件响应器
plugin_manager = on_shell_command("npm", parser=npm_parser, priority=1)


# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    plugin = matcher.module
    group_id = _get_group_id(event)
    loaded_plugin_list = _get_loaded_plugin_list()
    plugin_list = auto_update_plugin_list(loaded_plugin_list)

    # 无视本插件的 Matcher
    if plugin not in plugins2name_dict or matcher.priority in [1, 9] or await BanUser.isban(event.user_id):
        return
    try:
        if isinstance(event, PrivateMessageEvent) and plugin_list[plugin]["default"]:
            return
    except:
        pass

    # print(matcher.module)
    # print(f'plugin_list[plugin]["default"] = {plugin_list[plugin]["default"]}')
    # print(f'{matcher.module} -> this is hook')
    if not plugin_list[plugin]["default"]:
        if event.message_type == 'group':
            await bot.send_group_msg(group_id=event.group_id, message='此功能正在维护...')
        else:
            await bot.send_private_msg(user_id=event.user_id, message='此功能正在维护...')
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")
    # print(plugin_list[plugin])
    # print(group_id)
    # print(plugin_list[plugin][group_id])
    # print(not plugin_list[plugin][group_id])
    if group_id in plugin_list[plugin]:
        if not plugin_list[plugin][group_id]:
            if plugin != 'ai' and matcher.type == 'message':
                await bot.send_group_msg(group_id=event.group_id, message='该群未开启此功能..')
            raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@plugin_manager.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    group_id = _get_group_id(event)
    is_admin = _is_admin(event)
    is_superuser = _is_superuser(bot, event)
    if group_id == 0:
        group_id = 'default'

    if hasattr(args, "handle"):
        await plugin_manager.finish(args.handle(args, group_id, is_admin, is_superuser))


# 获取插件列表，并自动排除本插件
def _get_loaded_plugin_list() -> list:
    return list(
        filter(
            lambda plugin: plugin != "nonebot_plugin_manager",
            map(lambda plugin: plugin.name, get_loaded_plugins()),
        )
    )


def _get_group_id(event: Event) -> str:
    try:
        group_id = event.group_id
    except AttributeError:
        group_id = "default"
    return str(group_id) if group_id else "default"


def _is_admin(event: Event) -> bool:
    return (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )


def _is_superuser(bot: Bot, event: Event) -> bool:
    return str(event.user_id) in bot.config.superusers


plugins_dict = {

}
