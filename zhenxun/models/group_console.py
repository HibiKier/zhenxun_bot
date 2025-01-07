from typing import Any, overload
from typing_extensions import Self

from tortoise import fields
from tortoise.backends.base.client import BaseDBAsyncClient

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.db_context import Model
from zhenxun.utils.enum import PluginType


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
    superuser_block_plugin = fields.TextField(
        default="", description="超级用户禁用插件"
    )
    """超级用户禁用插件"""
    block_task = fields.TextField(default="", description="禁用被动技能")
    """禁用被动技能"""
    superuser_block_task = fields.TextField(default="", description="超级用户禁用被动")
    """超级用户禁用被动"""
    platform = fields.CharField(255, default="qq", description="所属平台")
    """所属平台"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "group_console"
        table_description = "群组信息表"
        unique_together = ("group_id", "channel_id")

    @staticmethod
    def format(name: str) -> str:
        return f"<{name},"

    @overload
    @classmethod
    def convert_module_format(cls, data: str) -> list[str]: ...

    @overload
    @classmethod
    def convert_module_format(cls, data: list[str]) -> str: ...

    @classmethod
    def convert_module_format(cls, data: str | list[str]) -> str | list[str]:
        """
        在 `<aaa,<bbb,<ccc,` 和 `["aaa", "bbb", "ccc"]` 之间进行相互转换。

        参数:
            data (str | list[str]): 输入数据，可能是格式化字符串或字符串列表。

        返回:
            str | list[str]: 根据输入类型返回转换后的数据。
        """
        if isinstance(data, str):
            return [item.strip(",") for item in data.split("<") if item]
        elif isinstance(data, list):
            return "".join(cls.format(item) for item in data)

    @classmethod
    async def create(
        cls, using_db: BaseDBAsyncClient | None = None, **kwargs: Any
    ) -> Self:
        """覆盖create方法"""
        group = await super().create(using_db=using_db, **kwargs)
        if modules := await TaskInfo.filter(default_status=False).values_list(
            "module", flat=True
        ):
            group.block_task = cls.convert_module_format(modules)  # type: ignore
        if modules := await PluginInfo.filter(
            plugin_type__in=[PluginType.NORMAL, PluginType.DEPENDANT],
            default_status=False,
        ).values_list("module", flat=True):
            group.block_plugin = cls.convert_module_format(modules)  # type: ignore
        await group.save(
            using_db=using_db, update_fields=["block_plugin", "block_task"]
        )
        return group

    @classmethod
    async def get_or_create(
        cls,
        defaults: dict | None = None,
        using_db: BaseDBAsyncClient | None = None,
        **kwargs: Any,
    ) -> tuple[Self, bool]:
        """覆盖get_or_create方法"""
        group, is_create = await super().get_or_create(
            defaults=defaults, using_db=using_db, **kwargs
        )
        if is_create and (
            modules := await TaskInfo.filter(default_status=False).values_list(
                "module", flat=True
            )
        ):
            group.block_task = cls.convert_module_format(modules)  # type: ignore
        if modules := await PluginInfo.filter(
            plugin_type__in=[PluginType.NORMAL, PluginType.DEPENDANT],
            default_status=False,
        ).values_list("module", flat=True):
            group.block_plugin = cls.convert_module_format(modules)  # type: ignore
        await group.save(
            using_db=using_db, update_fields=["block_plugin", "block_task"]
        )
        return group, is_create

    @classmethod
    async def update_or_create(
        cls,
        defaults: dict | None = None,
        using_db: BaseDBAsyncClient | None = None,
        **kwargs: Any,
    ) -> tuple[Self, bool]:
        """覆盖update_or_create方法"""
        group, is_create = await super().update_or_create(
            defaults=defaults, using_db=using_db, **kwargs
        )
        if is_create and (
            modules := await TaskInfo.filter(default_status=False).values_list(
                "module", flat=True
            )
        ):
            group.block_task = cls.convert_module_format(modules)  # type: ignore
        if modules := await PluginInfo.filter(
            plugin_type__in=[PluginType.NORMAL, PluginType.DEPENDANT],
            default_status=False,
        ).values_list("module", flat=True):
            group.block_plugin = cls.convert_module_format(modules)  # type: ignore
        await group.save(
            using_db=using_db, update_fields=["block_plugin", "block_task"]
        )
        return group, is_create

    @classmethod
    async def get_group(
        cls, group_id: str, channel_id: str | None = None
    ) -> Self | None:
        """获取群组

        参数:
            group_id: 群组id
            channel_id: 频道id.

        返回:
            Self: GroupConsole
        """
        if channel_id:
            return await cls.get_or_none(group_id=group_id, channel_id=channel_id)
        return await cls.get_or_none(group_id=group_id, channel_id__isnull=True)

    @classmethod
    async def is_super_group(cls, group_id: str) -> bool:
        """是否超级用户指定群

        参数:
            group_id: 群组id

        返回:
            bool: 是否超级用户指定群
        """
        return group.is_super if (group := await cls.get_group(group_id)) else False

    @classmethod
    async def is_superuser_block_plugin(cls, group_id: str, module: str) -> bool:
        """查看群组是否超级用户禁用功能

        参数:
            group_id: 群组id
            module: 模块名称

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            superuser_block_plugin__contains=f"<{module},",
        )

    @classmethod
    async def is_block_plugin(cls, group_id: str, module: str) -> bool:
        """查看群组是否禁用插件

        参数:
            group_id: 群组id
            plugin: 插件名称

        返回:
            bool: 是否禁用插件
        """
        return await cls.exists(
            group_id=group_id, block_plugin__contains=f"<{module},"
        ) or await cls.exists(
            group_id=group_id, superuser_block_plugin__contains=f"<{module},"
        )

    @classmethod
    async def set_block_plugin(
        cls,
        group_id: str,
        module: str,
        is_superuser: bool = False,
        platform: str | None = None,
    ):
        """禁用群组插件

        参数:
            group_id: 群组id
            task: 任务模块
            is_superuser: 是否为超级用户
            platform: 平台
        """
        group, _ = await cls.get_or_create(
            group_id=group_id, defaults={"platform": platform}
        )
        if is_superuser:
            if f"<{module}," not in group.superuser_block_plugin:
                group.superuser_block_plugin += f"<{module},"
        elif f"<{module}," not in group.block_plugin:
            group.block_plugin += f"<{module},"
        await group.save(update_fields=["block_plugin", "superuser_block_plugin"])

    @classmethod
    async def set_unblock_plugin(
        cls,
        group_id: str,
        module: str,
        is_superuser: bool = False,
        platform: str | None = None,
    ):
        """禁用群组插件

        参数:
            group_id: 群组id
            task: 任务模块
            is_superuser: 是否为超级用户
            platform: 平台
        """
        group, _ = await cls.get_or_create(
            group_id=group_id, defaults={"platform": platform}
        )
        if is_superuser:
            if f"<{module}," in group.superuser_block_plugin:
                group.superuser_block_plugin = group.superuser_block_plugin.replace(
                    f"<{module},", ""
                )
        elif f"<{module}," in group.block_plugin:
            group.block_plugin = group.block_plugin.replace(f"<{module},", "")
        await group.save(update_fields=["block_plugin", "superuser_block_plugin"])

    @classmethod
    async def is_normal_block_plugin(
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
            block_plugin__contains=f"<{module},",
        )

    @classmethod
    async def is_superuser_block_task(cls, group_id: str, task: str) -> bool:
        """查看群组是否超级用户禁用被动

        参数:
            group_id: 群组id
            task: 模块名称

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            superuser_block_task__contains=f"<{task},",
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
                block_task__contains=f"<{task},",
            ) or await cls.exists(
                group_id=group_id,
                channel_id__isnull=True,
                superuser_block_task__contains=f"<{task},",
            )
        return await cls.exists(
            group_id=group_id, channel_id=channel_id, block_task__contains=f"<{task},"
        ) or await cls.exists(
            group_id=group_id,
            channel_id__isnull=True,
            superuser_block_task__contains=f"<{task},",
        )

    @classmethod
    async def set_block_task(
        cls,
        group_id: str,
        task: str,
        is_superuser: bool = False,
        platform: str | None = None,
    ):
        """禁用群组插件

        参数:
            group_id: 群组id
            task: 任务模块
            is_superuser: 是否为超级用户
            platform: 平台
        """
        group, _ = await cls.get_or_create(
            group_id=group_id, defaults={"platform": platform}
        )
        if is_superuser:
            if f"<{task}," not in group.superuser_block_task:
                group.superuser_block_task += f"<{task},"
        elif f"<{task}," not in group.block_task:
            group.block_task += f"<{task},"
        await group.save(update_fields=["block_task", "superuser_block_task"])

    @classmethod
    async def set_unblock_task(
        cls,
        group_id: str,
        task: str,
        is_superuser: bool = False,
        platform: str | None = None,
    ):
        """禁用群组插件

        参数:
            group_id: 群组id
            task: 任务模块
            is_superuser: 是否为超级用户
            platform: 平台
        """
        group, _ = await cls.get_or_create(
            group_id=group_id, defaults={"platform": platform}
        )
        if is_superuser:
            if f"<{task}," in group.superuser_block_task:
                group.superuser_block_task = group.superuser_block_task.replace(
                    f"<{task},", ""
                )
        elif f"<{task}," in group.block_task:
            group.block_task = group.block_task.replace(f"<{task},", "")
        await group.save(update_fields=["block_task", "superuser_block_task"])

    @classmethod
    def _run_script(cls):
        return [
            "ALTER TABLE group_console ADD superuser_block_plugin"
            " character varying(255) NOT NULL DEFAULT '';",
            "ALTER TABLE group_console ADD superuser_block_task"
            " character varying(255) NOT NULL DEFAULT '';",
        ]
