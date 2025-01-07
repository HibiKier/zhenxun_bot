from datetime import datetime

from tortoise import fields

from zhenxun.services.db_context import Model


class SignGroupUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
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

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "sign_group_users"
        table_description = "群员签到数据表"
        unique_together = ("user_id", "group_id")

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
        cls, group_id: int | str
    ) -> tuple[list[str], list[float], list[str]]:
        """
        说明:
            获取该群所有用户 id 及对应 好感度
        参数:
            :param group_id: 群号
        """
        if group_id:
            query = cls.filter(group_id=str(group_id))
        else:
            query = cls
        value_list = await query.all().values_list("user_id", "group_id", "impression")  # type: ignore
        user_list = []
        group_list = []
        impression_list = []
        for value in value_list:
            user_list.append(value[0])
            group_list.append(value[1])
            impression_list.append(float(value[2]))
        return user_list, impression_list, group_list

    @classmethod
    async def _run_script(cls):
        return [
            # 将user_id改为user_id
            "ALTER TABLE sign_group_users RENAME COLUMN user_qq TO user_id;",
            "ALTER TABLE sign_group_users "
            "ALTER COLUMN user_id TYPE character varying(255);",
            # 将user_id字段类型改为character varying(255)
            "ALTER TABLE sign_group_users "
            "ALTER COLUMN group_id TYPE character varying(255);",
        ]
