from pathlib import Path

import nonebot

from zhenxun.configs.config import Config

Config.add_plugin_config(
    "word_bank",
    "WORD_BANK_LEVEL",
    5,
    help="设置增删词库的权限等级",
    default_value=5,
    type=int,
)
Config.set_name("word_bank", "词库问答")


nonebot.load_plugins(str(Path(__file__).parent.resolve()))
