from services.db_context import db
from configs.config import Config


class FriendUser(db.Model):
    __tablename__ = "friend_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger(), nullable=False)
    user_name = db.Column(db.Unicode(), nullable=False, default="")
    nickname = db.Column(db.Unicode())

    _idx1 = db.Index("friend_users_idx1", "user_id", unique=True)

    @classmethod
    async def get_user_name(cls, user_id: int) -> str:
        """
        说明：
            获取好友用户名称
        参数：
            :param user_id: qq号
        """
        query = cls.query.where(cls.user_id == user_id)
        user = await query.gino.first()
        if user:
            return user.user_name
        else:
            return ""

    @classmethod
    async def add_friend_info(cls, user_id: int, user_name: str) -> bool:
        """
        说明：
            添加好友信息
        参数：
            :param user_id: qq号
            :param user_name: 用户名称
        """
        try:
            query = cls.query.where(cls.user_id == user_id)
            user = await query.with_for_update().gino.first()
            if not user:
                await cls.create(
                    user_id=user_id,
                    user_name=user_name,
                )
            else:
                await user.update(
                    user_name=user_name,
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def delete_friend_info(cls, user_id: int) -> bool:
        """
        说明：
            删除好友信息
        参数：
            :param user_id: qq号
        """
        try:
            query = cls.query.where(cls.user_id == user_id)
            user = await query.with_for_update().gino.first()
            if user:
                await user.delete()
            return True
        except Exception:
            return False

    @classmethod
    async def get_friend_nickname(cls, user_id: int) -> str:
        """
        说明：
            获取用户昵称
        参数：
            :param user_id: qq号
        """
        query = cls.query.where(cls.user_id == user_id)
        user = await query.gino.first()
        if user:
            if user.nickname:
                _tmp = ""
                black_word = Config.get_config("nickname", "BLACK_WORD")
                if black_word:
                    for x in user.nickname:
                        _tmp += "*" if x in black_word else x
                return _tmp
        return ""

    @classmethod
    async def set_friend_nickname(cls, user_id: int, nickname: str) -> bool:
        """
        说明：
            设置用户昵称
        参数：
            :param user_id: qq号
            :param nickname: 昵称
        """
        try:
            query = cls.query.where(cls.user_id == user_id)
            user = await query.with_for_update().gino.first()
            if not user:
                await cls.create(
                    user_id=user_id,
                    nickname=nickname,
                )
            else:
                await user.update(
                    nickname=nickname,
                ).apply()
            return True
        except Exception:
            return False
