from typing_extensions import Self

from tortoise import fields

from zhenxun.services.db_context import Model

from .sign_log import SignLog
from .user_console import UserConsole


class SignUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, unique=True, description="用户id")
    """用户id"""
    sign_count = fields.IntField(default=0, description="签到次数")
    """签到次数"""
    impression = fields.DecimalField(10, 3, default=0, description="好感度")
    """好感度"""
    user_console: fields.OneToOneRelation[UserConsole] = fields.OneToOneField(
        "models.UserConsole", related_name="user_console", description="用户数据"
    )
    """用户数据"""
    add_probability = fields.DecimalField(
        10, 3, default=0, description="双倍签到增加概率"
    )
    """双倍签到增加概率"""
    specify_probability = fields.DecimalField(
        10, 3, default=0, description="指定双倍概率"
    )
    """使用指定双倍概率"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "sign_users"
        table_description = "用户签到数据表"

    @classmethod
    async def sign(
        cls,
        user_id: str | Self,
        impression: float,
        bot_id: str | None = None,
        platform: str | None = None,
    ) -> Self:
        """签到

        参数:
            user_id: 用户id
            impression: 好感度
            bot_id: bot Id
            platform: 平台
        """
        if isinstance(user_id, SignUser):
            user = user_id
        else:
            user, _ = await cls.get_or_create(
                user_id=user_id, defaults={"platform": platform}
            )
        user.impression = float(user.impression) + impression
        user.add_probability = 0
        user.specify_probability = 0
        user.sign_count += 1
        await user.save()
        await SignLog.create(
            user_id=user.user_id,
            impression=impression,
            bot_id=bot_id,
            platform=platform,
        )
        return user
