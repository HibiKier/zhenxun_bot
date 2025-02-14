from tortoise import fields

from zhenxun.configs.config import Config
from zhenxun.services.db_context import Model


class FriendUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, unique=True, description="用户id")
    """用户id"""
    user_name = fields.CharField(max_length=255, default="", description="用户名称")
    """用户名称"""
    nickname = fields.CharField(max_length=255, null=True, description="用户自定义昵称")
    """私聊下自定义昵称"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "friend_users"
        table_description = "好友信息数据表"

    @classmethod
    async def get_user_name(cls, user_id: str) -> str:
        """获取好友用户名称

        参数:
            user_id: 用户id
        """
        if user := await cls.get_or_none(user_id=user_id):
            return user.user_name
        return ""

    @classmethod
    async def get_user_nickname(cls, user_id: str) -> str:
        """获取用户昵称

        参数:
            user_id: 用户id
        """
        if user := await cls.get_or_none(user_id=user_id):
            if user.nickname:
                _tmp = ""
                if black_word := Config.get_config("nickname", "BLACK_WORD"):
                    for x in user.nickname:
                        _tmp += "*" if x in black_word else x
                return _tmp
        return ""

    @classmethod
    async def set_user_nickname(
        cls,
        user_id: str,
        nickname: str,
        uname: str | None = None,
        platform: str | None = None,
    ):
        """设置用户昵称

        参数:
            user_id: 用户id
            nickname: 昵称
            uname: 用户昵称
            platform: 平台
        """
        defaults = {"nickname": nickname}
        if uname is not None:
            defaults["user_name"] = uname
        if platform is not None:
            defaults["platform"] = platform
        await cls.update_or_create(
            user_id=user_id,
            defaults=defaults,
        )

    @classmethod
    def _run_script(cls):
        return [
            "ALTER TABLE friend_users "
            "ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE friend_users "
            "ADD COLUMN platform character varying(255) default 'qq';",
        ]
