from services.db_context import db
from typing import Dict
from typing import Optional, List
from services.log import logger


class BagUser(db.Model):
    __tablename__ = "bag_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    gold = db.Column(db.Integer(), default=100)
    props = db.Column(db.TEXT(), nullable=False, default="")  # 旧道具字段（废弃）
    spend_total_gold = db.Column(db.Integer(), default=0)
    get_total_gold = db.Column(db.Integer(), default=0)
    get_today_gold = db.Column(db.Integer(), default=0)
    spend_today_gold = db.Column(db.Integer(), default=0)
    property = db.Column(db.JSON(), nullable=False, default={})  # 新道具字段

    _idx1 = db.Index("bag_group_users_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def get_user_total_gold(cls, user_qq: int, group_id: int) -> str:
        """
        说明：
            获取金币概况
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.gino.first()
        if not user:
            user = await cls.create(
                user_qq=user_qq,
                group_id=group_id,
            )
        return (
            f"当前金币：{user.gold}\n今日获取金币：{user.get_today_gold}\n今日花费金币：{user.spend_today_gold}"
            f"\n今日收益：{user.get_today_gold - user.spend_today_gold}"
            f"\n总赚取金币：{user.get_total_gold}\n总花费金币：{user.spend_total_gold}"
        )

    @classmethod
    async def get_gold(cls, user_qq: int, group_id: int) -> int:
        """
        说明：
            获取当前金币
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.gino.first()
        if user:
            return user.gold
        else:
            await cls.create(
                user_qq=user_qq,
                group_id=group_id,
            )
            return 100

    @classmethod
    async def get_property(cls, user_qq: int, group_id: int) -> Dict[str, int]:
        """
        说明：
            获取当前道具
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.gino.first()
        if user:
            return user.property
        else:
            await cls.create(
                user_qq=user_qq,
                group_id=group_id,
            )
            return {}

    @classmethod
    async def add_gold(cls, user_qq: int, group_id: int, num: int):
        """
        说明：
            增加金币
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
            :param num: 金币数量
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        query = query.with_for_update()
        user = await query.gino.first()
        if user:
            await user.update(
                gold=user.gold + num,
                get_total_gold=user.get_total_gold + num,
                get_today_gold=user.get_today_gold + num,
            ).apply()
        else:
            await cls.create(
                user_qq=user_qq,
                group_id=group_id,
                gold=100 + num,
                get_total_gold=num,
                get_today_gold=num,
            )

    @classmethod
    async def spend_gold(cls, user_qq: int, group_id: int, num: int):
        """
        说明：
            花费金币
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
            :param num: 金币数量
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        query = query.with_for_update()
        user = await query.gino.first()
        if user:
            await user.update(
                gold=user.gold - num,
                spend_total_gold=user.spend_total_gold + num,
                spend_today_gold=user.spend_today_gold + num,
            ).apply()
        else:
            await cls.create(
                user_qq=user_qq,
                group_id=group_id,
                gold=100 - num,
                spend_total_gold=num,
                spend_today_gold=num,
            )

    @classmethod
    async def add_property(cls, user_qq: int, group_id: int, name: str):
        """
        说明：
            增加道具
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
            :param name: 道具名称
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        query = query.with_for_update()
        user = await query.gino.first()
        if user:
            p = user.property
            if p.get(name) is None:
                p[name] = 1
            else:
                p[name] += 1
            await user.update(property=p).apply()
        else:
            await cls.create(user_qq=user_qq, group_id=group_id, property={name: 1})

    @classmethod
    async def delete_property(
        cls, user_qq: int, group_id: int, name: str, num: int = 1
    ) -> bool:
        """
        说明：
            使用/删除 道具
        参数：
            :param user_qq: qq号
            :param group_id: 所在群号
            :param name: 道具名称
            :param num: 使用个数
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        query = query.with_for_update()
        user = await query.gino.first()
        if user:
            property_ = user.property
            if name in property_:
                if property_.get(name) == num:
                    del property_[name]
                else:
                    property_[name] -= num
                await user.update(property=property_).apply()
                return True
        return False

    @classmethod
    async def buy_property(
        cls, user_qq: int, group_id: int, goods: "GoodsInfo", goods_num: int
    ) -> bool:
        """
        说明：
            购买道具
        参数：
            :param user_qq: 用户qq
            :param group_id: 所在群聊
            :param goods: 商品
            :param goods_num: 商品数量
        """
        try:
            # 折扣后金币
            spend_gold = goods.goods_discount * goods.goods_price * goods_num
            await BagUser.spend_gold(user_qq, group_id, spend_gold)
            for _ in range(goods_num):
                await BagUser.add_property(user_qq, group_id, goods.goods_name)
            return True
        except Exception as e:
            logger.error(f"buy_property 发生错误 {type(e)}：{e}")
            return False

    @classmethod
    async def get_all_users(cls, group_id: Optional[int] = None) -> List["BagUser"]:
        """
        说明：
            获取所有用户数据
        参数：
            :param group_id: 群号
        """
        if not group_id:
            query = await cls.query.gino.all()
        else:
            query = await cls.query.where((cls.group_id == group_id)).gino.all()
        return query
