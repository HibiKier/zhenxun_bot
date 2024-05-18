from tortoise import fields

from zhenxun.services.db_context import Model

# 1.狂牙武器箱


class BuffPrice(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    case_id = fields.IntField()
    """箱子id"""
    skin_name = fields.CharField(255, unique=True)
    """皮肤名称"""
    skin_price = fields.FloatField()
    """皮肤价格"""
    update_date = fields.DatetimeField()

    class Meta:
        table = "buff_prices"
        table_description = "Buff价格数据表"
