from datetime import datetime, timedelta
from typing import List, Literal, Optional, Tuple, Union

from services.db_context import db


class ChatHistory(db.Model):
    __tablename__ = "chat_history"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger())
    text = db.Column(db.Text())
    plain_text = db.Column(db.Text())
    create_time = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    async def add_chat_msg(cls, user_qq: int, group_id: Optional[int], text: str, plain_text: str):
        await cls.create(
            user_qq=user_qq, group_id=group_id, text=text, plain_text=plain_text, create_time=datetime.now()
        )

    @classmethod
    async def get_user_msg(
        cls,
        uid: int,
        msg_type: Optional[Literal["private", "group"]],
        days: Optional[int] = None,
    ) -> List["ChatHistory"]:
        """
        说明:
            获取用户消息
        参数:
            :param uid: 用户qq
            :param msg_type: 消息类型，私聊或群聊
            :param days: 限制日期
        """
        return await cls._get_msg(uid, None, "user", msg_type, days).gino.all()

    @classmethod
    async def get_group_user_msg(
        cls,
        uid: int,
        gid: int,
        limit: int = 10,
        date_scope: Tuple[datetime, datetime] = None,
    ) -> List["ChatHistory"]:
        """
        说明:
            获取群聊指定用户聊天记录
        参数:
            :param uid: qq
            :param gid: 群号
            :param limit: 获取数量
            :param date_scope: 日期范围，默认None为全搜索
        """
        return (
            await cls._get_msg(uid, gid, "group", days=date_scope)
            .limit(limit)
            .gino.all()
        )

    @classmethod
    async def get_group_user_msg_count(cls, uid: int, gid: int) -> Optional[int]:
        """
        说明:
             查询群聊指定用户的聊天记录数量
        参数:
            :param uid: qq
            :param gid: 群号
        """
        if x := await db.first(
            db.text(
                f"SELECT COUNT(id) as sum FROM public.chat_history WHERE user_qq = {uid} AND group_id = {gid}"
            )
        ):
            return x[0]
        return None

    @classmethod
    async def get_group_msg_rank(
        cls,
        gid: int,
        limit: int = 10,
        order: str = "DESC",
        date_scope: Optional[Tuple[datetime, datetime]] = None,
    ) -> Optional[Tuple[int, int]]:
        """
        说明:
            获取排行数据
        参数:
            :param gid: 群号
            :param limit: 获取数量
            :param order: 排序类型，desc，des
            :param date_scope: 日期范围
        """
        sql = f"SELECT user_qq, COUNT(id) as sum FROM public.chat_history WHERE group_id = {gid} "
        if date_scope:
            sql += f"AND create_time BETWEEN '{date_scope[0]}' AND '{date_scope[1]}' "
        sql += f"GROUP BY user_qq ORDER BY sum {order if order and order.upper() != 'DES' else ''} LIMIT {limit}"
        return await db.all(db.text(sql))

    @classmethod
    async def get_group_first_msg_datetime(cls, gid: int) -> Optional[datetime]:
        """
        说明:
            获取群第一条记录消息时间
        参数:
            :param gid:
        """
        if (
            msg := await cls.query.where(cls.group_id == gid)
            .order_by(cls.create_time)
            .gino.first()
        ):
            return msg.create_time
        return None

    @classmethod
    async def get_user_msg_count(
        cls,
        uid: int,
        msg_type: Optional[Literal["private", "group"]],
        days: Optional[int] = None,
    ) -> int:
        """
        说明:
            获取用户消息数量
        参数:
            :param uid: 用户qq
            :param msg_type: 消息类型，私聊或群聊
            :param days: 限制日期
        """
        return (
            await cls._get_msg(uid, None, "user", msg_type, days, True).gino.first()
        )[0]

    @classmethod
    async def get_group_msg(
        cls,
        gid: int,
        days: Optional[int] = None,
    ) -> List["ChatHistory"]:
        """
        说明:
            获取群聊消息
        参数:
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
        说明:
            获取群聊消息数量
        参数:
            :param gid: 用户qq
            :param days: 限制日期
        """
        return (await cls._get_msg(None, gid, "group", None, days, True).gino.first())[
            0
        ]

    @classmethod
    def _get_msg(
        cls,
        uid: Optional[int],
        gid: Optional[int],
        type_: Literal["user", "group"],
        msg_type: Optional[Literal["private", "group"]] = None,
        days: Optional[Union[int, Tuple[datetime, datetime]]] = None,
        is_select_count: bool = False,
    ):
        """
        说明:
            获取消息查询query
        参数:
            :param uid: 用户qq
            :param gid: 群号
            :param type_: 类型，私聊或群聊
            :param msg_type: 消息类型，用户或群聊
            :param days: 限制日期
        """
        if is_select_count:
            setattr(ChatHistory, "count", db.func.count(cls.id).label("count"))
            query = cls.select("count")
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
            if uid:
                query = query.where(cls.user_qq == uid)
        if days:
            if isinstance(days, int):
                query = query.where(
                    cls.create_time >= datetime.now() - timedelta(days=days)
                )
            elif isinstance(days, tuple):
                query = query.where(cls.create_time >= days[0]).where(
                    cls.create_time <= days[1]
                )
        return query
