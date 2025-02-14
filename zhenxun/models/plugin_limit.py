from tortoise import fields

from zhenxun.services.db_context import Model
from zhenxun.utils.enum import LimitCheckType, LimitWatchType, PluginLimitType


class PluginLimit(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    module = fields.CharField(255, description="模块名")
    """模块名"""
    module_path = fields.CharField(255, description="模块路径")
    """模块路径"""
    plugin = fields.ForeignKeyField(
        "models.PluginInfo",
        related_name="plugin_limit",
        on_delete=fields.CASCADE,
        description="所属插件",
    )
    """所属插件"""
    limit_type = fields.CharEnumField(PluginLimitType, description="限制类型")
    """限制类型"""
    watch_type = fields.CharEnumField(LimitWatchType, description="监听类型")
    """监听类型"""
    status = fields.BooleanField(default=True, description="限制的开关状态")
    """限制的开关状态"""
    check_type = fields.CharEnumField(
        LimitCheckType, default=LimitCheckType.ALL, description="检查类型"
    )
    """检查类型"""
    result = fields.CharField(max_length=255, null=True, description="返回信息")
    """返回信息"""
    cd = fields.IntField(null=True, description="cd")
    """cd"""
    max_count = fields.IntField(null=True, description="最大调用次数")
    """最大调用次数"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "plugin_limit"
        table_description = "插件限制"
