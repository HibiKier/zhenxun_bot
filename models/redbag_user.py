from services.db_context import db
from typing import List


class RedbagUser(db.Model):
    __tablename__ = "redbag_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    send_redbag_count = db.Column(db.Integer(), default=0)
    get_redbag_count = db.Column(db.Integer(), default=0)
    spend_gold = db.Column(db.Integer(), default=0)
    get_gold = db.Column(db.Integer(), default=0)

    _idx1 = db.Index("redbag_group_users_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def add_redbag_data(cls, user_qq: int, group_id: int, itype: str, money: int):
        """
        说明：
            添加收发红包数据
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param itype: 收或发
            :param money: 金钱数量
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.with_for_update().gino.first() or await cls.create(
            user_qq=user_qq,
            group_id=group_id,
        )
        if itype == "get":
            await user.update(
                get_redbag_count=user.get_redbag_count + 1,
                get_gold=user.get_gold + money,
            ).apply()
        else:
            await user.update(
                send_redbag_count=user.send_redbag_count + 1,
                spend_gold=user.spend_gold + money,
            ).apply()

    @classmethod
    async def ensure(cls, user_qq: int, group_id: int) -> bool:
        """
        说明：
            获取用户对象
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.gino.first() or await cls.create(
            user_qq=user_qq,
            group_id=group_id,
        )
        return user

    @classmethod
    async def get_user_all(cls, group_id: int = None) -> List["RedbagUser"]:
        """
        说明：
            获取所有用户对象
        参数：
            :param group_id: 群号
        """
        if not group_id:
            query = await cls.query.gino.all()
        else:
            query = await cls.query.where((cls.group_id == group_id)).gino.all()
        return query
