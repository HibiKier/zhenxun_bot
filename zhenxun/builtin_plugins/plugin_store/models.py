from aiocache import cached
from strenum import StrEnum
from pydantic import BaseModel, validator

from zhenxun.utils.enum import PluginType
from zhenxun.utils.http_utils import AsyncHttpx

from .config import GITHUB_REPO_URL_PATTERN

type2name: dict[str, str] = {
    "NORMAL": "普通插件",
    "ADMIN": "管理员插件",
    "SUPERUSER": "超级用户插件",
    "ADMIN_SUPERUSER": "管理员/超级用户插件",
    "DEPENDANT": "依赖插件",
    "HIDDEN": "其他插件",
}


class StorePluginInfo(BaseModel):
    """插件信息"""

    module: str
    module_path: str
    description: str
    usage: str
    author: str
    version: str
    plugin_type: PluginType
    is_dir: bool
    github_url: str | None

    @property
    def plugin_type_name(self):
        return type2name[self.plugin_type.value]


class RepoInfo(BaseModel):
    """仓库信息"""

    owner: str
    repo: str
    branch: str | None

    @validator("branch", pre=True, always=True)
    def _set_default_branch(cls, v):
        return "main" if v is None else v

    async def get_download_url_with_path(self, path: str):
        url_format = await self.get_fastest_format()
        return url_format.format(**self.dict(), path=path)

    @classmethod
    def parse_github_url(cls, github_url: str) -> "RepoInfo":
        if matched := GITHUB_REPO_URL_PATTERN.match(github_url):
            return RepoInfo(**matched.groupdict())
        raise ValueError("github地址格式错误")

    @classmethod
    @cached()
    async def get_fastest_format(cls) -> str:
        """获取最快下载地址格式"""
        raw_format = "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        patterns: dict[str, str] = {
            (
                "https://raw.githubusercontent.com"
                "/zhenxun-org/zhenxun_bot_plugins/main"
                "/plugins.json"
            ): raw_format,
            "https://ghproxy.cc/": f"https://ghproxy.cc/{raw_format}",
            "https://mirror.ghproxy.com/": f"https://mirror.ghproxy.com/{raw_format}",
            "https://gh-proxy.com/": f"https://gh-proxy.com/{raw_format}",
            "https://cdn.jsdelivr.net/": "https://cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/{path}",
        }
        sorted_urls = await AsyncHttpx.get_fastest_mirror(list(patterns.keys()))
        if not sorted_urls:
            raise Exception("无法获取任意GitHub资源加速地址，请检查网络")
        return patterns[sorted_urls[0]]


class FileType(StrEnum):
    """文件类型"""

    FILE = "file"
    DIR = "directory"


class FileInfo(BaseModel):
    """文件信息"""

    type: FileType
    name: str
    files: list["FileInfo"] | None


class JsdPackageInfo(BaseModel):
    """jsd包信息"""

    type: str
    name: str
    version: str
    files: list[FileInfo]
