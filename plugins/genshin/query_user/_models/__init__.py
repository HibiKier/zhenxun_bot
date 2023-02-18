import random
from datetime import datetime, timedelta
from typing import Optional

import pytz
from tortoise import fields
from tortoise.contrib.postgres.functions import Random

from services.db_context import Model


class Genshin(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    uid = fields.BigIntField()
    """uid"""
    mys_id: int = fields.BigIntField(null=True)
    """米游社id"""
    cookie: str = fields.TextField(default="")
    """米游社cookie"""
    auto_sign = fields.BooleanField(default=False)
    """是否自动签到"""
    today_query_uid = fields.TextField(default="")
    """cookie今日查询uid"""
    auto_sign_time = fields.DatetimeField(null=True)
    """签到日期时间"""
    resin_remind = fields.BooleanField(default=False)
    """树脂提醒"""
    resin_recovery_time = fields.DatetimeField(null=True)
    """满树脂提醒日期"""
    bind_group: int = fields.BigIntField(null=True)
    """发送提示 绑定群聊"""
    login_ticket = fields.TextField(default="")
    """login_ticket"""
    stuid: str = fields.TextField(default="")
    """stuid"""
    stoken: str = fields.TextField(default="")
    """stoken"""

    class Meta:
        table = "genshin"
        table_description = "原神数据表"
        unique_together = ("user_qq", "uid")

    @classmethod
    async def random_sign_time(cls, uid: int) -> Optional[datetime]:
        """
        说明:
            随机签到时间
        说明:
            :param uid: uid
        """
        user = await cls.get_or_none(uid=uid)
        if user and user.cookie:
            if user.auto_sign_time and user.auto_sign_time.astimezone(
                pytz.timezone("Asia/Shanghai")
            ) - timedelta(seconds=2) >= datetime.now(pytz.timezone("Asia/Shanghai")):
                return user.auto_sign_time.astimezone(pytz.timezone("Asia/Shanghai"))
            hours = int(str(datetime.now()).split()[1].split(":")[0])
            minutes = int(str(datetime.now()).split()[1].split(":")[1])
            date = (
                datetime.now()
                + timedelta(days=1)
                - timedelta(hours=hours)
                - timedelta(minutes=minutes - 1)
            )
            random_hours = random.randint(0, 22)
            random_minutes = random.randint(1, 59)
            date += timedelta(hours=random_hours) + timedelta(minutes=random_minutes)
            user.auto_sign_time = date
            await user.save(update_fields=["auto_sign_time"])
            return date
        return None

    @classmethod
    async def random_cookie(cls, uid: int) -> Optional[str]:
        """
        说明:
            随机获取查询角色信息cookie
        参数:
            :param uid: 原神uid
        """
        # 查找用户今日是否已经查找过，防止重复
        user = await cls.get_or_none(today_query_uid__contains=str(uid))
        if user:
            return user.cookie
        for user in await cls.filter(cookie__not="").annotate(rand=Random()).all():
            if not user.today_query_uid or len(user.today_query_uid[:-1].split()) < 30:
                user.today_query_uid = user.today_query_uid + f"{uid} "
                await user.save(update_fields=["today_query_uid"])
                return user.cookie
        return None
