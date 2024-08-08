from tortoise import fields
from typing_extensions import Self

from zhenxun.services.db_context import Model


class GroupConsole(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    group_id = fields.CharField(255, description="群组id")
    """群聊id"""
    channel_id = fields.CharField(255, null=True, description="频道id")
    """频道id"""
    group_name = fields.TextField(default="", description="群组名称")
    """群聊名称"""
    max_member_count = fields.IntField(default=0, description="最大人数")
    """最大人数"""
    member_count = fields.IntField(default=0, description="当前人数")
    """当前人数"""
    status = fields.BooleanField(default=True, description="群状态")
    """群状态"""
    level = fields.IntField(default=5, description="群权限")
    """群权限"""
    is_super = fields.BooleanField(
        default=False, description="超级用户指定，可以使用全局关闭的功能"
    )
    """超级用户指定群，可以使用全局关闭的功能"""
    group_flag = fields.IntField(default=0, description="群认证标记")
    """群认证标记"""
    block_plugin = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    block_task = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    platform = fields.CharField(255, default="qq", description="所属平台")
    """所属平台"""

    class Meta:
        table = "group_console"
        table_description = "群组信息表"
        unique_together = ("group_id", "channel_id")

    @classmethod
    async def get_group(cls, group_id: str, channel_id: str | None = None) -> Self:
        """获取群组

        参数:
            group_id: 群组id
            channel_id: 频道id.

        返回:
            Self: GroupConsole
        """
        if channel_id:
            return await cls.get(group_id=group_id, channel_id=channel_id)
        return await cls.get(group_id=group_id, channel_id__isnull=True)

    @classmethod
    async def is_super_group(cls, group_id: str, channel_id: str | None = None) -> bool:
        """是否超级用户指定群

        参数:
            group_id: 群组id
            channel_id: 频道id.

        返回:
            bool: 是否超级用户指定群
        """
        if group := await cls.get_or_none(group_id=group_id):
            return group.is_super
        return False

    @classmethod
    async def is_super_block_plugin(
        cls, group_id: str, module: str, channel_id: str | None = None
    ) -> bool:
        """查看群组是否超级用户禁用功能

        参数:
            group_id: 群组id
            module: 模块名称
            channel_id: 频道id

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            channel_id=channel_id,
            block_plugin__contains=f"super:{module},",
        )

    @classmethod
    async def is_block_plugin(
        cls, group_id: str, module: str, channel_id: str | None = None
    ) -> bool:
        """查看群组是否禁用功能

        参数:
            group_id: 群组id
            module: 模块名称
            channel_id: 频道id

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            channel_id=channel_id,
            block_plugin__contains=f"{module},",
        )

    @classmethod
    async def is_block_task(
        cls, group_id: str, task: str, channel_id: str | None = None
    ) -> bool:
        """查看群组是否禁用被动

        参数:
            group_id: 群组id
            task: 任务模块
            channel_id: 频道id

        返回:
            bool: 是否禁用被动
        """
        if not channel_id:
            return await cls.exists(
                group_id=group_id,
                channel_id__isnull=True,
                block_task__contains=f"{task},",
            )
        return await cls.exists(
            group_id=group_id, channel_id=channel_id, block_task__contains=f"{task},"
        )

    @classmethod
    def _run_script(cls):
        return []
