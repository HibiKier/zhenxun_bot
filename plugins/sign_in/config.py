from configs.path_config import IMAGE_PATH
from pathlib import Path


SIGN_RESOURCE_PATH = Path(IMAGE_PATH) / 'sign' / 'sign_res'
SIGN_TODAY_CARD_PATH = Path(IMAGE_PATH) / 'sign' / 'today_card'
SIGN_BORDER_PATH = Path(SIGN_RESOURCE_PATH) / 'border'
SIGN_BACKGROUND_PATH = Path(SIGN_RESOURCE_PATH) / 'background'

SIGN_BORDER_PATH.mkdir(exist_ok=True, parents=True)
SIGN_BACKGROUND_PATH.mkdir(exist_ok=True, parents=True)

SIGN_CARD1_PROB = 0.2   # 好感度双倍加持卡Ⅰ
SIGN_CARD2_PROB = 0.09   # 好感度双倍加持卡Ⅱ
SIGN_CARD3_PROB = 0.05   # 好感度双倍加持卡Ⅲ

PROB_DATA = {
    SIGN_CARD3_PROB: '好感度双倍加持卡Ⅲ',
    SIGN_CARD2_PROB: '好感度双倍加持卡Ⅱ',
    SIGN_CARD1_PROB: '好感度双倍加持卡Ⅰ'
}


lik2relation = {
    '0': '路人',
    '1': '陌生',
    '2': '初识',
    '3': '普通',
    '4': '熟悉',
    '5': '信赖',
    '6': '相知',
    '7': '厚谊',
    '8': '亲密'
}

level2attitude = {
    '0': '排斥',
    '1': '警惕',
    '2': '可以交流',
    '3': '一般',
    '4': '是个好人',
    '5': '好朋友',
    '6': '可以分享小秘密',
    '7': '喜欢',
    '8': '恋人'
}

weekdays = {
    1: 'Mon',
    2: 'Tue',
    3: 'Wed',
    4: 'Thu',
    5: 'Fri',
    6: 'Sat',
    7: 'Sun'
}

lik2level = {
    9999: '9',
    400: '8',
    270: '7',
    200: '6',
    140: '5',
    90: '4',
    50: '3',
    25: '2',
    10: '1',
    0: '0'
}






