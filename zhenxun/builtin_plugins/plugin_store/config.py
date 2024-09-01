import re
from pathlib import Path

BASE_PATH = Path() / "zhenxun"
BASE_PATH.mkdir(parents=True, exist_ok=True)


CONFIG_URL = "https://cdn.jsdelivr.net/gh/zhenxun-org/zhenxun_bot_plugins/plugins.json"
"""插件信息文件"""

CONFIG_INDEX_URL = "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins_index/index/plugins.json"
"""插件索引库信息文件"""

CONFIG_INDEX_CDN_URL = "https://cdn.jsdelivr.net/gh/zhenxun-org/zhenxun_bot_plugins_index@index/plugins.json"
"""插件索引库信息文件cdn"""

DEFAULT_GITHUB_URL = "https://github.com/zhenxun-org/zhenxun_bot_plugins/tree/main"

GITHUB_REPO_URL_PATTERN = re.compile(
    r"^https://github.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)(/tree/(?P<branch>[^/]+))?$"
)
"""github仓库地址正则"""

JSD_PACKAGE_API_FORMAT = (
    "https://data.jsdelivr.com/v1/packages/gh/{owner}/{repo}@{branch}"
)
"""jsdelivr包地址格式"""
