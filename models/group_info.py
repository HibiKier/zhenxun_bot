from typing import List, Optional

from tortoise import fields

from services.db_context import Model
from services.log import logger


class GroupInfo(Model):

    group_id = fields.BigIntField(pk=True)
    """群聊id"""
    group_name = fields.TextField(default="")
    """群聊名称"""
    max_member_count = fields.IntField(default=0)
    """最大人数"""
    member_count = fields.IntField(default=0)
    """当前人数"""
    group_flag: int = fields.IntField(default=0)
    """群认证标记"""

    class Meta:
        table = "group_info"
        table_description = "群聊信息表"
