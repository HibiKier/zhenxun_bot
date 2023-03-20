from datetime import datetime
from typing import List, Literal, Optional, Tuple

from tortoise import fields

from services.db_context import Model


class SignGroupUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField()
    """群聊id"""
    checkin_count = fields.IntField(default=0)
    """签到次数"""
    checkin_time_last = fields.DatetimeField(default=datetime.min)
    """最后签到时间"""
    impression = fields.DecimalField(10, 3, default=0)
    """好感度"""
    add_probability = fields.DecimalField(10, 3, default=0)
    """双倍签到增加概率"""
    specify_probability = fields.DecimalField(10, 3, default=0)
    """使用指定双倍概率"""
    # specify_probability = fields.DecimalField(10, 3, default=0)

    class Meta:
        table = "sign_group_users"
        table_description = "群员签到数据表"
        unique_together = ("user_qq", "group_id")

    @classmethod
    async def sign(cls, user: "SignGroupUser", impression: float):
        """
        说明:
            签到
        说明:
            :param user: 用户
            :param impression: 增加的好感度
        """
        user.checkin_time_last = datetime.now()
        user.checkin_count = user.checkin_count + 1
        user.add_probability = 0
        user.specify_probability = 0
        user.impression = float(user.impression) + impression
        await user.save()

    @classmethod
    async def get_all_impression(
        cls, group_id: Optional[int]
    ) -> Tuple[List[int], List[int], List[float]]:
        """
        说明:
            获取该群所有用户 id 及对应 好感度
        参数:
            :param group_id: 群号
        """
        if group_id:
            query = cls.filter(group_id=group_id)
        else:
            query = cls
        value_list = await query.all().values_list("user_qq", "group_id", "impression")  # type: ignore
        qq_list = []
        group_list = []
        impression_list = []
        for value in value_list:
            qq_list.append(value[0])
            group_list.append(value[1])
            impression_list.append(float(value[2]))
        return qq_list, impression_list, group_list
