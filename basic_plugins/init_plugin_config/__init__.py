from .init_group_manager import init_group_manager, group_manager
from .init_plugins_config import init_plugins_config
from .init_plugins_data import init_plugins_data, plugins_manager
from .init_none_plugin_count_manager import init_none_plugin_count_manager
from .init_plugins_resources import init_plugins_resources
from .init_plugins_settings import init_plugins_settings
from .init_plugins_limit import (
    init_plugins_block_limit,
    init_plugins_count_limit,
    init_plugins_cd_limit,
)
from .init import init
from .check_plugin_status import check_plugin_status
from nonebot.adapters.onebot.v11 import Bot
from configs.path_config import DATA_PATH
from services.log import logger
from pathlib import Path
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
    _flag = False
    config_file = DATA_PATH / "configs" / "plugins2config.yaml"
    if not config_file.exists():
        _flag = True
    init()
    init_plugins_settings(DATA_PATH)
    init_plugins_cd_limit(DATA_PATH)
    init_plugins_block_limit(DATA_PATH)
    init_plugins_count_limit(DATA_PATH)
    init_plugins_data(DATA_PATH)
    init_plugins_config(DATA_PATH)
    init_plugins_resources()
    init_none_plugin_count_manager()
    x = group_manager.get_super_old_data()
    if x:
        for key in x.keys():
            plugins_manager.block_plugin(key, block_type=x[key])
    if _flag:
        raise Exception("首次运行，已在configs目录下生成配置文件config.yaml，修改后重启即可...")
    logger.info("初始化数据完成...")


@driver.on_bot_connect
async def _(bot: Bot):
    await init_group_manager()
    await check_plugin_status(bot)
