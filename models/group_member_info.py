from datetime import datetime

from services.db_context import db
from typing import List


class GroupInfoUser(db.Model):
    __tablename__ = "group_info_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    user_name = db.Column(db.Unicode(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), nullable=False)
    user_join_time = db.Column(db.DateTime(), nullable=False)
    nickname = db.Column(db.Unicode())

    _idx1 = db.Index("info_group_users_idx1", "user_qq", "belonging_group", unique=True)

    @classmethod
    async def add_member_info(
        cls,
        user_qq: int,
        belonging_group: int,
        user_name: str,
        user_join_time: datetime,
    ) -> bool:
        """
        说明：
            添加群内用户信息
        参数：
            :param user_qq: qq号
            :param belonging_group: 群号
            :param user_name: 用户名称
            :param user_join_time: 入群时间
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        try:
            if not await query.gino.first():
                await cls.create(
                    user_qq=user_qq,
                    user_name=user_name,
                    belonging_group=belonging_group,
                    user_join_time=user_join_time,
                )
            return True
        except Exception:
            return False

    @classmethod
    async def get_member_info(
        cls, user_qq: int, belonging_group: int
    ) -> "GroupInfoUser":
        """
        说明：
            查询群员信息
        参数：
            :param user_qq: qq号
            :param belonging_group: 群号
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        return await query.gino.first()

    @classmethod
    async def delete_member_info(cls, user_qq: int, belonging_group: int) -> bool:
        """
        说明：
            删除群员信息
        参数：
            :param user_qq: qq号
            :param belonging_group: 群号
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        try:
            if user is None:
                return True
            else:
                await cls.delete.where(
                    (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
                ).gino.status()
                return True
        except Exception:
            return False

    @classmethod
    async def get_group_member_id_list(cls, belonging_group: int) -> List[int]:
        """
        说明：
            获取该群所有用户qq
        参数：
            :param belonging_group: 群号
        """
        member_list = []
        query = cls.query.where((cls.belonging_group == belonging_group))
        for user in await query.gino.all():
            member_list.append(user.user_qq)
        return member_list

    @classmethod
    async def set_group_member_nickname(
        cls, user_qq: int, belonging_group: int, nickname: str
    ) -> bool:
        """
        说明：
            设置群员在该群内的昵称
        参数：
            :param user_qq: qq号
            :param belonging_group: 群号
            :param nickname: 昵称
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        user = await query.with_for_update().gino.first()
        if user:
            await user.update(nickname=nickname).apply()
            return True
        return False

    @classmethod
    async def get_group_member_nickname(cls, user_qq: int, belonging_group: int) -> str:
        """
        说明：
            获取用户在该群的昵称
        参数：
            :param user_qq: qq号
            :param belonging_group: 群号
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        user = await query.gino.first()
        if user:
            if user.nickname:
                return user.nickname
        return ""
