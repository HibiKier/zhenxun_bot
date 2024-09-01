from strenum import StrEnum
from pydantic import BaseModel, validator

from zhenxun.utils.enum import PluginType

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
    def set_default_branch(cls, v):
        return "main" if v is None else v

    def get_download_url_with_path(self, path: str):
        return f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}/{path}"


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
