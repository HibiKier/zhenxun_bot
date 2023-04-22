from typing import List, Optional

from tortoise import fields

from services.db_context import Model
from services.log import logger


class GroupInfo(Model):

    group_id = fields.CharField(255, pk=True)
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

    @classmethod
    def _run_script(cls):
        return ["ALTER TABLE group_info ADD group_flag Integer NOT NULL DEFAULT 0;",  # group_info表添加一个group_flag
                "ALTER TABLE group_info ALTER COLUMN group_id TYPE character varying(255);"
                # 将group_id字段类型改为character varying(255)
                ]
