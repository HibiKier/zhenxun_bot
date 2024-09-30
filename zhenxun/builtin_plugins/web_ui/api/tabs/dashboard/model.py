from datetime import datetime

from pydantic import BaseModel


class BotInfo(BaseModel):
    self_id: str
    """SELF ID"""
    nickname: str
    """昵称"""
    ava_url: str
    """头像url"""
    platform: str
    """平台"""
    friend_count: int = 0
    """好友数量"""
    group_count: int = 0
    """群聊数量"""
    received_messages: int = 0
    """今日消息接收"""
    day_call: int = 0
    """今日调用插件次数"""
    connect_time: int = 0
    """连接时间"""
    connect_date: datetime | None = None
    """连接日期"""
