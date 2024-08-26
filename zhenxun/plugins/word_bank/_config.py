from enum import Enum

from zhenxun.configs.path_config import DATA_PATH

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)


class ScopeType(Enum):
    """
    全局、群聊、私聊
    """

    GLOBAL = 0
    GROUP = 1
    PRIVATE = 2


scope2int = {
    "全局": ScopeType.GLOBAL,
    "群聊": ScopeType.GROUP,
    "私聊": ScopeType.PRIVATE,
}


class WordType(Enum):
    """
    精准、模糊、正则、图片
    """

    EXACT = 0
    FUZZY = 1
    REGEX = 2
    IMAGE = 3


type2int = {
    "精准": WordType.EXACT,
    "模糊": WordType.FUZZY,
    "正则": WordType.REGEX,
    "图片": WordType.IMAGE,
}

int2type = {
    "EXACT": "精准",
    "FUZZY": "模糊",
    "REGEX": "正则",
    "IMAGE": "图片",
}
