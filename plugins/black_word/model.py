from datetime import datetime, timedelta
from typing import List, Optional

from tortoise import fields

from services.db_context import Model


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

    class Meta:
        table = "black_word"
        table_description = "惩罚机制数据表"

    @classmethod
    async def set_user_punish(
        cls,
        user_id: str,
        punish: str,
        black_word: Optional[str] = None,
        id_: Optional[int] = None,
    ) -> bool:
        """
        说明:
            设置处罚
        参数:
            :param user_id: 用户id
            :param punish: 处罚
            :param black_word: 黑名单词汇
            :param id_: 记录下标
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
        cls, user_id: str, days: int = 7, punish_level: Optional[int] = None
    ) -> int:
        """
        说明:
            获取用户规定周期内的犯事次数
        参数:
            :param user_id: 用户id
            :param days: 周期天数
            :param punish_level: 惩罚等级
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
    async def get_user_punish_level(cls, user_id: str, days: int = 7) -> Optional[int]:
        """
        说明:
            获取用户最近一次的惩罚记录等级
        参数:
            :param user_id: 用户id
            :param days: 周期天数
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
        user_id: Optional[str],
        group_id: Optional[str],
        date: Optional[datetime],
        date_type: str = "=",
    ) -> List["BlackWord"]:
        """
        说明:
            通过指定条件查询数据
        参数:
            :param user_id: 用户id
            :param group_id: 群号
            :param date: 日期
            :param date_type: 日期查询类型
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
        return await query.all().order_by("id")  # type: ignore

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE black_word RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE black_word ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE black_word ALTER COLUMN group_id TYPE character varying(255);",
        ]
