from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from utils.manager import (
    plugins2cd_manager,
    plugins2settings_manager,
    plugins2block_manager,
    group_manager,
)
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent


__zx_plugin_name__ = "重载插件配置 [Superuser]"
__plugin_usage__ = """
usage：
    重载插件配置
    指令：
        重载插件配置
""".strip()
__plugin_des__ = "重载插件配置"
__plugin_cmd__ = [
    "重载插件配置",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


reload_plugins_manager = on_command(
    "重载插件限制", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@reload_plugins_manager.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    plugins2settings_manager.reload()
    plugins2cd_manager.reload()
    plugins2block_manager.reload()
    group_manager.reload()
    await reload_plugins_manager.send("重载完成...")
