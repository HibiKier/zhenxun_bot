from datetime import datetime
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

    img_url = fields.CharField(255)
    """图片url"""
    steam_price: float = fields.FloatField(default=0)
    """steam价格"""
    weapon_type = fields.CharField(255)
    """枪械类型"""
    buy_max_price: float = fields.FloatField(default=0)
    """最大求购价格"""
    buy_num: int = fields.IntField(default=0)
    """求购数量"""
    sell_min_price: float = fields.FloatField(default=0)
    """售卖最低价格"""
    sell_num: int = fields.IntField(default=0)
    """出售个数"""
    sell_reference_price: float = fields.FloatField(default=0)
    """参考价格"""

    create_time: datetime = fields.DatetimeField(auto_add_now=True)
    """创建日期"""
    update_time: datetime = fields.DatetimeField(auto_add=True)
    """更新日期"""

    class Meta:
        table = "buff_skin"
        table_description = "Buff皮肤数据表"
        unique_together = ("case_name", "name", "skin_name", "abrasion")

    @classmethod
    async def random_skin(
        cls,
        num: int,
        color: str,
        abrasion: str,
        is_stattrak: bool = False,
        case_name: Optional[str] = None,
    ) -> List["BuffSkin"]:  # type: ignore
        query = cls
        if case_name:
            query = query.filter(case_name=case_name)
        query = query.filter(abrasion=abrasion, is_stattrak=is_stattrak, color=color)
        skin_list = await query.annotate(rand=Random()).limit(num)  # type:ignore
        num_ = num
        cnt = 0
        while len(skin_list) < num:
            cnt += 1
            num_ = num - len(skin_list)
            skin_list += await query.annotate(rand=Random()).limit(num_)
            if cnt > 10:
                break
        return skin_list  # type: ignore

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE buff_skin ADD img_url varchar(255);",  # 新增img_url
            "ALTER TABLE buff_skin ADD steam_price float DEFAULT 0;",  # 新增steam_price
            "ALTER TABLE buff_skin ADD weapon_type varchar(255);",  # 新增type
            "ALTER TABLE buff_skin ADD buy_max_price float DEFAULT 0;",  # 新增buy_max_price
            "ALTER TABLE buff_skin ADD buy_num Integer DEFAULT 0;",  # 新增buy_max_price
            "ALTER TABLE buff_skin ADD sell_min_price float DEFAULT 0;",  # 新增sell_min_price
            "ALTER TABLE buff_skin ADD sell_num Integer DEFAULT 0;",  # 新增sell_num
            "ALTER TABLE buff_skin ADD sell_reference_price float DEFAULT 0;",  # 新增sell_reference_price
            "ALTER TABLE buff_skin DROP COLUMN skin_price;",  # 删除skin_price
        ]
