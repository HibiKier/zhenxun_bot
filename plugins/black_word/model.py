from services.db_context import db
from typing import Optional, List
from datetime import datetime, timedelta


class BlackWord(db.Model):
    __tablename__ = "black_word"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_qq = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    group_id = db.Column(db.BigInteger())
    plant_text = db.Column(db.String())
    black_word = db.Column(db.String())
    punish = db.Column(db.String(), default="")
    punish_level = db.Column(db.Integer())
    create_time = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    async def add_user_black_word(
        cls,
        user_qq: int,
        group_id: Optional[int],
        black_word: str,
        plant_text: str,
        punish_level: int,
    ):
        """
        说明：
            添加用户发送的敏感词
        参数：
            :param user_qq: 用户id
            :param group_id: 群号
            :param black_word: 黑名单词汇
            :param plant_text: 消息文本
            :param punish_level: 惩罚等级
        """
        await cls.create(
            user_qq=user_qq,
            group_id=group_id,
            plant_text=plant_text,
            black_word=black_word,
            punish_level=punish_level,
            create_time=datetime.now(),
        )

    @classmethod
    async def set_user_punish(
        cls,
        user_qq: int,
        punish: str,
        black_word: Optional[str] = None,
        id_: Optional[int] = None,
    ) -> bool:
        """
        说明：
            设置处罚
        参数：
            :param user_qq: 用户id
            :param punish: 处罚
            :param black_word: 黑名单词汇
            :param id_: 记录下标
        """
        user = None
        if (not black_word and not id_) or not punish:
            return False
        query = cls.query.where(cls.user_qq == user_qq).with_for_update()
        if black_word:
            user = await query.where(cls.black_word == black_word).order_by(cls.id.desc()).gino.first()
        elif id_:
            user_list = await query.gino.all()
            if len(user_list) == 0 or (id_ < 0 or id_ > len(user_list)):
                return False
            user = user_list[id_]
        if not user:
            return False
        await user.update(punish=cls.punish + punish + " ").apply()
        return True

    @classmethod
    async def get_user_count(
        cls, user_qq: int, days: int = 7, punish_level: Optional[int] = None
    ) -> int:
        """
        说明：
            获取用户规定周期内的犯事次数
        参数：
            :param user_qq: 用户qq
            :param days: 周期天数
            :param punish_level: 惩罚等级
        """
        setattr(BlackWord, "count", db.func.count(cls.id).label("count"))
        query = cls.select("count").where(
            (cls.user_qq == user_qq)
            & (cls.punish_level != -1)
            & (cls.create_time > datetime.now() - timedelta(days=days))
        )
        if punish_level is not None:
            query = query.where(cls.punish_level == punish_level)
        return (await query.gino.first())[0]

    @classmethod
    async def get_user_punish_level(cls, user_qq: int, days: int = 7) -> Optional[int]:
        """
        说明：
            获取用户最近一次的惩罚记录等级
        参数：
            :param user_qq: 用户qq
            :param days: 周期天数
        """
        if (
            query := await cls.query.where(cls.user_qq == user_qq)
            .where(cls.create_time > datetime.now() - timedelta(days=days))
            .order_by(cls.id.desc())
            .gino.first()
        ):
            return query.punish_level
        return None

    @classmethod
    async def get_black_data(
        cls,
        user_qq: Optional[int],
        group_id: Optional[int],
        date: Optional[datetime],
        date_type: str = "=",
    ) -> List["BlackWord"]:
        """
        说明：
            通过指定条件查询数据
        参数：
            :param user_qq: 用户qq
            :param group_id: 群号
            :param date: 日期
            :param date_type: 日期查询类型
        """
        query = cls.query
        if user_qq:
            query = query.where(cls.user_qq == user_qq)
        if group_id:
            query = query.where(cls.group_id == group_id)
        if date:
            if date_type == "=":
                query = query.where(cls.create_time == date)
            elif date_type == ">":
                query = query.where(cls.create_time > date)
            elif date_type == "<":
                query = query.where(cls.create_time < date)
        return await query.gino.all()
