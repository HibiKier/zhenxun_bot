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
    load_status = fields.BooleanField(default=True, description="进群默认开关状态")
    """加载状态"""
    default_status = fields.BooleanField(default=True, description="进群默认开关状态")
    """全局开关状态"""
    run_time = fields.CharField(255, null=True, description="运行时间")
    """运行时间"""
    run_count = fields.IntField(default=0, description="运行次数")
    """运行次数"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "task_info"
        table_description = "被动技能基本信息"

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE task_info ADD default_status boolean DEFAULT true;",
            "ALTER TABLE task_info ADD load_status boolean DEFAULT false;",
            # 默认状态
        ]
