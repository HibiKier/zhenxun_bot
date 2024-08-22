from pathlib import Path

BASE_PATH = Path() / "zhenxun"
BASE_PATH.mkdir(parents=True, exist_ok=True)


CONFIG_URL = (
    "https://cdn.jsdelivr.net/gh/HibiKier/zhenxun_bot_plugins/plugins.json"
)
"""插件信息文件"""

DOWNLOAD_URL = (
    "https://api.github.com/repos/HibiKier/zhenxun_bot_plugins/contents/{}?ref=main"
)
"""插件下载地址"""
