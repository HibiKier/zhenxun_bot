from tortoise import fields

from zhenxun.services.db_context import Model

from .goods_info import GoodsInfo


class BagUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
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
    property: dict[str, int] = fields.JSONField(default={})  # type: ignore
    """道具"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "bag_users"
        table_description = "用户道具数据表"
        unique_together = ("user_id", "group_id")

    @classmethod
    async def get_gold(cls, user_id: str, group_id: str) -> int:
        """获取当前金币

        参数:
            user_id: 用户id
            group_id: 所在群组id

        返回:
            int: 金币数量
        """
        user, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        return user.gold

    @classmethod
    async def get_property(
        cls, user_id: str, group_id: str, only_active: bool = False
    ) -> dict[str, int]:
        """获取当前道具

        参数:
            user_id: 用户id
            group_id: 所在群组id
            only_active: 仅仅获取主动使用的道具

        返回:
            Dict[str, int]: 道具名称与数量
        """
        user, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
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
    async def add_gold(cls, user_id: str, group_id: str, num: int):
        """增加金币

        参数:
            user_id: 用户id
            group_id: 所在群组id
            num: 金币数量
        """
        user, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        user.gold = user.gold + num
        user.get_total_gold = user.get_total_gold + num
        user.get_today_gold = user.get_today_gold + num
        await user.save(update_fields=["gold", "get_today_gold", "get_total_gold"])

    @classmethod
    async def spend_gold(cls, user_id: str, group_id: str, num: int):
        """花费金币

        参数:
            user_id: 用户id
            group_id: 所在群组id
            num: 金币数量
        """
        user, _ = await cls.get_or_create(user_id=str(user_id), group_id=str(group_id))
        user.gold = user.gold - num
        user.spend_total_gold = user.spend_total_gold + num
        user.spend_today_gold = user.spend_today_gold + num
        await user.save(update_fields=["gold", "spend_total_gold", "spend_today_gold"])

    @classmethod
    async def add_property(cls, user_id: str, group_id: str, name: str, num: int = 1):
        """增加道具

        参数:
            user_id: 用户id
            group_id: 所在群组id
            name: 道具名称
            num: 道具数量
        """
        user, _ = await cls.get_or_create(user_id=str(user_id), group_id=str(group_id))
        property_ = user.property
        if property_.get(name) is None:
            property_[name] = 0
        property_[name] += num
        user.property = property_
        await user.save(update_fields=["property"])

    @classmethod
    async def delete_property(
        cls, user_id: str, group_id: str, name: str, num: int = 1
    ) -> bool:
        """使用/删除 道具

        参数:
            user_id: 用户id
            group_id: 所在群组id
            name: 道具名称
            num: 使用个数

        返回:
            bool: 是否使用/删除成功
        """
        user, _ = await cls.get_or_create(user_id=str(user_id), group_id=str(group_id))
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
        return [
            # 删除 props 字段
            "ALTER TABLE bag_users DROP props;",
            # 将user_qq改为user_id
            "ALTER TABLE bag_users RENAME COLUMN user_qq TO user_id;",
            "ALTER TABLE bag_users ALTER COLUMN user_id TYPE character varying(255);",
            # 将user_id字段类型改为character varying(255)
            "ALTER TABLE bag_users ALTER COLUMN group_id TYPE character varying(255);",
        ]
