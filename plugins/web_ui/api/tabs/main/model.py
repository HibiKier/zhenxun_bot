from nonebot.adapters.onebot.v11 import Bot
from pydantic import BaseModel


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
    """今日 累计接收消息"""
    # received_messages_day: int = 0
    # """今日累计接收消息"""
    # received_messages_week: int = 0
    # """一周内累计接收消息"""
    # received_messages_month: int = 0
    # """一月内累计接收消息"""
    # received_messages_year: int = 0
    # """一年内累计接受消息"""
    connect_time: int = 0
    """连接时间"""

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
