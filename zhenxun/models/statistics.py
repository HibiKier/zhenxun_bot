from tortoise import fields

from zhenxun.services.db_context import Model


class Statistics(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255, null=True)
    """群聊id"""
    plugin_name = fields.CharField(255)
    """插件名称"""
    create_time = fields.DatetimeField(auto_now=True)
    """添加日期"""
    bot_id = fields.CharField(255, null=True)
    """Bot Id"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "statistics"
        table_description = "插件调用统计数据库"

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE statistics RENAME COLUMN user_qq TO user_id;",
            # 将user_qq改为user_id
            "ALTER TABLE statistics ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE statistics ALTER COLUMN group_id TYPE character varying(255);",
            "ALTER TABLE statistics ADD bot_id Text DEFAULT '';",
        ]
