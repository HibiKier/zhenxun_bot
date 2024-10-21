from tortoise import fields

from zhenxun.services.db_context import Model


class BotConsole(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    bot_id = fields.CharField(255, unique=True, description="bot_id")
    """bot_id"""
    status = fields.BooleanField(default=True, description="Bot状态")
    """Bot状态"""
    block_plugin = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    block_task = fields.TextField(default="", description="禁用被动技能")
    """禁用被动技能"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""

    class Meta:  # type: ignore
        table = "bot_console"
        table_description = "Bot数据表"

    @classmethod
    async def get_bot_status(cls, bot_id: str) -> bool:
        result = await cls.get_or_none(bot_id=bot_id)
        return result.status if result else False

    @classmethod
    async def set_block_plugin(cls, bot_id: str, module: str):
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        if f"<{module}," not in bot_data.block_plugin:
            bot_data.block_plugin += f"<{module},"
        await bot_data.save(update_fields=["block_plugin"])

    @classmethod
    async def set_unblock_plugin(cls, bot_id: str, module: str):
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        if f"<{module}," in bot_data.block_plugin:
            bot_data.block_plugin = bot_data.block_plugin.replace(f"<{module},", "")
        await bot_data.save(update_fields=["block_plugin"])

    @classmethod
    async def set_block_task(cls, bot_id: str, task: str):
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        if f"<{task}," not in bot_data.block_task:
            bot_data.block_plugin += f"<{task},"
        await bot_data.save(update_fields=["block_task"])

    @classmethod
    async def is_block_plugin(cls, bot_id: str, task: str) -> bool:
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        return f"<{task}," in bot_data.block_plugin

    @classmethod
    async def is_block_task(cls, bot_id: str, task: str) -> bool:
        bot_data, _ = await cls.get_or_create(bot_id=bot_id)
        return f"<{task}," in bot_data.block_task
