from pathlib import Path

BASE_PATH = Path() / "zhenxun"
BASE_PATH.mkdir(parents=True, exist_ok=True)


CONFIG_URL = "https://cdn.jsdelivr.net/gh/zhenxun-org/zhenxun_bot_plugins/plugins.json"
"""插件信息文件"""

CONFIG_INDEX_URL = "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins_index/index/plugins.json"
"""插件索引库信息文件"""

CONFIG_INDEX_CDN_URL = "https://cdn.jsdelivr.net/gh/zhenxun-org/zhenxun_bot_plugins_index@index/plugins.json"
"""插件索引库信息文件cdn"""

DOWNLOAD_URL = (
    "https://api.github.com/repos/zhenxun-org/zhenxun_bot_plugins/contents/{}?ref=main"
)
"""插件下载地址"""
