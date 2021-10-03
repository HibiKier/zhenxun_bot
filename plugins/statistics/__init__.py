from pathlib import Path
from configs.path_config import DATA_PATH
import nonebot
import os

nonebot.load_plugins("plugins/statistics")

old_file1 = Path(DATA_PATH) / "_prefix_count.json"
old_file2 = Path(DATA_PATH) / "_prefix_user_count.json"
new_path = Path(DATA_PATH) / "statistics"
new_path.mkdir(parents=True, exist_ok=True)
if old_file1.exists():
    os.rename(old_file1, new_path / "_prefix_count.json")
if old_file2.exists():
    os.rename(old_file2, new_path / "_prefix_user_count.json")
