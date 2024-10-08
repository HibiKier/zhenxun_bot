import random

from zhenxun.configs.config import Config

PROB_DATA = None


def random_event(impression: float) -> str | int:
    """签到随机事件

    参数:
        impression: 好感度

    返回:
        额外奖励 和 类型
    """
    global PROB_DATA
    if not PROB_DATA:
        PROB_DATA = {
            Config.get_config("sign_in", "SIGN_CARD3_PROB"): "好感度双倍加持卡Ⅲ",
            Config.get_config("sign_in", "SIGN_CARD2_PROB"): "好感度双倍加持卡Ⅱ",
            Config.get_config("sign_in", "SIGN_CARD1_PROB"): "好感度双倍加持卡Ⅰ",
        }
    rand = random.random() - impression / 1000
    for prob in PROB_DATA.keys():
        if rand <= prob:
            return PROB_DATA[prob]
    gold = random.randint(
        1, random.randint(1, int(1 if impression < 1 else impression))
    )
    max_sign_gold = Config.get_config("sign_in", "MAX_SIGN_GOLD")
    gold = max_sign_gold if gold > max_sign_gold else gold
    return gold
