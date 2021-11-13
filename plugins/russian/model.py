from services.db_context import db
from typing import List


class RussianUser(db.Model):
    __tablename__ = "russian_users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    win_count = db.Column(db.Integer(), default=0)
    fail_count = db.Column(db.Integer(), default=0)
    make_money = db.Column(db.Integer(), default=0)
    lose_money = db.Column(db.Integer(), default=0)
    winning_streak = db.Column(db.Integer(), default=0)
    losing_streak = db.Column(db.Integer(), default=0)
    max_winning_streak = db.Column(db.Integer(), default=0)
    max_losing_streak = db.Column(db.Integer(), default=0)

    _idx1 = db.Index("russian_group_users_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def ensure(cls, user_qq: int, group_id: int) -> "RussianUser":
        """
        说明：
            获取用户对象
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        user = (
            await cls.query.where((cls.user_qq == user_qq) & (cls.group_id == group_id))
            .with_for_update()
            .gino.first()
        )
        return user or await cls.create(user_qq=user_qq, group_id=group_id)

    @classmethod
    async def add_count(cls, user_qq: int, group_id: int, itype: str) -> bool:
        """
        说明：
            添加用户输赢次数
        说明：
            :param user_qq: qq号
            :param group_id: 群号
            :param itype: 输或赢 'win' or 'lose'
        """
        try:
            user = (
                await cls.query.where(
                    (cls.user_qq == user_qq) & (cls.group_id == group_id)
                )
                .with_for_update()
                .gino.first()
            )
            if not user:
                user = await cls.create(user_qq=user_qq, group_id=group_id)
            if itype == "win":
                _max = (
                    user.max_winning_streak
                    if user.max_winning_streak > user.winning_streak + 1
                    else user.winning_streak + 1
                )
                await user.update(
                    win_count=user.win_count + 1,
                    winning_streak=user.winning_streak + 1,
                    losing_streak=0,
                    max_winning_streak=_max
                ).apply()
            elif itype == "lose":
                _max = (
                    user.max_losing_streak
                    if user.max_losing_streak > user.losing_streak + 1
                    else user.losing_streak + 1
                )
                await user.update(
                    fail_count=user.fail_count + 1,
                    losing_streak=user.losing_streak + 1,
                    winning_streak=0,
                    max_losing_streak=_max,
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def money(cls, user_qq: int, group_id: int, itype: str, count: int) -> bool:
        """
        说明：
            添加用户输赢金钱
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param itype: 输或赢 'win' or 'lose'
            :param count: 金钱数量
        """
        try:
            user = (
                await cls.query.where(
                    (cls.user_qq == user_qq) & (cls.group_id == group_id)
                )
                .with_for_update()
                .gino.first()
            )
            if not user:
                user = await cls.create(user_qq=user_qq, group_id=group_id)
            if itype == "win":
                await user.update(
                    make_money=user.make_money + count,
                ).apply()
            elif itype == "lose":
                await user.update(
                    lose_money=user.lose_money + count,
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def get_all_user(cls, group_id: int) -> List["RussianUser"]:
        """
        说明：
            获取该群所有用户对象
        参数：
        :param group_id: 群号
        """
        users = await cls.query.where((cls.group_id == group_id)).gino.all()
        return users
