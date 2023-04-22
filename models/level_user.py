from tortoise import fields

from services.db_context import Model
from typing import Union

class LevelUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
    """群聊id"""
    user_level = fields.BigIntField()
    """用户权限等级"""
    group_flag = fields.IntField(default=0)
    """特殊标记，是否随群管理员变更而设置权限"""

    class Meta:
        table = "level_users"
        table_description = "用户权限数据库"
        unique_together = ("user_id", "group_id")

    @classmethod
    async def get_user_level(cls, user_id: Union[int, str], group_id: Union[int, str]) -> int:
        """
        说明:
            获取用户在群内的等级
        参数:
            :param user_id: 用户id
            :param group_id: 群组id
        """
        if user := await cls.get_or_none(user_id=str(user_id), group_id=str(group_id)):
            return user.user_level
        return -1

    @classmethod
    async def set_level(
        cls, user_id: Union[int, str], group_id: Union[int, str], level: int, group_flag: int = 0
    ):
        """
        说明:
            设置用户在群内的权限
        参数:
            :param user_id: 用户id
            :param group_id: 群组id
            :param level: 权限等级
            :param group_flag: 是否被自动更新刷新权限 0：是，1：否
        """
        await cls.update_or_create(
            user_id=str(user_id),
            group_id=str(group_id),
            defaults={"user_level": level, "group_flag": group_flag},
        )

    @classmethod
    async def delete_level(cls, user_id: Union[int, str], group_id: Union[int, str]) -> bool:
        """
        说明:
            删除用户权限
        参数:
            :param user_id: 用户id
            :param group_id: 群组id
        """
        if user := await cls.get_or_none(user_id=str(user_id), group_id=str(group_id)):
            await user.delete()
            return True
        return False

    @classmethod
    async def check_level(cls, user_id: Union[int, str], group_id: Union[int, str], level: int) -> bool:
        """
        说明:
            检查用户权限等级是否大于 level
        参数:
            :param user_id: 用户id
            :param group_id: 群组id
            :param level: 权限等级
        """
        if group_id:
            if user := await cls.get_or_none(user_id=str(user_id), group_id=str(group_id)):
                return user.user_level >= level
        else:
            user_list = await cls.filter(user_id=str(user_id)).all()
            user = max(user_list, key=lambda x: x.user_level)
            return user.user_level >= level
        return False

    @classmethod
    async def is_group_flag(cls, user_id: Union[int, str], group_id: Union[int, str]) -> bool:
        """
        说明:
            检测是否会被自动更新刷新权限
        参数:
            :param user_id: 用户id
            :param group_id: 群组id
        """
        if user := await cls.get_or_none(user_id=str(user_id), group_id=str(group_id)):
            return user.group_flag == 1
        return False

    @classmethod
    async def _run_script(cls):
        return ["ALTER TABLE level_users RENAME COLUMN user_qq TO user_id;",  # 将user_id改为user_id
                "ALTER TABLE level_users ALTER COLUMN user_id TYPE character varying(255);",
                # 将user_id字段类型改为character varying(255)
                "ALTER TABLE level_users ALTER COLUMN group_id TYPE character varying(255);"
                ]
