from datetime import datetime, timedelta
from typing import List, Literal, Optional

from services.db_context import db


class ChatHistory(db.Model):
    __tablename__ = "chat_history"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger())
    text = db.Column(db.Text())
    create_time = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    async def add_chat_msg(cls, user_qq: int, group_id: Optional[int], text: str):
        await cls.create(
            user_qq=user_qq, group_id=group_id, text=text, create_time=datetime.now()
        )

    @classmethod
    async def get_user_msg(
        cls,
        uid: int,
        msg_type: Optional[Literal["private", "group"]],
        days: Optional[int] = None,
    ) -> List["ChatHistory"]:
        """
        说明：
            获取用户消息
        参数：
            :param uid: 用户qq
            :param msg_type: 消息类型，私聊或群聊
            :param days: 限制日期
        """
        return await cls._get_msg(uid, None, "user", msg_type, days).gino.all()

    @classmethod
    async def get_user_msg_count(
        cls,
        uid: int,
        msg_type: Optional[Literal["private", "group"]],
        days: Optional[int] = None,
    ) -> int:
        """
        说明：
            获取用户消息数量
        参数：
            :param uid: 用户qq
            :param msg_type: 消息类型，私聊或群聊
            :param days: 限制日期
        """
        return (await cls._get_msg(uid, None, "user", msg_type, days, True).gino.first())[0]

    @classmethod
    async def get_group_msg(
        cls,
        gid: int,
        days: Optional[int] = None,
    ) -> List["ChatHistory"]:
        """
        说明：
            获取群聊消息
        参数：
            :param gid: 用户qq
            :param days: 限制日期
        """
        return await cls._get_msg(None, gid, "group", None, days).gino.all()

    @classmethod
    async def get_group_msg_count(
        cls,
        gid: int,
        days: Optional[int] = None,
    ) -> List["ChatHistory"]:
        """
        说明：
            获取群聊消息数量
        参数：
            :param gid: 用户qq
            :param days: 限制日期
        """
        return (await cls._get_msg(None, gid, "group", None, days, True).gino.first())[0]

    @classmethod
    def _get_msg(
        cls,
        uid: Optional[int],
        gid: Optional[int],
        type_: Literal["user", "group"],
        msg_type: Optional[Literal["private", "group"]],
        days: Optional[int],
        is_select_count: bool = False
    ):
        """
        说明：
            获取消息查询query
        参数：
            :param uid: 用户qq
            :param gid: 群号
            :param type_: 类型，私聊或群聊
            :param msg_type: 消息类型，用户或群聊
            :param days: 限制日期
        """
        if is_select_count:
            setattr(ChatHistory, 'count', db.func.count(cls.id).label('count'))
            query = cls.select('count')
        else:
            query = cls.query
        if type_ == "user":
            query = query.where(cls.user_qq == uid)
            if msg_type == "private":
                query = query.where(cls.group_id == None)
            elif msg_type == "group":
                query = query.where(cls.group_id != None)
        else:
            query = query.where(cls.group_id == gid)
        if days:
            query = query.where(
                cls.create_time >= datetime.now() - timedelta(days=days)
            )
        return query
