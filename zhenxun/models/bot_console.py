from typing import Literal, overload

from tortoise import fields

from zhenxun.services.db_context import Model


class BotConsole(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    bot_id = fields.CharField(255, unique=True, description="bot_id")
    """bot_id"""
    status = fields.BooleanField(default=True, description="Bot状态")
    """Bot状态"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""
    block_plugins = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    block_tasks = fields.TextField(default="", description="禁用被动技能")
    """禁用被动技能"""
    available_plugins = fields.TextField(default="", description="可用插件")
    # todo))  计划任务 or on_startup 写入可用插件
    """可用插件"""
    available_tasks = fields.TextField(default="", description="可用被动技能")
    # todo))  计划任务 or on_startup 写入可用被动技能
    """可用被动技能"""

    class Meta:  # type: ignore
        table = "bot_console"
        table_description = "Bot数据表"

    @staticmethod
    def format(name: str) -> str:
        return f"<{name},"

    @overload
    @classmethod
    async def get_bot_status(cls) -> list[tuple[str, bool]]: ...

    @overload
    @classmethod
    async def get_bot_status(cls, bot_id: str) -> bool: ...

    @classmethod
    async def get_bot_status(
        cls, bot_id: str | None = None
    ) -> list[tuple[str, bool]] | bool:
        """
        获取bot状态

        Args:
            bot_id (str, optional): bot_id. Defaults to None.

        Returns:
            list[tuple[str, bool]] | bool: bot状态
        """
        if not bot_id:
            return await cls.all().values_list("bot_id", "status")
        result = await cls.get_or_none(bot_id=bot_id)
        return result.status if result else False

    @overload
    @classmethod
    async def get_tasks(cls) -> list[tuple[str, str]]: ...

    @overload
    @classmethod
    async def get_tasks(cls, bot_id: str) -> str: ...

    @overload
    @classmethod
    async def get_tasks(cls, *, status: bool) -> list[tuple[str, str]]: ...

    @overload
    @classmethod
    async def get_tasks(cls, bot_id: str, status: bool = True) -> str: ...

    @classmethod
    async def get_tasks(cls, bot_id: str | None = None, status: bool | None = True):
        """
        获取bot被动技能

        Args:
            bot_id (str | None, optional): bot_id. Defaults to None.
            status (bool | None, optional): 被动状态. Defaults to True.

        Returns:
            list[tuple[str, str]] | str: 被动技能
        """
        if not bot_id:
            task_field = "available_tasks" if status else "block_tasks"
            return await cls.all().values_list("bot_id", task_field)

        result = await cls.get_or_none(bot_id=bot_id)
        if result:
            return result.available_tasks if status else result.block_tasks
        return ""

    @overload
    @classmethod
    async def get_plugins(cls) -> list[tuple[str, str]]: ...

    @overload
    @classmethod
    async def get_plugins(cls, bot_id: str) -> str: ...

    @overload
    @classmethod
    async def get_plugins(cls, *, status: bool) -> list[tuple[str, str]]: ...

    @overload
    @classmethod
    async def get_plugins(cls, bot_id: str, status: bool = True) -> str: ...

    @classmethod
    async def get_plugins(cls, bot_id: str | None = None, status: bool = True):
        """
        获取bot插件

        Args:
            bot_id (str | None, optional): bot_id. Defaults to None.
            status (bool, optional): 插件状态. Defaults to True.

        Returns:
            list[tuple[str, str]] | str: 插件
        """
        if not bot_id:
            plugin_field = "available_plugins" if status else "block_plugins"
            return await cls.all().values_list("bot_id", plugin_field)

        result = await cls.get_or_none(bot_id=bot_id)
        if result:
            return result.available_plugins if status else result.block_plugins
        return ""

    @classmethod
    async def set_bot_status(cls, status: bool, bot_id: str | None = None) -> None:
        """
        设置bot状态

        Args:
            status (bool): 状态
            bot_id (str, optional): bot_id. Defaults to None.

        Raises:
            ValueError: 未找到 bot_id
        """
        if bot_id:
            affected_rows = await cls.filter(bot_id=bot_id).update(status=status)
            if not affected_rows:
                raise ValueError(f"未找到 bot_id: {bot_id}")
        else:
            await cls.all().update(status=status)

    @overload
    @classmethod
    def _convert_module_format(cls, data: str) -> list[str]: ...

    @overload
    @classmethod
    def _convert_module_format(cls, data: list[str]) -> str: ...

    @classmethod
    def _convert_module_format(cls, data: str | list[str]) -> str | list[str]:
        """
        在 `<aaa,<bbb,<ccc,` 和 `["aaa", "bbb", "ccc"]` 之间进行相互转换。

        Args:
            data (str | list[str]): 输入数据，可能是格式化字符串或字符串列表。

        Returns:
            str | list[str]: 根据输入类型返回转换后的数据。
        """
        if isinstance(data, str):
            return [item.strip(",") for item in data.split("<") if item]
        elif isinstance(data, list):
            return "".join(cls.format(item) for item in data)

    @classmethod
    async def _toggle_field(
        cls,
        bot_id: str,
        from_field: str,
        to_field: str,
        data: str,
    ) -> None:
        """
        在 from_field 和 to_field 之间移动指定的 data

        Args:
            bot_id (str): 目标 bot 的 ID
            from_field (str): 源字段名称
            to_field (str): 目标字段名称
            data (str): 要插入的内容

        Raises:
            ValueError: 如果 data 不在 from_field 和 to_field 中
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        formatted_data = cls.format(data)

        from_list: str = getattr(bot_data, from_field)
        to_list: str = getattr(bot_data, to_field)

        if formatted_data not in (from_list + to_list):
            raise ValueError(f"{data} 不在源字段和目标字段中")

        if formatted_data in from_list:
            from_list = from_list.replace(formatted_data, "", 1)
            if formatted_data not in to_list:
                to_list += formatted_data

        setattr(bot_data, from_field, from_list)
        setattr(bot_data, to_field, to_list)

        await bot_data.save(update_fields=[from_field, to_field])

    @classmethod
    async def disable_plugin(cls, bot_id: str | None, plugin_name: str) -> None:
        """
        禁用插件

        Args:
            bot_id (str | None): bot_id
            plugin_name (str): 插件名称
        """
        if bot_id:
            await cls._toggle_field(
                bot_id,
                "available_plugins",
                "block_plugins",
                plugin_name,
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls._toggle_field(
                    bot.bot_id,
                    "available_plugins",
                    "block_plugins",
                    plugin_name,
                )

    @classmethod
    async def enable_plugin(cls, bot_id: str | None, plugin_name: str) -> None:
        """
        启用插件

        Args:
            bot_id (str | None): bot_id
            plugin_name (str): 插件名称
        """
        if bot_id:
            await cls._toggle_field(
                bot_id,
                "block_plugins",
                "available_plugins",
                plugin_name,
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls._toggle_field(
                    bot.bot_id,
                    "block_plugins",
                    "available_plugins",
                    plugin_name,
                )

    @classmethod
    async def disable_task(cls, bot_id: str | None, task_name: str) -> None:
        """
        禁用被动技能

        Args:
            bot_id (str | None): bot_id
            task_name (str): 被动技能名称
        """
        if bot_id:
            await cls._toggle_field(
                bot_id,
                "available_tasks",
                "block_tasks",
                task_name,
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls._toggle_field(
                    bot.bot_id,
                    "available_tasks",
                    "block_tasks",
                    task_name,
                )

    @classmethod
    async def enable_task(cls, bot_id: str | None, task_name: str) -> None:
        """
        启用被动技能

        Args:
            bot_id (str | None): bot_id
            task_name (str): 被动技能名称
        """
        if bot_id:
            await cls._toggle_field(
                bot_id,
                "block_tasks",
                "available_tasks",
                task_name,
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls._toggle_field(
                    bot.bot_id,
                    "block_tasks",
                    "available_tasks",
                    task_name,
                )

    @classmethod
    async def disable_all(
        cls,
        bot_id: str,
        feat: Literal["plugins", "tasks"],
    ) -> None:
        """
        禁用全部插件或被动技能

        Args:
            bot_id (str): bot_id
            feat (Literal["plugins", "tasks"]): 插件或被动技能
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        if feat == "plugins":
            bot_data.available_plugins = ""
            # todo)) 使用初始化方法重新写入bot_data.block_plugins以保证插件列表完整
        elif feat == "tasks":
            bot_data.available_tasks = ""
            # todo)) 使用初始化方法重新写入bot_data.block_tasks以保证插件列表完整
        await bot_data.save()

    @classmethod
    async def enable_all(
        cls,
        bot_id: str,
        feat: Literal["plugins", "tasks"],
    ) -> None:
        """
        启用全部插件或被动技能

        Args:
            bot_id (str): bot_id
            feat (Literal["plugins", "tasks"]): 插件或被动技能
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        if feat == "plugins":
            bot_data.block_plugins = ""
            # todo)) 使用初始化方法重新写入bot_data.available_plugins以保证插件列表完整
        elif feat == "tasks":
            bot_data.block_tasks = ""
            # todo)) 使用初始化方法重新写入bot_data.available_tasks以保证插件列表完整
        await bot_data.save()

    @classmethod
    async def is_block_plugin(cls, bot_id: str, plugin_name: str) -> bool:
        """
        检查插件是否被禁用

        Args:
            bot_id (str): bot_id
            plugin_name (str): 插件名称

        Returns:
            bool: 是否被禁用
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        return cls.format(plugin_name) in bot_data.block_plugins

    @classmethod
    async def is_block_task(cls, bot_id: str, task_name: str) -> bool:
        """
        检查被动技能是否被禁用

        Args:
            bot_id (str): bot_id
            task_name (str): 被动技能名称

        Returns:
            bool: 是否被禁用
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        return cls.format(task_name) in bot_data.block_tasks
