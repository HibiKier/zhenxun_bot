from typing import Dict

from tortoise import fields

from services.db_context import Model

from .goods_info import GoodsInfo


class BagUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField()
    """群聊id"""
    gold = fields.IntField(default=100)
    """金币数量"""
    spend_total_gold = fields.IntField(default=0)
    """花费金币总数"""
    get_total_gold = fields.IntField(default=0)
    """获取金币总数"""
    get_today_gold = fields.IntField(default=0)
    """今日获取金币"""
    spend_today_gold = fields.IntField(default=0)
    """今日获取金币"""
    property: Dict[str, int] = fields.JSONField(default={})
    """道具"""

    class Meta:
        table = "bag_users"
        table_description = "用户道具数据表"
        unique_together = ("user_qq", "group_id")

    @classmethod
    async def get_user_total_gold(cls, user_qq: int, group_id: int) -> str:
        """
        说明:
            获取金币概况
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        return (
            f"当前金币：{user.gold}\n今日获取金币：{user.get_today_gold}\n今日花费金币：{user.spend_today_gold}"
            f"\n今日收益：{user.get_today_gold - user.spend_today_gold}"
            f"\n总赚取金币：{user.get_total_gold}\n总花费金币：{user.spend_total_gold}"
        )

    @classmethod
    async def get_gold(cls, user_qq: int, group_id: int) -> int:
        """
        说明:
            获取当前金币
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        return user.gold

    @classmethod
    async def get_property(
        cls, user_qq: int, group_id: int, only_active: bool = False
    ) -> Dict[str, int]:
        """
        说明:
            获取当前道具
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
            :param only_active: 仅仅获取主动使用的道具
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        if only_active and user.property:
            data = {}
            name_list = [
                x.goods_name
                for x in await GoodsInfo.get_all_goods()
                if not x.is_passive
            ]
            for key in [x for x in user.property if x in name_list]:
                data[key] = user.property[key]
            return data
        return user.property

    @classmethod
    async def add_gold(cls, user_qq: int, group_id: int, num: int):
        """
        说明:
            增加金币
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
            :param num: 金币数量
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        user.gold = user.gold + num
        user.get_total_gold = user.get_total_gold + num
        user.get_today_gold = user.get_today_gold + num
        await user.save(update_fields=["gold", "get_today_gold", "get_total_gold"])

    @classmethod
    async def spend_gold(cls, user_qq: int, group_id: int, num: int):
        """
        说明:
            花费金币
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
            :param num: 金币数量
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        user.gold = user.gold - num
        user.spend_total_gold = user.spend_total_gold + num
        user.spend_today_gold = user.spend_today_gold + num
        await user.save(update_fields=["gold", "spend_total_gold", "spend_today_gold"])

    @classmethod
    async def add_property(cls, user_qq: int, group_id: int, name: str, num: int = 1):
        """
        说明:
            增加道具
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
            :param name: 道具名称
            :param num: 道具数量
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        property_ = user.property
        if property_.get(name) is None:
            property_[name] = 0
        property_[name] += num
        user.property = property_
        await user.save(update_fields=["property"])

    @classmethod
    async def delete_property(
        cls, user_qq: int, group_id: int, name: str, num: int = 1
    ) -> bool:
        """
        说明:
            使用/删除 道具
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
            :param name: 道具名称
            :param num: 使用个数
        """
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        property_ = user.property
        if name in property_:
            if (n := property_.get(name, 0)) < num:
                return False
            if n == num:
                del property_[name]
            else:
                property_[name] -= num
            await user.save(update_fields=["property"])
            return True
        return False

    @classmethod
    async def _run_script(cls):
        await cls.raw("ALTER TABLE bag_users DROP props;")
        """删除 props 字段"""
