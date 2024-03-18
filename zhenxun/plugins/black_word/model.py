from datetime import datetime, timedelta
from email.policy import default

import pytz
from tortoise import fields

from zhenxun.services.db_context import Model


class BlackWord(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255, null=True)
    """群聊id"""
    plant_text = fields.TextField()
    """检测文本"""
    black_word = fields.TextField()
    """黑名单词语"""
    punish = fields.TextField(default="")
    """惩罚内容"""
    punish_level = fields.IntField()
    """惩罚等级"""
    create_time = fields.DatetimeField(auto_now_add=True)
    """创建时间"""
    platform = fields.CharField(255, null=True)
    """平台"""

    class Meta:
        table = "black_word"
        table_description = "惩罚机制数据表"

    @classmethod
    async def set_user_punish(
        cls,
        user_id: str,
        punish: str,
        black_word: str | None = None,
        id_: int | None = None,
    ) -> bool:
        """设置处罚

        参数:
            user_id: 用户id
            punish: 处罚
            black_word: 黑名单词汇
            id_: 记录下标
        """
        user = None
        if (not black_word and id_ is None) or not punish:
            return False
        if black_word:
            user = (
                await cls.filter(user_id=user_id, black_word=black_word, punish="")
                .order_by("id")
                .first()
            )
        elif id_ is not None:
            user_list = await cls.filter(user_id=user_id).order_by("id").all()
            if len(user_list) == 0 or (id_ < 0 or id_ > len(user_list)):
                return False
            user = user_list[id_]
        if not user:
            return False
        user.punish = f"{user.punish}{punish} "
        await user.save(update_fields=["punish"])
        return True

    @classmethod
    async def get_user_count(
        cls, user_id: str, days: int = 7, punish_level: int | None = None
    ) -> int:
        """获取用户规定周期内的犯事次数

        参数:
            user_id: 用户id
            days: 周期天数
            punish_level: 惩罚等级
        """
        query = cls.filter(
            user_id=user_id,
            create_time__gte=datetime.now() - timedelta(days=days),
            punish_level__not_in=[-1],
        )
        if punish_level is not None:
            query = query.filter(punish_level=punish_level)
        return await query.count()

    @classmethod
    async def get_user_punish_level(cls, user_id: str, days: int = 7) -> int | None:
        """获取用户最近一次的惩罚记录等级

        参数:
            user_id: 用户id
            days: 周期天数
        """
        if (
            user := await cls.filter(
                user_id=user_id,
                create_time__gte=datetime.now() - timedelta(days=days),
            )
            .order_by("id")
            .first()
        ):
            return user.punish_level
        return None

    @classmethod
    async def get_black_data(
        cls,
        user_id: str | None,
        group_id: str | None,
        date: datetime | None,
        date_type: str = "=",
    ) -> list["BlackWord"]:
        """通过指定条件查询数据

        参数:
            user_id: 用户id
            group_id: 群号
            date: 日期
            date_type: 日期查询类型
        """
        query = cls
        if user_id:
            query = query.filter(user_id=user_id)
        if group_id:
            query = query.filter(group_id=group_id)
        if date:
            if date_type == "=":
                query = query.filter(
                    create_time__range=[date, date + timedelta(days=1)]
                )
            elif date_type == ">":
                query = query.filter(create_time__gte=date)
            elif date_type == "<":
                query = query.filter(create_time__lte=date)
        data_list = await query.all().order_by("id")
        for data in data_list:
            data.create_time = data.create_time.astimezone(
                pytz.timezone("Asia/Shanghai")
            )
        return data_list  # type: ignore

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE black_word RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE black_word ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE black_word ALTER COLUMN group_id TYPE character varying(255);",
            "ALTER TABLE black_word ADD COLUMN platform character varying(255);",
        ]
