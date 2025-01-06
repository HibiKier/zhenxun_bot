from zhenxun.configs.config import Config
from zhenxun.configs.path_config import IMAGE_PATH, TEMPLATE_PATH

base_config = Config.get("shop")

ICON_PATH = IMAGE_PATH / "shop_icon"


RANK_ICON_PATH = IMAGE_PATH / "_icon"

PLATFORM_PATH = {
    "dodo": RANK_ICON_PATH / "dodo.png",
    "discord": RANK_ICON_PATH / "discord.png",
    "kaiheila": RANK_ICON_PATH / "kook.png",
    "qq": RANK_ICON_PATH / "qq.png",
}

LEFT_RIGHT_IMAGE = ["1.png", "2.png", "qq.png"]

LEFT_RIGHT_PATH = TEMPLATE_PATH / "shop" / "res" / "img"
