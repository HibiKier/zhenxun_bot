from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from utils.manager import (
    plugins2cd_manager,
    plugins2settings_manager,
    plugins2block_manager,
    group_manager,
)
from configs.config import Config
from services.log import logger
from utils.utils import scheduler


__zx_plugin_name__ = "重载插件配置 [Superuser]"
__plugin_usage__ = """
usage：
    重载插件配置
    plugins2settings,
    plugins2cd
    plugins2block
    group_manager
    指令：
        重载插件配置
""".strip()
__plugin_des__ = "重载插件配置"
__plugin_cmd__ = [
    "重载插件配置",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_configs__ = {
    "AUTO_RELOAD": {
        "value": False,
        "help": "自动重载配置文件",
        "default_value": False
    },
    "AUTO_RELOAD_TIME": {
        "value": 180,
        "help": "控制自动重载配置文件时长",
        "default_value": 180
    }
}


reload_plugins_manager = on_command(
    "重载配置", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)


@reload_plugins_manager.handle()
async def _():
    plugins2settings_manager.reload()
    plugins2cd_manager.reload()
    plugins2block_manager.reload()
    group_manager.reload()
    Config.reload()
    await reload_plugins_manager.send("重载完成...")


@scheduler.scheduled_job(
    'interval',
    seconds=Config.get_config("reload_setting", "AUTO_RELOAD_TIME", 180),
)
async def _():
    if Config.get_config("reload_setting", "AUTO_RELOAD"):
        plugins2settings_manager.reload()
        plugins2cd_manager.reload()
        plugins2block_manager.reload()
        group_manager.reload()
        Config.reload()
        logger.debug("已自动重载所有配置文件...")
