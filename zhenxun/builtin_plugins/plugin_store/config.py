from pathlib import Path

BASE_PATH = Path() / "zhenxun"
BASE_PATH.mkdir(parents=True, exist_ok=True)


CONFIG_URL_LIST = [
    ("https://cdn.jsdelivr.net/gh/HibiKier/zhenxun_bot_plugins/plugins.json",
     "https://api.github.com/repos/HibiKier/zhenxun_bot_plugins/contents/{}?ref=main")
]
"""插件信息文件"""

CONFIG_URL = CONFIG_URL_LIST[0][0]

DOWNLOAD_URL = CONFIG_URL_LIST[0][1]
