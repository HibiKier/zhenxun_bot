from datetime import datetime

from services.db_context import db


class OpenCasesUser(db.Model):
    __tablename__ = 'open_cases_users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    total_count = db.Column(db.Integer(), nullable=False, default=0)
    blue_count = db.Column(db.Integer(), nullable=False, default=0)
    blue_st_count = db.Column(db.Integer(), nullable=False, default=0)
    purple_count = db.Column(db.Integer(), nullable=False, default=0)
    purple_st_count = db.Column(db.Integer(), nullable=False, default=0)
    pink_count = db.Column(db.Integer(), nullable=False, default=0)
    pink_st_count = db.Column(db.Integer(), nullable=False, default=0)
    red_count = db.Column(db.Integer(), nullable=False, default=0)
    red_st_count = db.Column(db.Integer(), nullable=False, default=0)
    knife_count = db.Column(db.Integer(), nullable=False, default=0)
    knife_st_count = db.Column(db.Integer(), nullable=False, default=0)
    spend_money = db.Column(db.Integer(), nullable=False, default=0)
    make_money = db.Column(db.Float(), nullable=False, default=0)
    today_open_total = db.Column(db.Integer(), nullable=False, default=0)
    open_cases_time_last = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
    knifes_name = db.Column(db.Unicode(), nullable=False, default="")

    _idx1 = db.Index('open_cases_group_users_idx1', 'user_qq', 'group_id', unique=True)

    @classmethod
    async def ensure(cls, user_qq: int, group_id: int, for_update: bool = False) -> 'OpenCasesUser':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
            user_qq=user_qq,
            group_id=group_id,
        )

    @classmethod
    async def get_user_all(cls, group_id: int = None) -> 'list':
        user_list = []
        if not group_id:
            query = await cls.query.gino.all()
        else:
            query = await cls.query.where(
                (cls.group_id == group_id)
            ).gino.all()
        for user in query:
            user_list.append(user)
        return user_list




