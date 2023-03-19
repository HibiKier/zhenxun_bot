from datetime import datetime
from typing import List, Optional, Set

from tortoise import fields

from configs.config import Config
from services.db_context import Model
from services.log import logger


class GroupInfoUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    user_name = fields.CharField(255, default="")
    """用户昵称"""
    group_id = fields.BigIntField()
    """群聊id"""
    user_join_time: datetime = fields.DatetimeField(null=True)
    """用户入群时间"""
    nickname = fields.CharField(255, null=True)
    """群聊昵称"""
    uid = fields.BigIntField(null=True)
    """用户uid"""

    class Meta:
        table = "group_info_users"
        table_description = "群员信息数据表"
        unique_together = ("user_qq", "group_id")

    @classmethod
    async def get_group_member_id_list(cls, group_id: int) -> Set[int]:
        """
        说明:
            获取该群所有用户qq
        参数:
            :param group_id: 群号
        """
        return set(
            await cls.filter(group_id=group_id).values_list("user_qq", flat=True)
        )  # type: ignore

    @classmethod
    async def set_user_nickname(cls, user_qq: int, group_id: int, nickname: str):
        """
        说明:
            设置群员在该群内的昵称
        参数:
            :param user_qq: qq号
            :param group_id: 群号
            :param nickname: 昵称
        """
        await cls.update_or_create(
            user_qq=user_qq,
            group_id=group_id,
            defaults={"nickname": nickname},
        )

    @classmethod
    async def get_user_all_group(cls, user_qq: int) -> List[int]:
        """
        说明:
            获取该用户所在的所有群聊
        参数:
            :param user_qq: 用户qq
        """
        return list(
            await cls.filter(user_qq=user_qq).values_list("group_id", flat=True)
        )  # type: ignore

    @classmethod
    async def get_user_nickname(cls, user_qq: int, group_id: int) -> str:
        """
        说明:
            获取用户在该群的昵称
        参数:
            :param user_qq: qq号
            :param group_id: 群号
        """
        if user := await cls.get_or_none(user_qq=user_qq, group_id=group_id):
            if user.nickname:
                nickname = ""
                if black_word := Config.get_config("nickname", "BLACK_WORD"):
                    for x in user.nickname:
                        nickname += "*" if x in black_word else x
                    return nickname
                return user.nickname
        return ""

    @classmethod
    async def get_group_member_uid(cls, user_qq: int, group_id: int) -> Optional[int]:
        logger.debug(
            f"GroupInfoUser 尝试获取 用户[<u><e>{user_qq}</e></u>] 群聊[<u><e>{group_id}</e></u>] UID"
        )
        user, _ = await cls.get_or_create(user_qq=user_qq, group_id=group_id)
        _max_uid_user, _ = await cls.get_or_create(user_qq=114514, group_id=114514)
        _max_uid = _max_uid_user.uid
        if not user.uid:
            all_user = await cls.filter(user_qq=user_qq).all()
            for x in all_user:
                if x.uid:
                    return x.uid
            user.uid = _max_uid + 1
            _max_uid_user.uid = _max_uid + 1
            await cls.bulk_update([user, _max_uid_user], ["uid"])
        logger.debug(
            f"GroupInfoUser 获取 用户[<u><e>{user_qq}</e></u>] 群聊[<u><e>{group_id}</e></u>] UID: {user.uid}"
        )
        return user.uid

    @classmethod
    async def _run_script(cls):
        return [
            "alter table group_info_users alter user_join_time drop not null;",  # 允许 user_join_time 为空
            "ALTER TABLE group_info_users ALTER COLUMN user_join_time TYPE timestamp with time zone USING user_join_time::timestamp with time zone;",
        ]
