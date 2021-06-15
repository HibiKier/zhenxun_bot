from services.db_context import db
import time


class BanUser(db.Model):
    __tablename__ = 'ban_users'

    user_qq = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    ban_level = db.Column(db.Integer(), nullable=False)
    ban_time = db.Column(db.BigInteger())
    duration = db.Column(db.BigInteger())

    _idx1 = db.Index('ban_group_users_idx1', 'user_qq', unique=True)

    @classmethod
    async def check_ban_level(cls, user_qq: int, level: int) -> 'bool':
        user = await cls.query.where(
            (cls.user_qq == user_qq)
        ).gino.first()
        if not user:
            return False
        if user.ban_level > level:
            return True
        return False

    @classmethod
    async def check_ban_time(cls, user_qq: int) -> 'str':
        query = cls.query.where(
            (cls.user_qq == user_qq)
        )
        user = await query.gino.first()
        if not user:
            return ''
        if time.time() - (user.ban_time + user.duration) > 0 and user.duration != -1:
            return ''
        if user.duration == -1:
            return '∞'
        return time.time() - user.ban_time - user.duration

    @classmethod
    async def isban(cls, user_qq: int) -> 'bool':
        if await cls.check_ban_time(user_qq):
            return True
        else:
            await cls.unban(user_qq)
            return False

    @classmethod
    async def ban(cls, user_qq: int, ban_level: int, duration: int) -> 'bool':
        query = cls.query.where(
            (cls.user_qq == user_qq)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        if not await cls.check_ban_time(user_qq):
            await cls.unban(user_qq)
            user = None
        if user is None:
            await cls.create(
                user_qq=user_qq,
                ban_level=ban_level,
                ban_time=time.time(),
                duration=duration,
            )
            return True
        else:
            return False

    @classmethod
    async def unban(cls, user_qq: int) -> 'bool':
        query = cls.query.where(
            (cls.user_qq == user_qq)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        if user is None:
            return False
        else:
            await cls.delete.where(
                (cls.user_qq == user_qq)
            ).gino.status()
            return True
