

from tortoise import fields

from services.db_context import Model


class Statistics(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField(null=True)
    """群聊id"""
    plugin_name = fields.CharField(255)
    """插件名称"""
    create_time = fields.DatetimeField(auto_now=True)
    """添加日期"""

    class Meta:
        table = "statistics"
        table_description = "用户权限数据库"
