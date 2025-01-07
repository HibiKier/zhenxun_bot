from tortoise import fields

from zhenxun.services.db_context import Model


class UserProps(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, unique=True, description="用户id")
    """用户id"""
    name = fields.CharField(255, description="道具名称")
    """道具名称"""
    property: dict[str, int] = fields.JSONField(default={})  # type: ignore
    """道具"""
    platform = fields.CharField(255, null=True)
    """平台"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "user_props"
        table_description = "用户道具表"
