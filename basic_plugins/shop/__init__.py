from pathlib import Path

import nonebot
from nonebot.drivers import Driver

from configs.config import Config
from utils.decorator.shop import shop_register

driver: Driver = nonebot.get_driver()


Config.add_plugin_config(
    "shop", "IMPORT_DEFAULT_SHOP_GOODS", True, help_="导入商店自带的三个商品", default_value=True
)


nonebot.load_plugins(str(Path(__file__).parent.resolve()))


@shop_register(
    name=("好感度双倍加持卡Ⅰ", "好感度双倍加持卡Ⅱ", "好感度双倍加持卡Ⅲ"),
    price=(30, 150, 250),
    des=(
        "下次签到双倍好感度概率 + 10%（谁才是真命天子？）（同类商品将覆盖）",
        "下次签到双倍好感度概率 + 20%（平平庸庸）（同类商品将覆盖）",
        "下次签到双倍好感度概率 + 30%（金币才是真命天子！）（同类商品将覆盖）",
    ),
    load_status=bool(Config.get_config("shop", "IMPORT_DEFAULT_SHOP_GOODS")),
    icon=(
        "favorability_card_1.png",
        "favorability_card_2.png",
        "favorability_card_3.png",
    ),
    **{"好感度双倍加持卡Ⅰ_prob": 0.1, "好感度双倍加持卡Ⅱ_prob": 0.2, "好感度双倍加持卡Ⅲ_prob": 0.3},
)
async def sign_card(user_id: int, group_id: int):
    pass


@driver.on_bot_connect
async def _():
    await shop_register.load_register()
