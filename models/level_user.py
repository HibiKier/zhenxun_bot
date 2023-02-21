from tortoise import fields

from services.db_context import Model


class LevelUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField()
    """群聊id"""
    user_level = fields.BigIntField()
    """用户权限等级"""
    group_flag = fields.IntField(default=0)
    """特殊标记，是否随群管理员变更而设置权限"""

    class Meta:
        table = "level_users"
        table_description = "用户权限数据库"
        unique_together = ("user_qq", "group_id")

    @classmethod
    async def get_user_level(cls, user_qq: int, group_id: int) -> int:
        """
        说明:
            获取用户在群内的等级
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        if user := await cls.get_or_none(user_qq=user_qq, group_id=group_id):
            return user.user_level
        return -1

    @classmethod
    async def set_level(
        cls, user_qq: int, group_id: int, level: int, group_flag: int = 0
    ):
        """
        说明:
            设置用户在群内的权限
        参数:
            :param user_qq: qq号
            :param group_id: 群号
            :param level: 权限等级
            :param group_flag: 是否被自动更新刷新权限 0：是，1：否
        """
        await cls.update_or_create(
            user_qq=user_qq,
            group_id=group_id,
            defaults={"user_level": level, "group_flag": group_flag},
        )

    @classmethod
    async def delete_level(cls, user_qq: int, group_id: int) -> bool:
        """
        说明:
            删除用户权限
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        if user := await cls.get_or_none(user_qq=user_qq, group_id=group_id):
            await user.delete()
            return True
        return False

    @classmethod
    async def check_level(cls, user_qq: int, group_id: int, level: int) -> bool:
        """
        说明:
            检查用户权限等级是否大于 level
        参数:
            :param user_qq: qq号
            :param group_id: 群号
            :param level: 权限等级
        """
        if group_id:
            if user := await cls.get_or_none(user_qq=user_qq, group_id=group_id):
                return user.user_level >= level
        else:
            user_list = await cls.filter(user_qq=user_qq).all()
            user = max(user_list, key=lambda x: x.user_level)
            return user.user_level >= level
        return False

    @classmethod
    async def is_group_flag(cls, user_qq: int, group_id: int) -> bool:
        """
        说明:
            检测是否会被自动更新刷新权限
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        if user := await cls.get_or_none(user_qq=user_qq, group_id=group_id):
            return user.group_flag == 1
        return False
