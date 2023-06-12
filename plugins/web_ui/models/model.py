from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union

from nonebot.adapters.onebot.v11 import Bot
from pydantic import BaseModel

from configs.utils import Config
from utils.manager.models import Plugin as PluginManager
from utils.manager.models import PluginBlock, PluginCd, PluginCount, PluginSetting


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
    data: Any = None
    """返回数据"""

    @classmethod
    def fail(cls, info: str = "异常错误", code: int = 500) -> "Result":
        return cls(suc=False, info=info, code=code)

    @classmethod
    def ok(cls, data: Any = None, info: str = "操作成功", code: int = 200) -> "Result":
        return cls(suc=True, info=info, code=code, data=data)


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


class BotInfo(BaseModel):
    """
    Bot基础信息
    """

    bot: Bot
    """Bot"""
    self_id: str
    """SELF ID"""
    nickname: str
    """昵称"""
    ava_url: str
    """头像url"""
    friend_count: int = 0
    """好友数量"""
    group_count: int = 0
    """群聊数量"""
    received_messages: int = 0
    """累计接收消息"""
    received_messages_day: int = 0
    """今日累计接收消息"""
    received_messages_week: int = 0
    """一周内累计接收消息"""
    received_messages_month: int = 0
    """一月内累计接收消息"""

    plugin_count: int = 0
    """加载插件数量"""
    success_plugin_count: int = 0
    """加载成功插件数量"""
    fail_plugin_count: int = 0
    """加载失败插件数量"""

    is_select: bool = False
    """当前选择"""

    class Config:
        arbitrary_types_allowed = True
