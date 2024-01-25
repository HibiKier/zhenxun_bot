from typing import Any

from nonebot.adapters.onebot.v11 import Message, MessageEvent
from pydantic import BaseModel


class ShopParam(BaseModel):


    goods_name: str
    """商品名称"""
    user_id: int
    """用户id"""
    group_id: int
    """群聊id"""
    bot: Any
    """bot"""
    event: MessageEvent
    """event"""
    num: int
    """道具单次使用数量"""
    message: Message
    """message"""
    text: str
    """text"""
    send_success_msg: bool = True
    """是否发送使用成功信息"""
    max_num_limit: int = 1
    """单次使用最大次数"""


class CommonSql(BaseModel):

    sql: str
    """sql语句"""
    remark: str
    """备注"""