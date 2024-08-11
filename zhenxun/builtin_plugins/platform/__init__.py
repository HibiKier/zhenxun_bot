import os
from pathlib import Path

import nonebot

path = Path(__file__).parent

for f in os.listdir(path):
    _p = path / f
    if _p.is_dir():
        nonebot.load_plugins(str(_p.resolve()))
