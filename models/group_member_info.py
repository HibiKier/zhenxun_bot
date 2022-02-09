from datetime import datetime
from configs.config import Config
from services.db_context import db
from typing import List, Optional


class GroupInfoUser(db.Model):
    __tablename__ = "group_info_users"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    user_name = db.Column(db.Unicode(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    user_join_time = db.Column(db.DateTime(), nullable=False)
    nickname = db.Column(db.Unicode())
    uid = db.Column(db.BigInteger())

    _idx1 = db.Index("info_group_users_idx1", "user_qq", "group_id", unique=True)

    @classmethod
    async def add_member_info(
        cls,
        user_qq: int,
        group_id: int,
        user_name: str,
        user_join_time: datetime,
        uid: Optional[int] = None,
    ) -> bool:
        """
        说明：
            添加群内用户信息
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param user_name: 用户名称
            :param user_join_time: 入群时间
            :param uid: 用户唯一 id（自动生成）
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        try:
            if not await query.gino.first():
                await cls.create(
                    user_qq=user_qq,
                    user_name=user_name,
                    group_id=group_id,
                    user_join_time=user_join_time,
                    uid=uid
                )
            return True
        except Exception:
            return False

    @classmethod
    async def get_member_info(
        cls, user_qq: int, group_id: int
    ) -> "GroupInfoUser":
        """
        说明：
            查询群员信息
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        return await query.gino.first()

    @classmethod
    async def delete_member_info(cls, user_qq: int, group_id: int) -> bool:
        """
        说明：
            删除群员信息
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        try:
            if user is None:
                return True
            else:
                await cls.delete.where(
                    (cls.user_qq == user_qq) & (cls.group_id == group_id)
                ).gino.status()
                return True
        except Exception:
            return False

    @classmethod
    async def get_group_member_id_list(cls, group_id: int) -> List[int]:
        """
        说明：
            获取该群所有用户qq
        参数：
            :param group_id: 群号
        """
        member_list = []
        query = cls.query.where((cls.group_id == group_id))
        for user in await query.gino.all():
            member_list.append(user.user_qq)
        return member_list

    @classmethod
    async def set_group_member_nickname(
        cls, user_qq: int, group_id: int, nickname: str
    ) -> bool:
        """
        说明：
            设置群员在该群内的昵称
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param nickname: 昵称
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        user = await query.with_for_update().gino.first()
        if user:
            await user.update(nickname=nickname).apply()
            return True
        return False

    @classmethod
    async def get_user_all_group(cls, user_qq: int) -> List[int]:
        """
        说明：
            获取该用户所在的所有群聊
        参数：
            :param user_qq: 用户qq
        """
        query = await cls.query.where(cls.user_qq == user_qq).gino.all()
        if query:
            query = [x.group_id for x in query]
        return query

    @classmethod
    async def get_group_member_nickname(cls, user_qq: int, group_id: int) -> str:
        """
        说明：
            获取用户在该群的昵称
        参数：
            :param user_qq: qq号
            :param group_id: 群号
        """
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
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
    async def get_group_member_uid(cls, user_qq: int, group_id: int) -> Optional[str]:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_id == group_id)
        )
        user = await query.gino.first()
        _max_uid = cls.query.where((cls.user_qq == 114514) & (cls.group_id == 114514)).with_for_update()
        _max_uid_user = await _max_uid.gino.first()
        _max_uid = _max_uid_user.uid
        if not user or not user.uid:
            all_user = await cls.query.where(cls.user_qq == user_qq).gino.all()
            for x in all_user:
                if x.uid:
                    return x.uid
            else:
                if not user:
                    await GroupInfoUser.add_member_info(user_qq, group_id, '', datetime.min)
                    user = await cls.query.where(
                        (cls.user_qq == user_qq) & (cls.group_id == group_id)
                    ).gino.first()
                await user.update(
                    uid=_max_uid + 1,
                ).apply()
                await _max_uid_user.update(
                    uid=_max_uid + 1,
                ).apply()

        return user.uid if user and user.uid else None

