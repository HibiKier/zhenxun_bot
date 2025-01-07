from tortoise import fields

from zhenxun.services.db_context import Model
from zhenxun.utils.enum import PropHandle


class UserPropsLog(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, description="用户id")
    """用户id"""
    uuid = fields.CharField(255, description="道具uuid")
    """道具uuid"""
    num = fields.IntField(null=True, description="道具金币")
    """数量"""
    gold = fields.IntField(null=True, description="道具金币")
    """道具金币"""
    handle = fields.CharEnumField(PropHandle, default=None, description="道具处理类型")
    """道具处理类型"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "user_props_log"
        table_description = "用户道具记录表"
