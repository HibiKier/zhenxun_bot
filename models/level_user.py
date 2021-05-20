from services.db_context import db


class LevelUser(db.Model):
    __tablename__ = 'level_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    user_level = db.Column(db.BigInteger(), nullable=False)
    group_flag = db.Column(db.Integer(), nullable=False, default=0)

    _idx1 = db.Index('level_group_users_idx1', 'user_qq', 'group_id', unique=True)

    @classmethod
    async def get_user_level(cls, user_qq: int, group_id: int) -> int:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        user = await query.gino.first()
        if user:
            return user.user_level
        else:
            return -1

    @classmethod
    async def set_level(cls, user_qq: int, group_id: int, level: int, group_flag: int = 0) -> 'bool':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        if user is None:
            await cls.create(
                user_qq=user_qq,
                group_id=group_id,
                user_level=level,
                group_flag=group_flag,
            )
            return True
        else:
            await user.update(user_level=level, group_flag=group_flag).apply()
            return False

    @classmethod
    async def delete_level(cls, user_qq: int, group_id: int, for_update: bool = False) -> 'bool':
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        if user is None:
            return False
        else:
            await user.delete()
            return True

    @classmethod
    async def check_level(cls, user_qq: int, group_id: int, level: int) -> 'bool':
        if group_id != 0:
            query = cls.query.where(
                (cls.user_qq == user_qq) & (cls.group_id == group_id)
            )
            user = await query.gino.first()
            if user is None:
                return False
            user_level = user.user_level
        else:
            query = cls.query.where(
                cls.user_qq == user_qq
            )
            highest_level = 0
            for user in await query.gino.all():
                if user.user_level > highest_level:
                    highest_level = user.user_level
            user_level = highest_level
        if user_level >= level:
            return True
        else:
            return False

    @classmethod
    async def is_group_flag(cls, user_qq: int, group_id: int) -> 'bool':
        user = await cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        ).gino.first()
        if not user:
            return False
        if user.group_flag == 1:
            return True
        else:
            return False

