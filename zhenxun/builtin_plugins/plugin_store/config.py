import re
from pathlib import Path

BASE_PATH = Path() / "zhenxun"
BASE_PATH.mkdir(parents=True, exist_ok=True)


DEFAULT_GITHUB_URL = "https://github.com/zhenxun-org/zhenxun_bot_plugins/tree/main"
"""伴生插件github仓库地址"""

EXTRA_GITHUB_URL = "https://github.com/zhenxun-org/zhenxun_bot_plugins_index/tree/index"
"""插件库索引github仓库地址"""

GITHUB_REPO_URL_PATTERN = re.compile(
    r"^https://github.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)(/tree/(?P<branch>[^/]+))?$"
)
"""github仓库地址正则"""

JSD_PACKAGE_API_FORMAT = (
    "https://data.jsdelivr.com/v1/packages/gh/{owner}/{repo}@{branch}"
)
"""jsdelivr包地址格式"""

GIT_API_TREES_FORMAT = (
    "https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
)
"""git api trees地址格式"""
