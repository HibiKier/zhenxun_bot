from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, validator
from typing_extensions import Self

T = TypeVar("T")


class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Result(BaseModel):
    """
    总体返回
    """

    suc: bool
    """调用状态"""
    code: int = 200
    """code"""
    info: str = "操作成功"
    """info"""
    warning: Optional[str] = None
    """警告信息"""
    data: Any = None
    """返回数据"""

    @classmethod
    def warning_(cls, info: str, code: int = 200) -> Self:
        return cls(suc=True, warning=info, code=code)

    @classmethod
    def fail(cls, info: str = "异常错误", code: int = 500) -> Self:
        return cls(suc=False, info=info, code=code)

    @classmethod
    def ok(cls, data: Any = None, info: str = "操作成功", code: int = 200) -> Self:
        return cls(suc=True, info=info, code=code, data=data)


class QueryModel(BaseModel, Generic[T]):
    """
    基本查询条件
    """

    index: int
    """页数"""
    size: int
    """每页数量"""
    data: T
    """携带数据"""

    @validator("index")
    def index_validator(cls, index):
        if index < 1:
            raise ValueError("查询下标小于1...")
        return index

    @validator("size")
    def size_validator(cls, size):
        if size < 1:
            raise ValueError("每页数量小于1...")
        return size


class BaseResultModel(BaseModel):
    """
    基础返回
    """

    total: int
    """总页数"""
    data: Any
    """数据"""


class SystemStatus(BaseModel):
    """
    系统状态
    """

    cpu: float
    memory: float
    disk: float
    check_time: datetime


class SystemFolderSize(BaseModel):
    """
    资源文件占比
    """

    name: str
    """名称"""
    size: float
    """大小"""
    full_path: Optional[str]
    """完整路径"""
    is_dir: bool
    """是否为文件夹"""
