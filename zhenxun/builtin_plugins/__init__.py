import os

from nonebot import require

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_alconna")
require("nonebot_plugin_session")
require("nonebot_plugin_saa")

from nonebot_plugin_saa import enable_auto_select_bot

enable_auto_select_bot()
from pathlib import Path

import nonebot

path = Path(__file__).parent / "platform"
for d in os.listdir(path):
    nonebot.load_plugins(str((path / d).resolve()))
