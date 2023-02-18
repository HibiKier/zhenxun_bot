from datetime import datetime

from tortoise import fields

from services.db_context import Model


class UserShopGoldLog(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField()
    """群聊id"""
    type = fields.IntField()
    """金币使用类型 0: 购买, 1: 使用, 2: 插件"""
    name = fields.CharField(255)
    """商品/插件 名称"""
    spend_gold = fields.IntField(default=0)
    """花费金币"""
    num = fields.IntField()
    """数量"""
    create_time = fields.DatetimeField(auto_now_add=True)
    """创建时间"""

    class Meta:
        table = "user_shop_gold_log"
        table_description = "金币使用日志表"
