from tortoise import fields
from typing import Union
from configs.config import Config
from services.db_context import Model


class FriendUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, unique=True)
    """用户id"""
    user_name = fields.CharField(max_length=255, default="")
    """用户名称"""
    nickname = fields.CharField(max_length=255, null=True)
    """私聊下自定义昵称"""

    class Meta:
        table = "friend_users"
        table_description = "好友信息数据表"

    @classmethod
    async def get_user_name(cls, user_id: Union[int, str]) -> str:
        """
        说明:
            获取好友用户名称
        参数:
            :param user_id: 用户id
        """
        if user := await cls.get_or_none(user_id=str(user_id)):
            return user.user_name
        return ""

    @classmethod
    async def get_user_nickname(cls, user_id: Union[int, str]) -> str:
        """
        说明:
            获取用户昵称
        参数:
            :param user_id: 用户id
        """
        if user := await cls.get_or_none(user_id=str(user_id)):
            if user.nickname:
                _tmp = ""
                if black_word := Config.get_config("nickname", "BLACK_WORD"):
                    for x in user.nickname:
                        _tmp += "*" if x in black_word else x
                return _tmp
        return ""

    @classmethod
    async def set_user_nickname(cls, user_id: Union[int, str], nickname: str):
        """
        说明:
            设置用户昵称
        参数:
            :param user_id: 用户id
            :param nickname: 昵称
        """
        await cls.update_or_create(user_id=str(user_id), defaults={"nickname": nickname})

    @classmethod
    async def _run_script(cls):
        await cls.raw("ALTER TABLE friend_users ALTER COLUMN user_id TYPE character varying(255);")
        # 将user_id字段类型改为character varying(255))
