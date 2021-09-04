from datetime import datetime

from services.db_context import db


class SignGroupUser(db.Model):
    __tablename__ = "sign_group_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), nullable=False)

    checkin_count = db.Column(db.Integer(), nullable=False)
    checkin_time_last = db.Column(db.DateTime(timezone=True), nullable=False)
    impression = db.Column(db.Numeric(scale=3, asdecimal=False), nullable=False)
    add_probability = db.Column(
        db.Numeric(scale=3, asdecimal=False), nullable=False, default=0
    )
    specify_probability = db.Column(
        db.Numeric(scale=3, asdecimal=False), nullable=False, default=0
    )

    _idx1 = db.Index("sign_group_users_idx1", "user_qq", "belonging_group", unique=True)

    @classmethod
    async def ensure(
        cls, user_qq: int, belonging_group: int, for_update: bool = False
    ) -> "SignGroupUser":
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
            user_qq=user_qq,
            belonging_group=belonging_group,
            checkin_count=0,
            checkin_time_last=datetime.min,  # 从未签到过
            impression=0,
        )

    @classmethod
    async def sign(cls, user: "SignGroupUser", impression: float, checkin_time_last: datetime):
        await user.update(
            checkin_count=user.checkin_count + 1,
            checkin_time_last=checkin_time_last,
            impression=user.impression + impression,
            add_probability=0,
            specify_probability=0,
        ).apply()

    @classmethod
    async def get_all_impression(cls, belonging_group: int) -> "list, list, list":
        """
        说明：
            获取该群所有用户 id 及对应 好感度
        参数：
            :param belonging_group: 群号
        """
        impression_list = []
        user_qq_list = []
        user_group = []
        if belonging_group:
            query = cls.query.where(cls.belonging_group == belonging_group)
        else:
            query = cls.query
        for user in await query.gino.all():
            impression_list.append(user.impression)
            user_qq_list.append(user.user_qq)
            user_group.append(user.belonging_group)
        return user_qq_list, impression_list, user_group
