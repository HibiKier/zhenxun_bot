from enum import Enum
from abc import ABC, abstractmethod

from aiocache import cached
from strenum import StrEnum
from pydantic import BaseModel

from zhenxun.utils.enum import PluginType
from zhenxun.utils.http_utils import AsyncHttpx

from .config import (
    CACHED_API_TTL,
    GIT_API_TREES_FORMAT,
    JSD_PACKAGE_API_FORMAT,
    GITHUB_REPO_URL_PATTERN,
)

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
    branch: str = "main"

    async def get_download_url_with_path(self, path: str):
        url_format = await self.get_fastest_format()
        return url_format.format(**self.dict(), path=path)

    @classmethod
    def parse_github_url(cls, github_url: str) -> "RepoInfo":
        if matched := GITHUB_REPO_URL_PATTERN.match(github_url):
            return RepoInfo(**{k: v for k, v in matched.groupdict().items() if v})
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
    PACKAGE = "gh"


class BaseInfo(BaseModel, ABC):
    """基础信息类"""

    @classmethod
    @abstractmethod
    @cached(ttl=CACHED_API_TTL)
    async def parse_repo_info(cls, repo_info: RepoInfo) -> "BaseInfo": ...

    @abstractmethod
    def get_files(cls, module_path: str, is_dir) -> list[str]: ...


class FileInfo(BaseInfo):
    """文件信息"""

    type: FileType
    name: str
    files: list["FileInfo"] = []

    def recurrence_files(self, dir_path: str, is_dir: bool = True) -> list[str]:
        """
        递归获取文件路径

        参数:
            files: 文件列表
            dir_path: 目录路径
            is_dir: 是否为目录

        返回:
            list[str]: 文件路径
        """
        if not is_dir and dir_path.endswith(self.name):
            return [dir_path]
        if self.files is None:
            raise ValueError("文件列表为空")
        paths = []
        for file in self.files:
            if is_dir and file.type == FileType.DIR and file.files:
                paths.extend(self.recurrence_files(f"{dir_path}/{file.name}", is_dir))
            elif file.type == FileType.FILE:
                if is_dir:
                    paths.append(f"{dir_path}/{file.name}")
                elif dir_path.endswith(file.name):
                    paths.append(dir_path)
        return paths

    def full_files_path(self, module_path: str, is_dir: bool = True) -> "FileInfo":
        """
        获取文件路径

        参数:
            module_path: 模块路径
            is_dir: 是否为目录

        返回:
            list[FileInfo]: 文件路径
        """
        paths: list[str] = module_path.split("/")
        if not is_dir:
            paths = paths[:-1]
        cur_file: FileInfo = self

        for path in paths:
            for file in cur_file.files:
                if file.type == FileType.DIR and file.name == path and file.files:
                    cur_file = file
                    break
            else:
                raise ValueError(f"模块路径 {module_path} 不存在")
        return cur_file

    @classmethod
    @cached(ttl=CACHED_API_TTL)
    async def parse_repo_info(cls, repo_info: RepoInfo) -> "FileInfo":
        """解析仓库信息"""

        """获取插件包信息

        参数:
            repo_info: 仓库信息

        返回:
            FileInfo: 插件包信息
        """
        jsd_package_url: str = JSD_PACKAGE_API_FORMAT.format(
            owner=repo_info.owner, repo=repo_info.repo, branch=repo_info.branch
        )
        res = await AsyncHttpx.get(url=jsd_package_url)
        if res.status_code != 200:
            raise ValueError(f"下载错误, code: {res.status_code}")
        return FileInfo(**res.json())

    def get_files(self, module_path: str, is_dir: bool = True) -> list[str]:
        """获取文件路径"""

        file = self.full_files_path(module_path, is_dir)
        files = file.recurrence_files(
            module_path,
            is_dir,
        )
        return files


class TreeType(StrEnum):
    """树类型"""

    FILE = "blob"
    DIR = "tree"


class Tree(BaseModel):
    """树"""

    path: str
    mode: str
    type: TreeType
    sha: str
    size: int | None
    url: str


class TreesInfo(BaseInfo):
    """树信息"""

    sha: str
    url: str
    tree: list[Tree]

    def export_files(self, module_path: str) -> list[str]:
        """导出文件路径"""
        return [
            file.path
            for file in self.tree
            if file.type == TreeType.FILE and file.path.startswith(module_path)
        ]

    @classmethod
    @cached(ttl=CACHED_API_TTL)
    async def parse_repo_info(cls, repo_info: RepoInfo) -> "TreesInfo":
        """获取仓库树

        参数:
            repo_info: 仓库信息

        返回:
            TreesInfo: 仓库树信息
        """
        git_tree_url: str = GIT_API_TREES_FORMAT.format(
            owner=repo_info.owner, repo=repo_info.repo, branch=repo_info.branch
        )
        res = await AsyncHttpx.get(url=git_tree_url)
        if res.status_code != 200:
            raise ValueError(f"下载错误, code: {res.status_code}")
        return TreesInfo(**res.json())

    def get_files(self, module_path: str, is_dir: bool = True) -> list[str]:
        """获取文件路径"""
        return self.export_files(module_path)


class PackageApi(Enum):
    """插件包接口"""

    GITHUB = TreesInfo
    JSDELIVR = FileInfo
