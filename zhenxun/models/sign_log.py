from tortoise import fields

from zhenxun.services.db_context import Model


class SignLog(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, description="用户id")
    """用户id"""
    impression = fields.DecimalField(10, 3, default=0, description="好感度")
    """好感度"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""
    bot_id = fields.CharField(255, null=True, description="botId")
    """bot记录id"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "sign_log"
        table_description = "用户签到记录表"
