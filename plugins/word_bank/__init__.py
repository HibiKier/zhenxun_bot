from pathlib import Path

import nonebot

from configs.config import Config
from utils.utils import GDict

Config.add_plugin_config(
    "word_bank",
    "WORD_BANK_LEVEL [LEVEL]",
    5,
    name="词库问答",
    help_="设置增删词库的权限等级",
    default_value=5,
    type=int,
)

GDict["run_sql"].append("ALTER TABLE word_bank2 ADD to_me VARCHAR(255);")

nonebot.load_plugins(str(Path(__file__).parent.resolve()))
