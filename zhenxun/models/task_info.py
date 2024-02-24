from tortoise import fields

from zhenxun.services.db_context import Model


class TaskInfo(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    module = fields.CharField(255, description="被动技能模块名")
    """被动技能模块名"""
    name = fields.CharField(255, description="被动技能名称")
    """被动技能名称"""
    status = fields.BooleanField(default=True, description="全局开关状态")
    """全局开关状态"""
    run_time = fields.CharField(255, null=True, description="运行时间")
    """运行时间"""
    run_count = fields.IntField(default=0, description="运行次数")
    """运行次数"""

    class Meta:
        table = "task_info"
        table_description = "被动技能基本信息"
