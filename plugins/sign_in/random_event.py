from configs.config import MAX_SIGN_GOLD
from typing import Union
from .config import PROB_DATA
import random


def random_event(impression: float) -> 'Union[str, int], str':
    """
    签到随机事件
    :param impression: 好感度
    :return: 额外奖励 和 类型
    """
    rand = random.random() - impression / 1000
    for prob in PROB_DATA.keys():
        if rand <= prob:
            return PROB_DATA[prob], 'props'
    gold = random.randint(1, random.randint(1, int(1 if impression < 1 else impression)))
    gold = MAX_SIGN_GOLD if gold > MAX_SIGN_GOLD else gold
    return gold, 'gold'





