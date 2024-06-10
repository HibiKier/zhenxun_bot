from tortoise import fields

from zhenxun.services.db_context import Model


class RussianUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
    """群聊id"""
    win_count = fields.IntField(default=0)
    """胜利次数"""
    fail_count = fields.IntField(default=0)
    """失败次数"""
    make_money = fields.IntField(default=0)
    """赢得金币"""
    lose_money = fields.IntField(default=0)
    """输得金币"""
    winning_streak = fields.IntField(default=0)
    """当前连胜"""
    losing_streak = fields.IntField(default=0)
    """当前连败"""
    max_winning_streak = fields.IntField(default=0)
    """最大连胜"""
    max_losing_streak = fields.IntField(default=0)
    """最大连败"""

    class Meta:
        table = "russian_users"
        table_description = "俄罗斯轮盘数据表"
        unique_together = ("user_id", "group_id")

    @classmethod
    async def add_count(cls, user_id: str, group_id: str, itype: str):
        """添加用户输赢次数

        说明:
            user_id: 用户id
            group_id: 群号
            itype: 输或赢 'win' or 'lose'
        """
        user, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        if itype == "win":
            _max = (
                user.max_winning_streak
                if user.max_winning_streak > user.winning_streak + 1
                else user.winning_streak + 1
            )
            user.win_count = user.win_count + 1
            user.winning_streak = user.winning_streak + 1
            user.losing_streak = 0
            user.max_winning_streak = _max
            await user.save(
                update_fields=[
                    "win_count",
                    "winning_streak",
                    "losing_streak",
                    "max_winning_streak",
                ]
            )
        elif itype == "lose":
            _max = (
                user.max_losing_streak
                if user.max_losing_streak > user.losing_streak + 1
                else user.losing_streak + 1
            )
            user.fail_count = user.fail_count + 1
            user.losing_streak = user.losing_streak + 1
            user.winning_streak = 0
            user.max_losing_streak = _max
            await user.save(
                update_fields=[
                    "fail_count",
                    "winning_streak",
                    "losing_streak",
                    "max_losing_streak",
                ]
            )
        return user

    @classmethod
    async def money(cls, user_id: str, group_id: str, itype: str, count: int):
        """添加用户输赢金钱

        参数:
            user_id: 用户id
            group_id: 群号
            itype: 输或赢 'win' or 'lose'
            count: 金钱数量
        """
        user, _ = await cls.get_or_create(user_id=str(user_id), group_id=group_id)
        if itype == "win":
            user.make_money = user.make_money + count
        elif itype == "lose":
            user.lose_money = user.lose_money + count
        await user.save(update_fields=["make_money", "lose_money"])

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE russian_users RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE russian_users ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE russian_users ALTER COLUMN group_id TYPE character varying(255);",
        ]
