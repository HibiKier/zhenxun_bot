from tortoise import fields

from zhenxun.services.db_context import Model


class BuffSkinLog(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    case_name = fields.CharField(255)
    """箱子名称"""
    name = fields.CharField(255)
    """武器/手套/刀名称"""
    skin_name = fields.CharField(255)
    """皮肤名称"""
    is_stattrak = fields.BooleanField(default=False)
    """是否暗金(计数)"""
    abrasion = fields.CharField(255)
    """磨损度"""
    color = fields.CharField(255)
    """颜色(品质)"""

    steam_price = fields.FloatField(default=0)
    """steam价格"""
    weapon_type = fields.CharField(255)
    """枪械类型"""
    buy_max_price = fields.FloatField(default=0)
    """最大求购价格"""
    buy_num = fields.IntField(default=0)
    """求购数量"""
    sell_min_price = fields.FloatField(default=0)
    """售卖最低价格"""
    sell_num = fields.IntField(default=0)
    """出售个数"""
    sell_reference_price = fields.FloatField(default=0)
    """参考价格"""

    create_time = fields.DatetimeField(auto_add_now=True)
    """创建日期"""

    class Meta:
        table = "buff_skin_log"
        table_description = "Buff皮肤更新日志表"

    @classmethod
    async def _run_script(cls):
        return [
            "UPDATE buff_skin_log set case_name='手套' where case_name='手套武器箱'",
            "UPDATE buff_skin_log set case_name='左轮' where case_name='左轮武器箱'",
        ]
