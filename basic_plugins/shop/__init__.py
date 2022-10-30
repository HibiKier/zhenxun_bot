from configs.config import Config
from nonebot import Driver
from utils.decorator.shop import shop_register
import nonebot

driver: Driver = nonebot.get_driver()


Config.add_plugin_config(
    "shop",
    "IMPORT_DEFAULT_SHOP_GOODS",
    True,
    help_="导入商店自带的三个商品",
    default_value=True
)


nonebot.load_plugins("basic_plugins/shop")


@driver.on_bot_connect
async def _():
    await shop_register.load_register()
