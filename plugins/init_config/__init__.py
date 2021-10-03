from .data_source import (
    init_plugins_settings,
    init_plugins_cd_limit,
    init_plugins_block_limit,
    init_group_manager,
)
from nonebot.adapters.cqhttp import Bot
from configs.path_config import DATA_PATH
from services.log import logger
from nonebot import Driver
import nonebot


__zx_plugin_name__ = "初始化插件数据 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


driver: Driver = nonebot.get_driver()


@driver.on_startup
def _():
    """
    初始化数据
    """
    init_plugins_settings(DATA_PATH)
    init_plugins_cd_limit(DATA_PATH)
    init_plugins_block_limit(DATA_PATH)
    logger.info("初始化数据完成...")


@driver.on_bot_connect
async def _(bot: Bot):
    await init_group_manager()

