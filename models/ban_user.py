import time
from typing import Union

from tortoise import fields

from services.db_context import Model
from services.log import logger


class BanUser(Model):

    user_qq = fields.IntField(pk=True)
    """用户id"""
    ban_level = fields.IntField()
    """使用ban命令的用户等级"""
    ban_time = fields.BigIntField()
    """ban开始的时间"""
    duration = fields.BigIntField()
    """ban时长"""

    class Meta:
        table = "ban_users"
        table_description = ".ban/b了 封禁人员数据表"

    @classmethod
    async def check_ban_level(cls, user_qq: int, level: int) -> bool:
        """
        说明:
            检测ban掉目标的用户与unban用户的权限等级大小
        参数:
            :param user_qq: unban用户的qq号
            :param level: ban掉目标用户的权限等级
        """
        user = await cls.filter(user_qq=user_qq).first()
        if user:
            logger.debug(
                f"检测用户被ban等级，user_level: {user.ban_level}，level: {level}",
                target=user_qq,
            )
            return bool(user and user.ban_level > level)
        return False

    @classmethod
    async def check_ban_time(cls, user_qq: int) -> Union[str, int]:
        """
        说明:
            检测用户被ban时长
        参数:
            :param user_qq: qq号
        """
        logger.debug(f"获取用户ban时长", target=user_qq)
        if user := await cls.filter(user_qq=user_qq).first():
            if (
                time.time() - (user.ban_time + user.duration) > 0
                and user.duration != -1
            ):
                return ""
            if user.duration == -1:
                return "∞"
            return int(time.time() - user.ban_time - user.duration)
        return ""

    @classmethod
    async def is_ban(cls, user_qq: int) -> bool:
        """
        说明:
            判断用户是否被ban
        参数:
            :param user_qq: qq号
        """
        logger.debug(f"检测是否被ban", target=user_qq)
        if await cls.check_ban_time(user_qq):
            return True
        else:
            await cls.unban(user_qq)
        return False

    @classmethod
    async def is_super_ban(cls, user_qq: int) -> bool:
        """
        说明:
            判断用户是否被超级用户ban / b了
        参数:
            :param user_qq: qq号
        """
        logger.debug(f"检测是否被超级用户权限封禁", target=user_qq)
        if user := await cls.filter(user_qq=user_qq).first():
            if user.ban_level == 10:
                return True
        return False

    @classmethod
    async def ban(cls, user_qq: int, ban_level: int, duration: int):
        """
        说明:
            ban掉目标用户
        参数:
            :param user_qq: 目标用户qq号
            :param ban_level: 使用ban命令用户的权限
            :param duration:  ban时长，秒
        """
        logger.debug(f"封禁用户，等级:{ban_level}，时长: {duration}", target=user_qq)
        if await cls.filter(user_qq=user_qq).first():
            await cls.unban(user_qq)
        await cls.create(
            user_qq=user_qq,
            ban_level=ban_level,
            ban_time=time.time(),
            duration=duration,
        )

    @classmethod
    async def unban(cls, user_qq: int) -> bool:
        """
        说明:
            unban用户
        参数:
            :param user_qq: qq号
        """
        if user := await cls.filter(user_qq=user_qq).first():
            logger.debug("解除封禁", target=user_qq)
            await user.delete()
            return True
        return False
