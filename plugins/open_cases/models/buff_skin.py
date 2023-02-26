import random
from typing import List, Optional

from tortoise import fields
from tortoise.contrib.postgres.functions import Random

from services.db_context import Model


class BuffSkin(Model):

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
    skin_price = fields.FloatField(default=0)
    """皮肤价格"""
    create_time = fields.DatetimeField(auto_add_now=True)
    """创建日期"""
    update_time = fields.DatetimeField(auto_add=True)
    """更新日期"""

    class Meta:
        table = "buff_skin"
        table_description = "Buff皮肤数据表"

    @classmethod
    async def random_skin(
        cls,
        num: int,
        color: str,
        abrasion: str,
        is_stattrak: bool = False,
        case_name: Optional[str] = None,
    ) -> List["BuffSkin"]:
        query = cls
        if case_name:
            query = query.filter(case_name=case_name)
        query = query.filter(abrasion=abrasion, is_stattrak=is_stattrak, color=color)
        return await query.annotate(rand=Random()).limit(num)  # type:ignore
