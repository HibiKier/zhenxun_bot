import nonebot
from pathlib import Path
from configs.path_config import DATA_PATH
from configs.config import FGO_FLAG, PCR_FLAG, AZUR_FLAG, PRTS_FLAG,\
    PRETTY_FLAG, GUARDIAN_FLAG, GENSHIN_FLAG, ONMYOJI_FLAG, PCR_TAI, SEMAPHORE
try:
    import ujson as json
except ModuleNotFoundError:
    import json


DRAW_PATH = DATA_PATH + '/draw_card/'

_draw_config = Path(rf"{DRAW_PATH}/draw_card_config/draw_card_config.json")


# 开关
PRTS_FLAG = PRTS_FLAG
GENSHIN_FLAG = GENSHIN_FLAG
PRETTY_FLAG = PRETTY_FLAG
GUARDIAN_FLAG = GUARDIAN_FLAG
PCR_FLAG = PCR_FLAG
AZUR_FLAG = AZUR_FLAG
FGO_FLAG = FGO_FLAG
ONMYOJI_FLAG = ONMYOJI_FLAG

PCR_TAI = PCR_TAI
SEMAPHORE = SEMAPHORE

# 方舟概率
PRTS_SIX_P = 0.02
PRTS_FIVE_P = 0.08
PRTS_FOUR_P = 0.48
PRTS_THREE_P = 0.42

# 原神概率
GENSHIN_FIVE_P = 0.006
GENSHIN_FOUR_P = 0.051
GENSHIN_THREE_P = 0.43
# 保底概率
GENSHIN_G_FIVE_P = 0.016
GENSHIN_G_FOUR_P = 0.13
# 72抽后增加的概率
I72_ADD = 0.0585

# 赛马娘概率
PRETTY_THREE_P = 0.03
PRETTY_TWO_P = 0.18
PRETTY_ONE_P = 0.79

# 坎公骑冠剑
# 角色概率
GUARDIAN_THREE_CHAR_P = 0.0275
GUARDIAN_TWO_CHAR_P = 0.19
GUARDIAN_ONE_CHAR_P = 0.7825
# UP角色
GUARDIAN_THREE_CHAR_UP_P = 0.01375
GUARDIAN_THREE_CHAR_OTHER_P = 0.01375
# 武器概率
GUARDIAN_EXCLUSIVE_ARMS_P = 0.03
GUARDIAN_FIVE_ARMS_P = 0.03
GUARDIAN_FOUR_ARMS_P = 0.09
GUARDIAN_THREE_ARMS_P = 0.27
GUARDIAN_TWO_ARMS_P = 0.58
# UP武器
GUARDIAN_EXCLUSIVE_ARMS_UP_P = 0.01
GUARDIAN_EXCLUSIVE_ARMS_OTHER_P = 0.02

# PCR
PCR_THREE_P = 0.025
PCR_TWO_P = 0.18
PCR_ONE_P = 0.795
# 保底
PCR_G_THREE_P = 0.025
PCR_G_TWO_P = 0.975

# 碧蓝航线
AZUR_FIVE_P = 0.012
AZUR_FOUR_P = 0.07
AZUR_THREE_P = 0.12
AZUR_TWO_P = 0.51
AZUR_ONE_P = 0.3

# FGO
FGO_SERVANT_FIVE_P = 0.01
FGO_SERVANT_FOUR_P = 0.03
FGO_SERVANT_THREE_P = 0.4
FGO_CARD_FIVE_P = 0.04
FGO_CARD_FOUR_P = 0.12
FGO_CARD_THREE_P = 0.4

# 阴阳师
ONMYOJI_SP = 0.0025
ONMYOJI_SSR = 0.01
ONMYOJI_SR = 0.2
ONMYOJI_R = 0.7875


path_dict = {
    'genshin': '原神',
    'prts': '明日方舟',
    'pretty': '赛马娘',
    'guardian': '坎公骑冠剑',
    'pcr': '公主连结',
    'azur': '碧蓝航线',
    'fgo': '命运-冠位指定',
    'onmyoji': '阴阳师',
}

driver: nonebot.Driver = nonebot.get_driver()

config_default_data = {

    'path_dict': {
        'genshin': '原神',
        'prts': '明日方舟',
        'pretty': '赛马娘',
        'guardian': '坎公骑冠剑',
        'pcr': '公主连结',
        'azur': '碧蓝航线',
        'fgo': '命运-冠位指定',
        'onmyoji': '阴阳师',
    },

    'prts': {
        'PRTS_SIX_P': 0.02,
        'PRTS_FIVE_P': 0.08,
        'PRTS_FOUR_P': 0.48,
        'PRTS_THREE_P': 0.42,
    },

    'genshin': {
        'GENSHIN_FIVE_P': 0.006,
        'GENSHIN_FOUR_P': 0.051,
        'GENSHIN_THREE_P': 0.43,
        'GENSHIN_G_FIVE_P': 0.13,
        'GENSHIN_G_FOUR_P': 0.016,
        'I72_ADD': 0.0585,
    },

    'pretty': {
        'PRETTY_THREE_P': 0.03,
        'PRETTY_TWO_P': 0.18,
        'PRETTY_ONE_P': 0.79,
    },

    'guardian': {
        'GUARDIAN_THREE_CHAR_P': 0.0275,
        'GUARDIAN_TWO_CHAR_P': 0.19,
        'GUARDIAN_ONE_CHAR_P': 0.7825,

        'GUARDIAN_THREE_CHAR_UP_P': 0.01375,
        'GUARDIAN_THREE_CHAR_OTHER_P': 0.01375,

        'GUARDIAN_EXCLUSIVE_ARMS_P': 0.03,
        'GUARDIAN_FIVE_ARMS_P': 0.03,
        'GUARDIAN_FOUR_ARMS_P': 0.09,
        'GUARDIAN_THREE_ARMS_P': 0.27,
        'GUARDIAN_TWO_ARMS_P': 0.58,

        'GUARDIAN_EXCLUSIVE_ARMS_UP_P': 0.01,
        'GUARDIAN_EXCLUSIVE_ARMS_OTHER_P': 0.02,
    },

    'pcr': {
        'PCR_THREE_P': 0.025,
        'PCR_TWO_P': 0.18,
        'PCR_ONE_P': 0.795,
    },

    'azur': {
        'AZUR_FIVE_P': 0.012,
        'AZUR_FOUR_P': 0.07,
        'AZUR_THREE_P': 0.12,
        'AZUR_TWO_P': 0.51,
        'AZUR_ONE_P': 0.3,
    },

    'fgo': {
        'FGO_SERVANT_FIVE_P': 0.01,
        'FGO_SERVANT_FOUR_P': 0.03,
        'FGO_SERVANT_THREE_P': 0.4,
        'FGO_CARD_FIVE_P': 0.04,
        'FGO_CARD_FOUR_P': 0.12,
        'FGO_CARD_THREE_P': 0.4,
    },

    'onmyoji': {
        'ONMYOJI_SP': 0.0025,
        'ONMYOJI_SSR': 0.01,
        'ONMYOJI_SR': 0.2,
        'ONMYOJI_R': 0.7875,
    }
}


@driver.on_startup
def check_config():
    global PRTS_SIX_P, PRTS_FOUR_P, PRTS_FIVE_P, PRTS_THREE_P, GENSHIN_G_FIVE_P, config_default_data, \
        GENSHIN_G_FOUR_P, GENSHIN_FOUR_P, GENSHIN_FIVE_P, I72_ADD, path_dict, PRETTY_THREE_P, \
        PRETTY_ONE_P, PRETTY_TWO_P, GENSHIN_THREE_P, GUARDIAN_THREE_CHAR_P, GUARDIAN_TWO_CHAR_P, GUARDIAN_ONE_CHAR_P, \
        GUARDIAN_THREE_CHAR_UP_P, GUARDIAN_THREE_CHAR_OTHER_P, GUARDIAN_EXCLUSIVE_ARMS_P, GUARDIAN_FIVE_ARMS_P, \
        GUARDIAN_FOUR_ARMS_P, GUARDIAN_THREE_ARMS_P, GUARDIAN_TWO_ARMS_P, GENSHIN_FLAG, PRTS_FLAG, \
        PRETTY_FLAG, GUARDIAN_FLAG, GUARDIAN_EXCLUSIVE_ARMS_UP_P, GUARDIAN_EXCLUSIVE_ARMS_OTHER_P, DRAW_PATH, \
        PCR_THREE_P, PCR_TWO_P, PCR_ONE_P, AZUR_FOUR_P, AZUR_THREE_P, AZUR_TWO_P, AZUR_ONE_P, AZUR_FIVE_P, FGO_CARD_FIVE_P,\
        FGO_CARD_FOUR_P, FGO_CARD_THREE_P, FGO_SERVANT_THREE_P, FGO_SERVANT_FOUR_P, FGO_SERVANT_FIVE_P, ONMYOJI_R, ONMYOJI_SP, \
        ONMYOJI_SSR, ONMYOJI_SR
    _draw_config.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.load(open(_draw_config, 'r', encoding='utf8'))
    except (FileNotFoundError, ValueError):
        _draw_config.parent.mkdir(parents=True, exist_ok=True)
        json.dump(config_default_data, open(_draw_config, 'w', encoding='utf8'), indent=4, ensure_ascii=False)
        print('draw_card：配置文件不存在或格式错误，已重新生成配置文件.....')
    else:

        try:
            PRTS_SIX_P = float(data['prts']['PRTS_SIX_P'])
            PRTS_FIVE_P = float(data['prts']['PRTS_FIVE_P'])
            PRTS_FOUR_P = float(data['prts']['PRTS_FOUR_P'])
            PRTS_THREE_P = float(data['prts']['PRTS_THREE_P'])
        except KeyError:
            data['prts'] = {}
            data['prts']['PRTS_SIX_P'] = config_default_data['prts']['PRTS_SIX_P']
            data['prts']['PRTS_FIVE_P'] = config_default_data['prts']['PRTS_FIVE_P']
            data['prts']['PRTS_FOUR_P'] = config_default_data['prts']['PRTS_FOUR_P']
            data['prts']['PRTS_THREE_P'] = config_default_data['prts']['PRTS_THREE_P']

        try:
            GENSHIN_FIVE_P = float(data['genshin']['GENSHIN_FIVE_P'])
            GENSHIN_FOUR_P = float(data['genshin']['GENSHIN_FOUR_P'])
            GENSHIN_THREE_P = float(data['genshin']['GENSHIN_THREE_P'])
            GENSHIN_G_FIVE_P = float(data['genshin']['GENSHIN_G_FIVE_P'])
            GENSHIN_G_FOUR_P = float(data['genshin']['GENSHIN_G_FOUR_P'])
            I72_ADD = float(data['genshin']['I72_ADD'])
        except KeyError:
            data['genshin'] = {}
            data['genshin']['GENSHIN_FIVE_P'] = config_default_data['genshin']['GENSHIN_FIVE_P']
            data['genshin']['GENSHIN_FOUR_P'] = config_default_data['genshin']['GENSHIN_FOUR_P']
            data['genshin']['GENSHIN_THREE_P'] = config_default_data['genshin']['GENSHIN_THREE_P']
            data['genshin']['GENSHIN_G_FIVE_P'] = config_default_data['genshin']['GENSHIN_G_FIVE_P']
            data['genshin']['GENSHIN_G_FOUR_P'] = config_default_data['genshin']['GENSHIN_G_FOUR_P']
            data['genshin']['I72_ADD'] = config_default_data['genshin']['I72_ADD']

        try:
            PRETTY_THREE_P = float(data['pretty']['PRETTY_THREE_P'])
            PRETTY_TWO_P = float(data['pretty']['PRETTY_TWO_P'])
            PRETTY_ONE_P = float(data['pretty']['PRETTY_ONE_P'])
        except KeyError:
            data['pretty'] = {}
            data['pretty']['PRETTY_THREE_P'] = config_default_data['pretty']['PRETTY_THREE_P']
            data['pretty']['PRETTY_TWO_P'] = config_default_data['pretty']['PRETTY_TWO_P']
            data['pretty']['PRETTY_ONE_P'] = config_default_data['pretty']['PRETTY_ONE_P']

        try:
            GUARDIAN_THREE_CHAR_P = float(data['guardian']['GUARDIAN_THREE_CHAR_P'])
            GUARDIAN_TWO_CHAR_P = float(data['guardian']['GUARDIAN_TWO_CHAR_P'])
            GUARDIAN_ONE_CHAR_P = float(data['guardian']['GUARDIAN_ONE_CHAR_P'])
            GUARDIAN_THREE_CHAR_UP_P = float(data['guardian']['GUARDIAN_THREE_CHAR_UP_P'])
            GUARDIAN_THREE_CHAR_OTHER_P = float(data['guardian']['GUARDIAN_THREE_CHAR_OTHER_P'])
            GUARDIAN_EXCLUSIVE_ARMS_P = float(data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_P'])
            GUARDIAN_FIVE_ARMS_P = float(data['guardian']['GUARDIAN_FIVE_ARMS_P'])
            GUARDIAN_FOUR_ARMS_P = float(data['guardian']['GUARDIAN_FOUR_ARMS_P'])
            GUARDIAN_THREE_ARMS_P = float(data['guardian']['GUARDIAN_THREE_ARMS_P'])
            GUARDIAN_TWO_ARMS_P = float(data['guardian']['GUARDIAN_TWO_ARMS_P'])
            GUARDIAN_EXCLUSIVE_ARMS_UP_P = float(data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_UP_P'])
            GUARDIAN_EXCLUSIVE_ARMS_OTHER_P = float(data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_OTHER_P'])
        except KeyError:
            data['guardian'] = {}
            data['guardian']['GUARDIAN_THREE_CHAR_P'] = config_default_data['guardian']['GUARDIAN_THREE_CHAR_P']
            data['guardian']['GUARDIAN_TWO_CHAR_P'] = config_default_data['guardian']['GUARDIAN_TWO_CHAR_P']
            data['guardian']['GUARDIAN_ONE_CHAR_P'] = config_default_data['guardian']['GUARDIAN_ONE_CHAR_P']
            data['guardian']['GUARDIAN_THREE_CHAR_UP_P'] = config_default_data['guardian']['GUARDIAN_THREE_CHAR_UP_P']
            data['guardian']['GUARDIAN_THREE_CHAR_OTHER_P'] = config_default_data['guardian']['GUARDIAN_THREE_CHAR_OTHER_P']
            data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_P'] = config_default_data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_P']
            data['guardian']['GUARDIAN_FIVE_ARMS_P'] = config_default_data['guardian']['GUARDIAN_FIVE_ARMS_P']
            data['guardian']['GUARDIAN_FOUR_ARMS_P'] = config_default_data['guardian']['GUARDIAN_FOUR_ARMS_P']
            data['guardian']['GUARDIAN_THREE_ARMS_P'] = config_default_data['guardian']['GUARDIAN_THREE_ARMS_P']
            data['guardian']['GUARDIAN_TWO_ARMS_P'] = config_default_data['guardian']['GUARDIAN_TWO_ARMS_P']
            data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_UP_P'] = config_default_data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_UP_P']
            data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_OTHER_P'] = config_default_data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_OTHER_P']

        try:
            PCR_THREE_P = float(data['pcr']['PCR_THREE_P'])
            PCR_TWO_P = float(data['pcr']['PCR_TWO_P'])
            PCR_ONE_P = float(data['pcr']['PCR_ONE_P'])
        except KeyError:
            data['pcr'] = {}
            data['pcr']['PCR_THREE_P'] = config_default_data['pcr']['PCR_THREE_P']
            data['pcr']['PCR_TWO_P'] = config_default_data['pcr']['PCR_TWO_P']
            data['pcr']['PCR_ONE_P'] = config_default_data['pcr']['PCR_ONE_P']

        try:
            AZUR_FIVE_P = float(data['azur']['AZUR_FIVE_P'])
            AZUR_FOUR_P = float(data['azur']['AZUR_FOUR_P'])
            AZUR_THREE_P = float(data['azur']['AZUR_THREE_P'])
            AZUR_TWO_P = float(data['azur']['AZUR_TWO_P'])
            AZUR_ONE_P = float(data['azur']['AZUR_ONE_P'])
        except KeyError:
            data['azur'] = {}
            data['azur']['AZUR_FIVE_P'] = config_default_data['azur']['AZUR_FIVE_P']
            data['azur']['AZUR_FOUR_P'] = config_default_data['azur']['AZUR_FOUR_P']
            data['azur']['AZUR_THREE_P'] = config_default_data['azur']['AZUR_THREE_P']
            data['azur']['AZUR_TWO_P'] = config_default_data['azur']['AZUR_TWO_P']
            data['azur']['AZUR_ONE_P'] = config_default_data['azur']['AZUR_ONE_P']

        try:
            FGO_SERVANT_FIVE_P = float(data['fgo']['FGO_SERVANT_FIVE_P'])
            FGO_SERVANT_FOUR_P = float(data['fgo']['FGO_SERVANT_FOUR_P'])
            FGO_SERVANT_THREE_P = float(data['fgo']['FGO_SERVANT_THREE_P'])
            FGO_CARD_FIVE_P = float(data['fgo']['FGO_CARD_FIVE_P'])
            FGO_CARD_FOUR_P = float(data['fgo']['FGO_CARD_FOUR_P'])
            FGO_CARD_THREE_P = float(data['fgo']['FGO_CARD_THREE_P'])
        except KeyError:
            data['fgo'] = {}
            data['fgo']['FGO_SERVANT_FIVE_P'] = config_default_data['fgo']['FGO_SERVANT_FIVE_P']
            data['fgo']['FGO_SERVANT_FOUR_P'] = config_default_data['fgo']['FGO_SERVANT_FOUR_P']
            data['fgo']['FGO_SERVANT_THREE_P'] = config_default_data['fgo']['FGO_SERVANT_THREE_P']
            data['fgo']['FGO_CARD_FIVE_P'] = config_default_data['fgo']['FGO_CARD_FIVE_P']
            data['fgo']['FGO_CARD_FOUR_P'] = config_default_data['fgo']['FGO_CARD_FOUR_P']
            data['fgo']['FGO_CARD_THREE_P'] = config_default_data['fgo']['FGO_CARD_THREE_P']

        try:
            ONMYOJI_SP = float(data['onmyoji']['ONMYOJI_SP'])
            ONMYOJI_SSR = float(data['onmyoji']['ONMYOJI_SSR'])
            ONMYOJI_SR = float(data['onmyoji']['ONMYOJI_SR'])
            ONMYOJI_R = float(data['onmyoji']['ONMYOJI_R'])
        except KeyError:
            data['onmyoji'] = {}
            data['onmyoji']['ONMYOJI_SP'] = config_default_data['onmyoji']['ONMYOJI_SP']
            data['onmyoji']['ONMYOJI_SSR'] = config_default_data['onmyoji']['ONMYOJI_SSR']
            data['onmyoji']['ONMYOJI_SR'] = config_default_data['onmyoji']['ONMYOJI_SR']
            data['onmyoji']['ONMYOJI_R'] = config_default_data['onmyoji']['ONMYOJI_R']

        json.dump(data, open(_draw_config, 'w', encoding='utf8'), indent=4, ensure_ascii=False)





