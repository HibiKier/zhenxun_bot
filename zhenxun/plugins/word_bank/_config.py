from zhenxun.configs.path_config import DATA_PATH

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)

scope2int = {
    "全局": 0,
    "群聊": 1,
    "私聊": 2,
}

type2int = {
    "精准": 0,
    "模糊": 1,
    "正则": 2,
    "图片": 3,
}

int2type = {
    0: "精准",
    1: "模糊",
    2: "正则",
    3: "图片",
}
