from nonebot.adapters.onebot.v11 import Message, MessageEvent
from pydantic import BaseModel
from typing import Any


class ShopParam(BaseModel):
    goods_name: str
    user_id: int
    group_id: int
    bot: Any
    event: MessageEvent
    num: int        # 道具单次使用数量
    message: Message
    text: str
    send_success_msg: bool = True  # 是否发送使用成功信息
    max_num_limit: int = 1         # 单次使用最大次数
