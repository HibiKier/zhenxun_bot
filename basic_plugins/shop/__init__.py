import nonebot
from configs.config import Config


Config.add_plugin_config(
    "shop",
    "IMPORT_DEFAULT_SHOP_GOODS",
    True,
    help_="导入商店自带的三个商品",
    default_value=True
)


nonebot.load_plugins("basic_plugins/shop")
