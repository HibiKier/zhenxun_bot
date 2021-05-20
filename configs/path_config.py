from .utils.util import get_config_data
from pathlib import Path
from configs.config import USE_CONFIG_FILE

# 图片路径
IMAGE_PATH = Path("resources/img/")
# 音频路径
VOICE_PATH = Path("resources/voice/")
# 文本路径
TXT_PATH = Path("resources/txt/")
# 日志路径
LOG_PATH = Path("log/")
# 字体路径
TTF_PATH = Path("resources/ttf/")
# 数据路径
DATA_PATH = Path("data/")
# 抽卡数据路径
DRAW_PATH = Path("data/draw_card/")
# 临时图片路径
TEMP_PATH = Path("resources/img/temp/")


def init_path():
    global IMAGE_PATH, VOICE_PATH, TXT_PATH, LOG_PATH, TTF_PATH, DATA_PATH, DRAW_PATH, TEMP_PATH
    if USE_CONFIG_FILE:
        data = get_config_data()
        if data.get('IMAGE_PATH'):
            IMAGE_PATH = Path(data['IMAGE_PATH'])
        if data.get('VOICE_PATH'):
            VOICE_PATH = Path(data['VOICE_PATH'])
        if data.get('TXT_PATH'):
            TXT_PATH = Path(data['TXT_PATH'])
        if data.get('LOG_PATH'):
            LOG_PATH = Path(data['LOG_PATH'])
        if data.get('TTF_PATH'):
            TTF_PATH = Path(data['TTF_PATH'])
        if data.get('DATA_PATH'):
            DATA_PATH = Path(data['DATA_PATH'])
        if data.get('DRAW_PATH'):
            DRAW_PATH = Path(data['DRAW_PATH'])
        if data.get('TEMP_PATH'):
            TEMP_PATH = Path(data['TEMP_PATH'])
    IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    VOICE_PATH.mkdir(parents=True, exist_ok=True)
    TXT_PATH.mkdir(parents=True, exist_ok=True)
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    TTF_PATH.mkdir(parents=True, exist_ok=True)
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    DRAW_PATH.mkdir(parents=True, exist_ok=True)
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    IMAGE_PATH = str(IMAGE_PATH.absolute()) + '/'
    VOICE_PATH = str(VOICE_PATH.absolute()) + '/'
    TXT_PATH = str(TXT_PATH.absolute()) + '/'
    LOG_PATH = str(LOG_PATH.absolute()) + '/'
    TTF_PATH = str(TTF_PATH.absolute()) + '/'
    DATA_PATH = str(DATA_PATH.absolute()) + '/'
    DRAW_PATH = str(DRAW_PATH.absolute()) + '/'
    TEMP_PATH = str(TEMP_PATH.absolute()) + '/'


init_path()


if __name__ == '__main__':
    print(IMAGE_PATH)
