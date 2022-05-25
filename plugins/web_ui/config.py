from typing import Optional, List, Any, Union, Dict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import nonebot


app = nonebot.get_app()

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CdLimit(BaseModel):
    """
    Cd 限制
    """
    cd: int
    status: bool
    check_type: str
    limit_type: str
    rst: Optional[str]


class BlockLimit(BaseModel):
    """
    Block限制
    """
    status: bool
    check_type: str
    limit_type: str
    rst: Optional[str]


class CountLimit(BaseModel):
    """
    Count限制
    """
    max_count: int
    status: bool
    limit_type: str
    rst: Optional[str]


class PluginManager(BaseModel):
    """
    插件信息
    """
    plugin_name: str  # 插件名称
    status: Optional[bool]  # 插件状态
    error: Optional[bool]  # 加载状态
    version: Optional[float]  # 版本
    author: Optional[str]  # 作者
    block_type: Optional[str]  # 禁用类型


class PluginSettings(BaseModel):
    """
    插件基本设置
    """
    level: Optional[int]  # 群权限等级
    default_status: Optional[bool]  # 默认开关
    limit_superuser: Optional[bool]  # 是否限制超级用户
    cmd: Optional[str]  # cmd别名
    cost_gold: Optional[int]  # 花费金币限制
    plugin_type: Optional[List[Union[str, int]]]  # 帮助类型


class PluginConfig(BaseModel):
    """
    插件配置项
    """
    id: int
    key: str
    value: Optional[Any]
    help_: Optional[str]
    default_value: Optional[Any]


class Plugin(BaseModel):
    """
    插件
    """
    model: str  # 模块
    plugin_settings: Optional[PluginSettings]
    plugin_manager: Optional[PluginManager]
    plugin_config: Optional[List[PluginConfig]]
    cd_limit: Optional[CdLimit]
    block_limit: Optional[BlockLimit]
    count_limit: Optional[CountLimit]


class Group(BaseModel):
    """
    群组信息
    """
    group_id: int
    group_name: str
    member_count: int
    max_member_count: int


class Task(BaseModel):
    """
    被动技能
    """
    name: str
    nameZh: str
    status: bool


class GroupResult(BaseModel):
    """
    群组返回数据
    """
    group: Group
    level: int
    status: bool
    close_plugins: List[str]
    task: List[Task]


class RequestResult(BaseModel):
    """
    好友/群组请求管理
    """
    oid: str
    id: int
    flag: str
    nickname: Optional[str]
    level: Optional[int]
    sex: Optional[str]
    age: Optional[int]
    from_: Optional[str]
    comment: Optional[str]
    invite_group: Optional[int]
    group_name: Optional[str]


class RequestParma(BaseModel):
    """
    操作请求接收数据
    """
    id: int
    handle: str
    type: str


class SystemStatus(BaseModel):
    """
    系统状态
    """
    cpu: int
    memory: int
    disk: int
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


class Result(BaseModel):
    """
    总体返回
    """
    code: int
    data: Any
