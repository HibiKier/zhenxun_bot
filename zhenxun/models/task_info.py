from tortoise import fields

from zhenxun.services.db_context import Model

from .ban_console import BanConsole
from .group_console import GroupConsole


class TaskInfo(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    module = fields.CharField(255, description="被动技能模块名")
    """被动技能模块名"""
    name = fields.CharField(255, description="被动技能名称")
    """被动技能名称"""
    status = fields.BooleanField(default=True, description="全局开关状态")
    """全局开关状态"""
    # default_status = fields.BooleanField(default=True, description="进群默认状态")
    # """进群默认状态"""
    run_time = fields.CharField(255, null=True, description="运行时间")
    """运行时间"""
    run_count = fields.IntField(default=0, description="运行次数")
    """运行次数"""

    class Meta:
        table = "task_info"
        table_description = "被动技能基本信息"

    @classmethod
    async def is_block(cls, module: str, group_id: str | None) -> bool:
        """判断被动技能是否可以发送

        参数:
            module: 被动技能模块名
            group_id: 群组id

        返回:
            bool: 是否可以发送
        """
        if task := await cls.get_or_none(module=module):
            """被动全局状态"""
            if not task.status:
                return True
        if group_id:
            if await GroupConsole.is_block_task(group_id, module):
                """群组是否禁用被动"""
                return True
            if g := await GroupConsole.get_or_none(
                group_id=group_id, channel_id__isnull=True
            ):
                """群组权限是否小于0"""
                if g.level < 0:
                    return True
            if await BanConsole.is_ban(None, group_id):
                """群组是否被ban"""
                return True
        return False

    @classmethod
    def _run_script(cls):
        return [
            # "ALTER TABLE task_info ADD default_status boolean NOT NULL DEFAULT true;",
        ]
