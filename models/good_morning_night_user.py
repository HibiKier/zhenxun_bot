from services.db_context import db
from datetime import datetime


class GoodMorningNightUser(db.Model):
    __tablename__ = 'good_morning_night_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), nullable=False)
    good_morning_time1 = db.Column(db.DateTime(timezone=True), nullable=True)
    good_night_time1 = db.Column(db.DateTime(timezone=True), nullable=True)
    good_morning_time2 = db.Column(db.DateTime(timezone=True), nullable=True)
    good_night_time2 = db.Column(db.DateTime(timezone=True), nullable=True)
    good_morning_count = db.Column(db.BigInteger(), nullable=True)
    good_night_count = db.Column(db.BigInteger(), nullable=True)
    sleep_time = db.Column(db.BigInteger(), nullable=True)
    first_flag = db.Column(db.BigInteger(), nullable=True)

    _idx1 = db.Index('good_group_users_idx1', 'user_qq', 'belonging_group', unique=True)

    @classmethod
    async def get_good_morning_user(cls, user_qq: int, belonging_group: int, for_update: bool = False)\
            -> 'GoodMorningNightUser':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
                user_qq=user_qq,
                belonging_group=belonging_group,
                good_morning_time1=datetime.now(),
                good_night_time1=datetime.min,
                good_morning_time2=datetime.min,
                good_night_time2=datetime.min,
                good_morning_count=1,
                good_night_count=0,
                sleep_time=0,
                first_flag=0,
            )


    @classmethod
    async def get_good_night_user(cls, user_qq: int, belonging_group: int, for_update: bool = False) \
            -> 'GoodMorningNightUser':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
            user_qq=user_qq,
            belonging_group=belonging_group,
            good_morning_time1=datetime.min,
            good_night_time1=datetime.now(),
            good_morning_time2=datetime.min,
            good_night_time2=datetime.min,
            good_morning_count=0,
            good_night_count=1,
            sleep_time=0,
            first_flag=0,
        )


    @classmethod
    async def delete_user(cls, user_qq: int, belonging_group: int, for_update: bool = False) \
            -> 'bool':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = await query.with_for_update()
        if await query.gino.first() is None:
            return False
        else:
            await cls.delete.where(
                (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
            ).gino.status()
            return True


    @classmethod
    async def get_user(cls, user_qq: int, belonging_group: int, for_update: bool = False) \
            -> 'GoodMorningNightUser':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        if for_update:
            query = await query.with_for_update()
        return await query.gino.first()







