from typing import NoReturn, overload

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
    block_plugin = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    block_task = fields.TextField(default="", description="禁用被动技能")
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

    @classmethod
    async def set_bot_status(cls, status: bool, bot_id: str | None = None) -> None:
        """
        设置bot状态

        Args:
            status (bool): 状态
            bot_id (str, optional): bot_id. Defaults to None.
        """
        if bot_id:
            await cls.filter(bot_id=bot_id).update(status=status)
        else:
            await cls.all().update(status=status)

    @overload
    def convert_module_format(self, data: str) -> list[str]: ...

    @overload
    def convert_module_format(self, data: list[str]) -> str: ...

    def convert_module_format(self, data: str | list[str]) -> str | list[str]:
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
            return "".join(self.format(item) for item in data)

    @classmethod
    async def toggle_field(
        cls,
        bot_id: str,
        available_field: str,
        block_field: str,
        data: str,
        to_block: bool,
    ) -> NoReturn:
        """
        在 available_field 和 block_field 之间移动指定的 data

        Args:
            bot_id (str): 目标 bot 的 ID
            available_field (str): 可用的目标字段
            block_field (str): 禁用的目标字段
            data (str): 要插入的内容
            to_block (bool): 移动到 block_list 还是 available_list

        Raises:
            ValueError: 如果 data 不在 block_list 与 available_list 中
        """

        def __move_to_block():
            nonlocal available_list, block_list
            setattr(
                bot_data, available_field, available_list.replace(formatted_data, "")
            )
            setattr(bot_data, block_field, block_list + formatted_data)

        def __move_to_available():
            nonlocal available_list, block_list
            setattr(bot_data, block_field, block_list.replace(formatted_data, ""))
            setattr(bot_data, available_field, available_list + formatted_data)

        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        formatted_data = cls.format(data)

        available_list: str = getattr(bot_data, available_field)
        block_list: str = getattr(bot_data, block_field)

        if formatted_data not in available_list and formatted_data not in block_list:
            raise ValueError(f"{data} 不在block_list与available_list中")

        if to_block and formatted_data in available_list:
            __move_to_block()
        elif not to_block and formatted_data in block_list:
            __move_to_available()

        await bot_data.save(update_fields=[available_field, block_field])

    @classmethod
    async def set_block_plugin(cls, bot_id: str | None, module: str) -> NoReturn:
        """
        禁用插件

        Args:
            bot_id (str | None): bot_id
            module (str): 模块名称
        """
        if bot_id:
            await cls.toggle_field(
                bot_id, "available_plugins", "block_plugin", module, True
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls.toggle_field(
                    bot.bot_id,
                    "available_plugins",
                    "block_plugin",
                    module,
                    True,
                )

    @classmethod
    async def set_unblock_plugin(cls, bot_id: str | None, module: str) -> NoReturn:
        """
        启用插件

        Args:
            bot_id (str | None): bot_id
            module (str): 模块名称
        """
        if bot_id:
            await cls.toggle_field(
                bot_id, "block_plugin", "available_plugins", module, False
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls.toggle_field(
                    bot.bot_id,
                    "block_plugin",
                    "available_plugins",
                    module,
                    False,
                )

    @classmethod
    async def set_block_task(cls, bot_id: str | None, module: str) -> NoReturn:
        """
        禁用被动技能

        Args:
            bot_id (str | None): bot_id
            module (str): 模块名称
        """
        if bot_id:
            await cls.toggle_field(
                bot_id, "available_tasks", "block_task", module, True
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls.toggle_field(
                    bot.bot_id, "available_tasks", "block_task", module, True
                )

    @classmethod
    async def set_unblock_task(cls, bot_id: str | None, module: str) -> NoReturn:
        """
        启用被动技能

        Args:
            bot_id (str | None): bot_id
            module (str): 模块名称
        """
        if bot_id:
            await cls.toggle_field(
                bot_id, "block_task", "available_tasks", module, False
            )
        else:
            bot_list = await cls.all()
            for bot in bot_list:
                await cls.toggle_field(
                    bot.bot_id, "block_task", "available_tasks", module, False
                )

    @classmethod
    async def is_block_plugin(cls, bot_id: str, module: str) -> bool:
        """
        检查插件是否被禁用

        Args:
            bot_id (str): bot_id
            module (str): 插件名称

        Returns:
            bool: 是否被禁用
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        return cls.format(module) in bot_data.block_plugin

    @classmethod
    async def is_block_task(cls, bot_id: str, module: str) -> bool:
        """
        检查被动技能是否被禁用

        Args:
            bot_id (str): bot_id
            module (str): 被动技能名称

        Returns:
            bool: 是否被禁用
        """
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        return cls.format(module) in bot_data.block_task
