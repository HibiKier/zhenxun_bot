from typing import Dict

from tortoise import fields

from zhenxun.services.db_context import Model
from zhenxun.utils.enum import GoldHandle

from .user_gold_log import UserGoldLog


class UserConsole(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, unique=True, description="用户id")
    """用户id"""
    uid = fields.IntField(description="UID")
    """UID"""
    gold = fields.IntField(default=100, description="金币数量")
    """金币数量"""
    sign = fields.ReverseRelation["SignUser"]  # type: ignore
    """好感度"""
    props: Dict[str, int] = fields.JSONField(default={})  # type: ignore
    """道具"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""

    class Meta:
        table = "user_console"
        table_description = "用户数据表"

    @classmethod
    async def get_new_uid(cls):
        if user := await cls.annotate().order_by("uid").first():
            return user.uid + 1
        return 1

    @classmethod
    async def add_gold(
        cls, user_id: str, gold: int, source: str, platform: str | None = None
    ):
        """添加金币

        参数:
            user_id: 用户id
            gold: 金币
            source: 来源
            platform: 平台.
        """
        user, _ = await cls.get_or_create(
            user_id=user_id, defaults={"platform": platform, "uid": cls.get_new_uid()}
        )
        user.gold += gold
        await user.save(update_fields=["gold"])
        await UserGoldLog.create(
            user_id=user_id, gold=gold, handle=GoldHandle.GET, source=source
        )

    @classmethod
    async def add_props(
        cls, user_id: str, goods_uuid: str, num: int = 1, platform: str | None = None
    ):
        """添加道具

        参数:
            user_id: 用户id
            goods_uuid: 道具uuid
            num: 道具数量.
            platform: 平台.
        """
        user, _ = await cls.get_or_create(
            user_id=user_id, defaults={"platform": platform, "uid": cls.get_new_uid()}
        )
        if goods_uuid not in user.props:
            user.props[goods_uuid] = 0
        user.props[goods_uuid] += num
        await user.save(update_fields=["props"])
