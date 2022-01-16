from datetime import datetime
from typing import List
from services.db_context import db


class SignGroupUser(db.Model):
    __tablename__ = "sign_group_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    checkin_count = db.Column(db.Integer(), nullable=False)
    checkin_time_last = db.Column(db.DateTime(timezone=True), nullable=False)
    impression = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False)
    add_probability = db.Column(
        db.Numeric(scale=3, asdecimal=False), nullable=False, default=0
    )
    specify_probability = db.Column(
        db.Numeric(scale=3, asdecimal=False), nullable=False, default=0
    )

    _idx1 = db.Index("sign_group_users_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def ensure(
        cls, user_qq: int, group_id: int, for_update: bool = False
    ) -> "SignGroupUser":
        """
        说明:
            获取签到用户
        参数:
            :param user_qq: 用户qq
            :param group_id: 所在群聊
            :param for_update: 是否存在修改数据
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
            user_qq=user_qq,
            group_id=group_id,
            checkin_count=0,
            checkin_time_last=datetime.min,  # 从未签到过
            impression=0,
        )

    @classmethod
    async def get_user_all_data(cls, user_qq: int) -> List["SignGroupUser"]:
        """
        说明:
            获取某用户所有数据
        参数:
            :param user_qq: 用户qq
        """
        query = cls.query.where(cls.user_qq == user_qq)
        query = query.with_for_update()
        return await query.gino.all()

    @classmethod
    async def sign(cls, user: "SignGroupUser", impression: float, checkin_time_last: datetime):
        """
        说明:
            签到
        说明:
            :param user: 用户
            :param impression: 增加的好感度
            :param checkin_time_last: 签到时间
        """
        await user.update(
            checkin_count=user.checkin_count + 1,
            checkin_time_last=checkin_time_last,
            impression=user.impression + impression,
            add_probability=0,
            specify_probability=0,
        ).apply()

    @classmethod
    async def get_all_impression(cls, group_id: int) -> "list, list, list":
        """
        说明：
            获取该群所有用户 id 及对应 好感度
        参数：
            :param group_id: 群号
        """
        impression_list = []
        user_qq_list = []
        user_group = []
        if group_id:
            query = cls.query.where(cls.group_id == group_id)
        else:
            query = cls.query
        for user in await query.gino.all():
            impression_list.append(user.impression)
            user_qq_list.append(user.user_qq)
            user_group.append(user.group_id)
        return user_qq_list, impression_list, user_group
