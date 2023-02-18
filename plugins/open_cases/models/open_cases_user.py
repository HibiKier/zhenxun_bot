from tortoise import fields

from services.db_context import Model


class OpenCasesUser(Model):
    __tablename__ = "open_cases_users"

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField()
    """群聊id"""
    total_count = fields.IntField(default=0)
    """总开启次数"""
    blue_count = fields.IntField(default=0)
    """蓝色"""
    blue_st_count = fields.IntField(default=0)
    """蓝色暗金"""
    purple_count = fields.IntField(default=0)
    """紫色"""
    purple_st_count = fields.IntField(default=0)
    """紫色暗金"""
    pink_count = fields.IntField(default=0)
    """粉色"""
    pink_st_count = fields.IntField(default=0)
    """粉色暗金"""
    red_count = fields.IntField(default=0)
    """紫色"""
    red_st_count = fields.IntField(default=0)
    """紫色暗金"""
    knife_count = fields.IntField(default=0)
    """金色"""
    knife_st_count = fields.IntField(default=0)
    """金色暗金"""
    spend_money = fields.IntField(default=0)
    """花费金币"""
    make_money = fields.IntField(default=0)
    """赚取金币"""
    today_open_total = fields.IntField(default=0)
    """今日开箱数量"""
    open_cases_time_last = fields.DatetimeField()
    """最后开箱日期"""
    knifes_name = fields.TextField(default="")
    """已获取金色"""

    class Meta:
        table = "open_cases_users"
        table_description = "开箱统计数据表"
        unique_together = ("user_qq", "group_id")
