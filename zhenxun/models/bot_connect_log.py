from tortoise import fields

from zhenxun.services.db_context import Model


class BotConnectLog(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    bot_id = fields.CharField(255, description="Bot id")
    """Bot id"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""
    connect_time = fields.DatetimeField(description="连接时间")
    """日期"""
    type = fields.IntField(null=True, description="1: 连接, 0: 断开")
    """1: 连接, 0: 断开"""
    create_time = fields.DatetimeField(auto_now_add=True)
    """创建时间"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "bot_connect_log"
        table_description = "bot连接表"
