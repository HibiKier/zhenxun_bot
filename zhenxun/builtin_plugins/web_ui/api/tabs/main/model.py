from typing import Any

from nonebot.adapters import Bot
from nonebot.compat import model_dump
from nonebot.config import Config
from pydantic import BaseModel


class BotManageUpdateParam(BaseModel):
    """bot更新参数"""

    bot_id: str
    """bot id"""
    block_plugins: list[str]
    """禁用插件"""
    block_tasks: list[str]
    """禁用被动"""


class BotStatusParam(BaseModel):
    """bot状态参数"""

    bot_id: str
    """bot id"""
    status: bool
    """状态"""


class BotBlockModule(BaseModel):
    """bot禁用模块参数"""

    bot_id: str
    """bot id"""
    block_plugins: list[str]
    """禁用插件"""
    block_tasks: list[str]
    """禁用被动"""
    all_plugins: list[dict[str, Any]]
    """所有插件"""
    all_tasks: list[dict[str, Any]]
    """所有被动"""


class SystemStatus(BaseModel):
    """
    系统状态
    """

    cpu: float
    memory: float
    disk: float


class BaseInfo(BaseModel):
    """
    基础信息
    """

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
    """今日 累计接收消息"""
    connect_time: int = 0
    """连接时间"""
    connect_date: str | None = None
    """连接日期"""
    connect_count: int = 0
    """连接次数"""
    status: bool = False
    """全局状态"""

    is_select: bool = False
    """当前选择"""
    day_call: int = 0
    """今日调用插件次数"""
    version: str = "unknown"
    """真寻版本"""

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self, **kwargs):
        return model_dump(self, **kwargs)


class TemplateBaseInfo(BaseInfo):
    """
    基础信息
    """

    bot: Bot
    """bot"""


class QueryCount(BaseModel):
    """
    聊天记录数量
    """

    num: int
    """总数"""
    day: int
    """一天内"""
    week: int
    """一周内"""
    month: int
    """一月内"""
    year: int
    """一年内"""


class ActiveGroup(BaseModel):
    """
    活跃群聊数据
    """

    group_id: str
    """群组id"""
    name: str
    """群组名称"""
    chat_num: int
    """发言数量"""
    ava_img: str
    """群组头像"""


class HotPlugin(BaseModel):
    """
    热门插件
    """

    module: str
    """模块名"""
    name: str
    """插件名称"""
    count: int
    """调用次数"""


class NonebotData(BaseModel):
    config: Config
    """nb配置"""
    run_time: int
    """运行时间"""
