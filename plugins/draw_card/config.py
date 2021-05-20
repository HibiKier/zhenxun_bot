import nonebot
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

# 方舟概率
PRTS_SIX_P = 0.02
PRTS_FIVE_P = 0.08
PRTS_FOUR_P = 0.48
PRTS_THREE_P = 0.42

# 原神概率
GENSHIN_FIVE_P = 0.006
GENSHIN_FOUR_P = 0.051
GENSHIN_THREE_P = 0.43
GENSHIN_G_FOUR_P = 0.13
GENSHIN_G_FIVE_P = 0.016
I72_ADD = 0.0585

# 赛马娘概率
PRETTY_THREE = 0.03
PRETTY_TWO = 0.18
PRETTY_ONE = 0.79

path_dict = {
    'genshin': '原神',
    'prts': '明日方舟',
    'pretty': '赛马娘',
}


_draw_config = Path() / "data" / "draw_card" / "draw_card_config" / "draw_card_config.json"


driver: nonebot.Driver = nonebot.get_driver()


@driver.on_startup
def check_config():
    global PRTS_SIX_P, PRTS_FOUR_P, PRTS_FIVE_P, PRTS_THREE_P, GENSHIN_G_FIVE_P, \
        GENSHIN_G_FOUR_P, GENSHIN_FOUR_P, GENSHIN_FIVE_P, I72_ADD, path_dict, PRETTY_THREE, \
        PRETTY_ONE, PRETTY_TWO, GENSHIN_THREE_P
    if _draw_config.exists():
        data = json.load(open(_draw_config, 'r', encoding='utf8'))
        PRTS_SIX_P = float(data['prts']['six'])
        PRTS_FIVE_P = float(data['prts']['five'])
        PRTS_FOUR_P = float(data['prts']['four'])
        PRTS_THREE_P = float(data['prts']['three'])

        GENSHIN_FIVE_P = float(data['genshin']['five_char'])
        GENSHIN_FOUR_P = float(data['genshin']['four_char'])
        GENSHIN_THREE_P = float(data['genshin']['three_char'])
        GENSHIN_G_FIVE_P = float(data['genshin']['five_weapon'])
        GENSHIN_G_FOUR_P = float(data['genshin']['four_weapon'])
        I72_ADD = float(data['genshin']['72_add'])

        PRETTY_THREE = float(data['pretty']['three'])
        PRETTY_TWO = float(data['pretty']['two'])
        PRETTY_ONE = float(data['pretty']['one'])

        path_dict = data['path_dict']
    else:
        _draw_config.parent.mkdir(parents=True, exist_ok=True)
        config_dict = {
            'path_dict': {
                'genshin': '原神',
                'prts': '明日方舟',
                'pretty': '赛马娘',
            },

            'prts': {
                'six': 0.02,
                'five': 0.08,
                'four': 0.48,
                'three': 0.42,
            },

            'genshin': {
                'five_char': 0.006,
                'four_char': 0.051,
                'three_char': 0.43,
                'five_weapon': 0.13,
                'four_weapon': 0.016,
                '72_add': 0.0585,
            },

            'pretty': {
                'three': 0.03,
                'two': 0.18,
                'one': 0.79,
            }
        }
        json.dump(config_dict, open(_draw_config, 'w', encoding='utf8'), indent=4, ensure_ascii=False)









