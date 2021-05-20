from services.db_context import db


class FriendUser(db.Model):
    __tablename__ = 'friend_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger(), nullable=False)
    user_name = db.Column(db.Unicode(), nullable=False, default="")
    nickname = db.Column(db.Unicode())

    _idx1 = db.Index('friend_users_idx1', 'user_id', unique=True)

    @classmethod
    async def get_user_name(cls, user_id: int) -> str:
        query = cls.query.where(
            cls.user_id == user_id
        )
        user = await query.gino.first()
        if user:
            return user.user_name
        else:
            return ''

    @classmethod
    async def add_friend_info(cls, user_id: int, user_name: str) -> 'bool':
        try:
            query = cls.query.where(
                cls.user_id == user_id
            )
            user = await query.with_for_update().gino.first()
            if not user:
                await cls.create(
                    user_id=user_id,
                    user_name=user_name,
                )
            else:
                await user.update(
                    user_name=user_name,
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def delete_friend_info(cls, user_id: int) -> 'bool':
        try:
            query = cls.query.where(
                cls.user_id == user_id
            )
            user = await query.with_for_update().gino.first()
            if user:
                await user.delete()
            return True
        except Exception:
            return False

    @classmethod
    async def get_friend_nickname(cls, user_id: int) -> 'str':
        query = cls.query.where(
            cls.user_id == user_id
        )
        user = await query.with_for_update().gino.first()
        if user:
            if user.nickname:
                return user.nickname
        return ''

    @classmethod
    async def set_friend_nickname(cls, user_id: int, nickname: str) -> 'bool':
        try:
            query = cls.query.where(
                cls.user_id == user_id
            )
            user = await query.with_for_update().gino.first()
            if not user:
                await cls.create(
                    user_id=user_id,
                    nickname=nickname,
                )
            else:
                await user.update(
                    nickname=nickname,
                ).apply()
            return True
        except Exception:
            return False
