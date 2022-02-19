import nonebot
from nonebot.log import logger
from pydantic import BaseModel, Extra, ValidationError
from configs.path_config import IMAGE_PATH, DATA_PATH
from configs.config import Config

try:
    import ujson as json
except ModuleNotFoundError:
    import json


# 原神
class GenshinConfig(BaseModel, extra=Extra.ignore):
    GENSHIN_FIVE_P: float = 0.006
    GENSHIN_FOUR_P: float = 0.051
    GENSHIN_THREE_P: float = 0.43
    GENSHIN_G_FIVE_P: float = 0.13
    GENSHIN_G_FOUR_P: float = 0.016
    I72_ADD: float = 0.0585


# 明日方舟
class PrtsConfig(BaseModel, extra=Extra.ignore):
    PRTS_SIX_P: float = 0.02
    PRTS_FIVE_P: float = 0.08
    PRTS_FOUR_P: float = 0.48
    PRTS_THREE_P: float = 0.42


# 赛马娘
class PrettyConfig(BaseModel, extra=Extra.ignore):
    PRETTY_THREE_P: float = 0.03
    PRETTY_TWO_P: float = 0.18
    PRETTY_ONE_P: float = 0.79


# 坎公骑冠剑
class GuardianConfig(BaseModel, extra=Extra.ignore):
    GUARDIAN_THREE_CHAR_P: float = 0.0275
    GUARDIAN_TWO_CHAR_P: float = 0.19
    GUARDIAN_ONE_CHAR_P: float = 0.7825
    GUARDIAN_THREE_CHAR_UP_P: float = 0.01375
    GUARDIAN_THREE_CHAR_OTHER_P: float = 0.01375
    GUARDIAN_EXCLUSIVE_ARMS_P: float = 0.03
    GUARDIAN_FIVE_ARMS_P: float = 0.03
    GUARDIAN_FOUR_ARMS_P: float = 0.09
    GUARDIAN_THREE_ARMS_P: float = 0.27
    GUARDIAN_TWO_ARMS_P: float = 0.58
    GUARDIAN_EXCLUSIVE_ARMS_UP_P: float = 0.01
    GUARDIAN_EXCLUSIVE_ARMS_OTHER_P: float = 0.02


# 公主连结
class PcrConfig(BaseModel, extra=Extra.ignore):
    PCR_THREE_P: float = 0.025
    PCR_TWO_P: float = 0.18
    PCR_ONE_P: float = 0.795
    PCR_G_THREE_P: float = 0.025
    PCR_G_TWO_P: float = 0.975


# 碧蓝航线
class AzurConfig(BaseModel, extra=Extra.ignore):
    AZUR_FIVE_P: float = 0.012
    AZUR_FOUR_P: float = 0.07
    AZUR_THREE_P: float = 0.12
    AZUR_TWO_P: float = 0.51
    AZUR_ONE_P: float = 0.3


# 命运-冠位指定
class FgoConfig(BaseModel, extra=Extra.ignore):
    FGO_SERVANT_FIVE_P: float = 0.01
    FGO_SERVANT_FOUR_P: float = 0.03
    FGO_SERVANT_THREE_P: float = 0.4
    FGO_CARD_FIVE_P: float = 0.04
    FGO_CARD_FOUR_P: float = 0.12
    FGO_CARD_THREE_P: float = 0.4


# 阴阳师
class OnmyojiConfig(BaseModel, extra=Extra.ignore):
    ONMYOJI_SP: float = 0.0025
    ONMYOJI_SSR: float = 0.01
    ONMYOJI_SR: float = 0.2
    ONMYOJI_R: float = 0.7875


class PathDict(BaseModel, extra=Extra.ignore):
    genshin: str = "原神"
    prts: str = "明日方舟"
    pretty: str = "赛马娘"
    guardian: str = "坎公骑冠剑"
    pcr: str = "公主连结"
    azur: str = "碧蓝航线"
    fgo: str = "命运-冠位指定"
    onmyoji: str = "阴阳师"


class DrawConfig(BaseModel, extra=Extra.ignore):
    # 开关
    PRTS_FLAG: bool = Config.get_config("draw_card", "PRTS_FLAG")
    GENSHIN_FLAG: bool = Config.get_config("draw_card", "GENSHIN_FLAG")
    PRETTY_FLAG: bool = Config.get_config("draw_card", "PRETTY_FLAG")
    GUARDIAN_FLAG: bool = Config.get_config("draw_card", "GUARDIAN_FLAG")
    PCR_FLAG: bool = Config.get_config("draw_card", "PCR_FLAG")
    AZUR_FLAG: bool = Config.get_config("draw_card", "AZUR_FLAG")
    FGO_FLAG: bool = Config.get_config("draw_card", "FGO_FLAG")
    ONMYOJI_FLAG: bool = Config.get_config("draw_card", "ONMYOJI_FLAG")

    # 其他配置
    PCR_TAI: bool = Config.get_config("draw_card", "PCR_TAI")
    SEMAPHORE: int = Config.get_config("draw_card", "SEMAPHORE")

    # 路径
    path_dict: dict = {
        "genshin": "原神",
        "prts": "明日方舟",
        "pretty": "赛马娘",
        "guardian": "坎公骑冠剑",
        "pcr": "公主连结",
        "azur": "碧蓝航线",
        "fgo": "命运-冠位指定",
        "onmyoji": "阴阳师",
    }

    # 抽卡概率
    prts: PrtsConfig = PrtsConfig()
    genshin: GenshinConfig = GenshinConfig()
    pretty: PrettyConfig = PrettyConfig()
    guardian: GuardianConfig = GuardianConfig()
    pcr: PcrConfig = PcrConfig()
    azur: AzurConfig = AzurConfig()
    fgo: FgoConfig = FgoConfig()
    onmyoji: OnmyojiConfig = OnmyojiConfig()


driver = nonebot.get_driver()
global_config = driver.config
DRAW_DATA_PATH = DATA_PATH / "draw_card"
DRAW_IMAGE_PATH = IMAGE_PATH / "draw_card"
# DRAW_PATH = Path(draw_path) if draw_path else Path("data/draw_card").absolute()
config_path = DRAW_DATA_PATH / "draw_card_config" / "draw_card_config.json"

draw_config: Config = DrawConfig()


@driver.on_startup
def check_config():
    global draw_config

    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        draw_config = DrawConfig()
        logger.warning("draw_card：配置文件不存在，已重新生成配置文件.....")

    json.dump(
        draw_config.dict(),
        config_path.open("w", encoding="utf8"),
        indent=4,
        ensure_ascii=False,
    )
