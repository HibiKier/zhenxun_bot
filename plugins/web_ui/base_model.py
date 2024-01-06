from datetime import datetime
from logging import warning
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from nonebot.adapters.onebot.v11 import Bot
from pydantic import BaseModel, validator

from configs.utils import Config
from utils.manager.models import Plugin as PluginManager
from utils.manager.models import PluginBlock, PluginCd, PluginCount, PluginSetting

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
    def warning_(cls, info: str, code: int = 200) -> "Result":
        return cls(suc=True, warning=info, code=code)

    @classmethod
    def fail(cls, info: str = "异常错误", code: int = 500) -> "Result":
        return cls(suc=False, info=info, code=code)

    @classmethod
    def ok(cls, data: Any = None, info: str = "操作成功", code: int = 200) -> "Result":
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


class PluginConfig(BaseModel):
    """
    插件配置项
    """

    module: str
    key: str
    value: Optional[Any]
    help: Optional[str]
    default_value: Optional[Any]
    has_type: bool


class Plugin(BaseModel):
    """
    插件
    """

    model: str
    """模块名称"""
    plugin_settings: Optional[PluginSetting]
    """settings"""
    plugin_manager: Optional[PluginManager]
    """manager"""
    plugin_config: Optional[Dict[str, PluginConfig]]
    """配置项"""
    cd_limit: Optional[PluginCd]
    """cd限制"""
    block_limit: Optional[PluginBlock]
    """阻断限制"""
    count_limit: Optional[PluginCount]
    """次数限制"""


class SystemStatus(BaseModel):
    """
    系统状态
    """

    cpu: float
    memory: float
    disk: float
    check_time: datetime


class SystemNetwork(BaseModel):
    """
    系统网络状态
    """

    baidu: int
    google: int


class SystemFolderSize(BaseModel):
    """
    资源文件占比
    """

    font_dir_size: float
    image_dir_size: float
    text_dir_size: float
    record_dir_size: float
    temp_dir_size: float
    data_dir_size: float
    log_dir_size: float
    check_time: datetime


class SystemStatusList(BaseModel):
    """
    状态记录
    """

    cpu_data: List[Dict[str, Union[float, str]]]
    memory_data: List[Dict[str, Union[float, str]]]
    disk_data: List[Dict[str, Union[float, str]]]


class SystemResult(BaseModel):
    """
    系统api返回
    """

    status: SystemStatus
    network: SystemNetwork
    disk: SystemFolderSize
    check_time: datetime
