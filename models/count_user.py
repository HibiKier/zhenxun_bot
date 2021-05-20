
from services.db_context import db


class UserCount(db.Model):
    __tablename__ = 'count_users'

    user_qq = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    reimu_count = db.Column(db.Integer(), nullable=False, default=0)
    setu_r18_count = db.Column(db.Integer(), nullable=False, default=0)

    _idx1 = db.Index('sign_reimu_users_idx1', 'user_qq', unique=True)

    @classmethod
    async def add_user(cls, user_qq: int):
        query = cls.query.where(
            (cls.user_qq == user_qq)
        )
        query = query.with_for_update()
        if not await query.gino.first():
            await cls.create(
                user_qq=user_qq,
            )

    @classmethod
    async def add_count(cls, user_qq: int, name: str, count: int = 1):
        query = cls.query.where(
            (cls.user_qq == user_qq)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        if user:
            if name == 'reimu':
                await user.update(
                    reimu_count=cls.reimu_count + count
                ).apply()
            if name == 'setu_r18':
                await user.update(
                    setu_r18_count=cls.setu_r18_count + count
                ).apply()
        else:
            await cls.create(
                user_qq=user_qq
            )


    @classmethod
    async def check_count(cls, user_qq: int, name: str, max_count: int) -> bool:
        query = cls.query.where(
            (cls.user_qq == user_qq)
        )
        user = await query.gino.first()
        if user:
            if name == 'reimu':
                if user.reimu_count == max_count:
                    return True
                else:
                    return False
            if name == 'setu_r18':
                if user.setu_r18_count == max_count:
                    return True
                else:
                    return False
        else:
            await cls.add_user(user_qq)
            return False

    @classmethod
    async def reset_count(cls):
        for user in await cls.query.gino.all():
            await user.update(
                    reimu_count=0,
                    setu_r18_count=0
                ).apply()




