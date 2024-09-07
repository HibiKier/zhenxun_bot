from enum import Enum
from abc import ABC, abstractmethod

from aiocache import cached
from strenum import StrEnum
from pydantic import BaseModel

from ..http_utils import AsyncHttpx
from .consts import CACHED_API_TTL, GIT_API_TREES_FORMAT, JSD_PACKAGE_API_FORMAT
from .func import (
    get_fastest_raw_format,
    get_fastest_archive_format,
    get_fastest_release_source_format,
)


class RepoInfo(BaseModel):
    """仓库信息"""

    owner: str
    repo: str
    branch: str = "main"

    async def get_raw_download_url(self, path: str):
        url_format = await get_fastest_raw_format()
        return url_format.format(**self.dict(), path=path)

    async def get_archive_download_url(self):
        url_format = await get_fastest_archive_format()
        return url_format.format(**self.dict())

    async def get_release_source_download_url_tgz(self, version: str):
        url_format = await get_fastest_release_source_format()
        return url_format.format(**self.dict(), version=version, compress="tar.gz")

    async def get_release_source_download_url_zip(self, version: str):
        url_format = await get_fastest_release_source_format()
        return url_format.format(**self.dict(), version=version, compress="zip")


class FileType(StrEnum):
    """文件类型"""

    FILE = "file"
    DIR = "directory"
    PACKAGE = "gh"


class BaseAPI(BaseModel, ABC):
    """基础接口"""

    @classmethod
    @abstractmethod
    @cached(ttl=CACHED_API_TTL)
    async def parse_repo_info(cls, repo_info: RepoInfo) -> "BaseAPI": ...

    @abstractmethod
    def get_files(cls, module_path: str, is_dir) -> list[str]: ...


class JsdelivrAPI(BaseAPI):
    """jsdelivr接口"""

    type: FileType
    name: str
    files: list["JsdelivrAPI"] = []

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

    def full_files_path(self, module_path: str, is_dir: bool = True) -> "JsdelivrAPI":
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
        cur_file: JsdelivrAPI = self

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
    async def parse_repo_info(cls, repo_info: RepoInfo) -> "JsdelivrAPI":
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
        return JsdelivrAPI(**res.json())

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


class GitHubAPI(BaseAPI):
    """github接口"""

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
    async def parse_repo_info(cls, repo_info: RepoInfo) -> "GitHubAPI":
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
        return GitHubAPI(**res.json())

    def get_files(self, module_path: str, is_dir: bool = True) -> list[str]:
        """获取文件路径"""
        return self.export_files(module_path)


class PackageApi(Enum):
    """插件包接口"""

    GITHUB = GitHubAPI
    JSDELIVR = JsdelivrAPI
