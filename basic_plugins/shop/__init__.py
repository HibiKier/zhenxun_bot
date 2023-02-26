from pathlib import Path

import nonebot
from nonebot.drivers import Driver

from configs.config import Config
from utils.decorator.shop import shop_register

driver: Driver = nonebot.get_driver()


Config.add_plugin_config(
    "shop",
    "IMPORT_DEFAULT_SHOP_GOODS",
    True,
    help_="导入商店自带的三个商品",
    default_value=True,
    type=bool,
)


nonebot.load_plugins(str(Path(__file__).parent.resolve()))


@driver.on_bot_connect
async def _():
    await shop_register.load_register()
