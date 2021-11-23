from services.db_context import db
import time


class BanUser(db.Model):
    __tablename__ = "ban_users"

    user_qq = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    ban_level = db.Column(db.Integer(), nullable=False)
    ban_time = db.Column(db.BigInteger())
    duration = db.Column(db.BigInteger())

    _idx1 = db.Index("ban_group_users_idx1", "user_qq", unique=True)

    @classmethod
    async def check_ban_level(cls, user_qq: int, level: int) -> bool:
        """
        说明：
            检测ban掉目标的用户与unban用户的权限等级大小
        参数：
            :param user_qq: unban用户的qq号
            :param level: ban掉目标用户的权限等级
        """
        user = await cls.query.where((cls.user_qq == user_qq)).gino.first()
        if not user:
            return False
        if user.ban_level > level:
            return True
        return False

    @classmethod
    async def check_ban_time(cls, user_qq: int) -> str:
        """
        说明：
            检测用户被ban时长
        参数：
            :param user_qq: qq号
        """
        query = cls.query.where((cls.user_qq == user_qq))
        user = await query.gino.first()
        if not user:
            return ""
        if time.time() - (user.ban_time + user.duration) > 0 and user.duration != -1:
            return ""
        if user.duration == -1:
            return "∞"
        return time.time() - user.ban_time - user.duration

    @classmethod
    async def is_ban(cls, user_qq: int) -> bool:
        """
        说明：
            判断用户是否被ban
        参数：
            :param user_qq: qq号
        """
        if await cls.check_ban_time(user_qq):
            return True
        else:
            await cls.unban(user_qq)
            return False

    @classmethod
    async def is_super_ban(cls, user_qq: int) -> bool:
        """
        说明：
            判断用户是否被ban
        参数：
            :param user_qq: qq号
        """
        user = await cls.query.where((cls.user_qq == user_qq)).gino.first()
        if not user:
            return False
        if user.ban_level == 10:
            return True

    @classmethod
    async def ban(cls, user_qq: int, ban_level: int, duration: int) -> bool:
        """
        说明：
            ban掉目标用户
        参数：
            :param user_qq: 目标用户qq号
            :param ban_level: 使用ban命令用户的权限
            :param duration:  ban时长，秒
        """
        query = cls.query.where((cls.user_qq == user_qq))
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
    async def unban(cls, user_qq: int) -> bool:
        """
        说明：
            unban用户
        参数：
            :param user_qq: qq号
        """
        query = cls.query.where((cls.user_qq == user_qq))
        query = query.with_for_update()
        user = await query.gino.first()
        if user is None:
            return False
        else:
            await cls.delete.where((cls.user_qq == user_qq)).gino.status()
            return True
