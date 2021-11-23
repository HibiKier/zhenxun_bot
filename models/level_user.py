from services.db_context import db


class LevelUser(db.Model):
    __tablename__ = "level_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    user_level = db.Column(db.BigInteger(), nullable=False)
    group_flag = db.Column(db.Integer(), nullable=False, default=0)

    _idx1 = db.Index("level_group_users_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def get_user_level(cls, user_qq: int, group_id: int) -> int:
        """
        说明：
            获取用户在群内的等级
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        user = await query.gino.first()
        if user:
            return user.user_level
        else:
            return -1

    @classmethod
    async def set_level(
        cls, user_qq: int, group_id: int, level: int, group_flag: int = 0
    ) -> bool:
        """
        说明：
            设置用户在群内的权限
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param level: 权限等级
            :param group_flag: 是否被自动更新刷新权限 0：是，1：否
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
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
    async def delete_level(cls, user_qq: int, group_id: int) -> bool:
        """
        说明：
            删除用户权限
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
        query = query.with_for_update()
        user = await query.gino.first()
        if user is None:
            return False
        else:
            await user.delete()
            return True

    @classmethod
    async def check_level(cls, user_qq: int, group_id: int, level: int) -> bool:
        """
        说明：
            检查用户权限等级是否大于 level
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param level: 权限等级
        """
        if group_id != 0:
            query = cls.query.where(
                (cls.user_qq == user_qq) & (cls.group_id == group_id)
            )
            user = await query.gino.first()
            if user is None:
                return False
            user_level = user.user_level
        else:
            query = cls.query.where(cls.user_qq == user_qq)
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
    async def is_group_flag(cls, user_qq: int, group_id: int) -> bool:
        """
        说明：
            检测是否会被自动更新刷新权限
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        user = await cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        ).gino.first()
        if not user:
            return False
        if user.group_flag == 1:
            return True
        else:
            return False
