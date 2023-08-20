from datetime import datetime

from tortoise import fields

from services.db_context import Model


class OpenCasesUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
    """群聊id"""
    total_count: int = fields.IntField(default=0)
    """总开启次数"""
    blue_count: int = fields.IntField(default=0)
    """蓝色"""
    blue_st_count: int = fields.IntField(default=0)
    """蓝色暗金"""
    purple_count: int = fields.IntField(default=0)
    """紫色"""
    purple_st_count: int = fields.IntField(default=0)
    """紫色暗金"""
    pink_count: int = fields.IntField(default=0)
    """粉色"""
    pink_st_count: int = fields.IntField(default=0)
    """粉色暗金"""
    red_count: int = fields.IntField(default=0)
    """紫色"""
    red_st_count: int = fields.IntField(default=0)
    """紫色暗金"""
    knife_count: int = fields.IntField(default=0)
    """金色"""
    knife_st_count: int = fields.IntField(default=0)
    """金色暗金"""
    spend_money: float = fields.IntField(default=0)
    """花费金币"""
    make_money: float = fields.FloatField(default=0)
    """赚取金币"""
    today_open_total: int = fields.IntField(default=0)
    """今日开箱数量"""
    open_cases_time_last: datetime = fields.DatetimeField()
    """最后开箱日期"""
    knifes_name: str = fields.TextField(default="")
    """已获取金色"""

    class Meta:
        table = "open_cases_users"
        table_description = "开箱统计数据表"
        unique_together = ("user_id", "group_id")

    @classmethod
    async def _run_script(cls):
        return [
            "alter table open_cases_users alter COLUMN make_money type float;",  # 将make_money字段改为float
            "alter table open_cases_users alter COLUMN spend_money type float;",  # 将spend_money字段改为float
            "ALTER TABLE open_cases_users RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE open_cases_users ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE open_cases_users ALTER COLUMN group_id TYPE character varying(255);",
        ]
