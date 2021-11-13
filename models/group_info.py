from services.db_context import db
from services.log import logger
from typing import List, Optional


class GroupInfo(db.Model):
    __tablename__ = "group_info"

    group_id = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    group_name = db.Column(db.Unicode(), nullable=False, default="")
    max_member_count = db.Column(db.Integer(), nullable=False, default=0)
    member_count = db.Column(db.Integer(), nullable=False, default=0)
    group_flag = db.Column(db.Integer(), nullable=False, default=0)

    _idx1 = db.Index("group_info_idx1", "group_id", unique=True)

    @classmethod
    async def get_group_info(cls, group_id: int) -> "GroupInfo":
        """
        说明：
            获取群信息
        参数：
            :param group_id: 群号
        """
        query = cls.query.where(cls.group_id == group_id)
        return await query.gino.first()

    @classmethod
    async def add_group_info(
        cls,
        group_id: int,
        group_name: str,
        max_member_count: int,
        member_count: int,
        group_flag: Optional[int] = None,
    ) -> bool:
        """
        说明：
            添加群信息
        参数：
            :param group_id: 群号
            :param group_name: 群名称
            :param max_member_count: 群员最大数量
            :param member_count: 群员数量
            :param group_flag: 群认证，0为未认证，1为认证
        """
        try:
            group = (
                await cls.query.where(cls.group_id == group_id)
                .with_for_update()
                .gino.first()
            )
            if group:
                await group.update(
                    group_name=group_name,
                    max_member_count=max_member_count,
                    member_count=member_count,
                ).apply()
                if group_flag is not None:
                    await group.update(group_flag=group_flag).apply()
            else:
                await cls.create(
                    group_id=group_id,
                    group_name=group_name,
                    max_member_count=max_member_count,
                    member_count=member_count,
                    group_flag=group_flag,
                )
            return True
        except Exception as e:
            logger.info(f"GroupInfo 调用 add_group_info 发生错误 {type(e)}：{e}")
            return False

    @classmethod
    async def delete_group_info(cls, group_id: int):
        """
        说明：
            删除群信息
        参数：
            :param group_id: 群号
        """
        await cls.delete.where(cls.group_id == group_id).gino.status()

    @classmethod
    async def get_all_group(cls) -> List["GroupInfo"]:
        """
        说明：
            获取所有群对象
        """
        query = await cls.query.gino.all()
        return query

    @classmethod
    async def set_group_flag(cls, group_id: int, group_flag: int) -> bool:
        """
        设置群认证
        :param group_id: 群号
        :param group_flag: 群认证，0为未认证，1为认证
        """
        group = (
            await cls.query.where(cls.group_id == group_id)
            .with_for_update()
            .gino.first()
        )
        if group:
            if group.group_flag != group_flag:
                await group.update(
                    group_flag=group_flag,
                ).apply()
            return True
        return False
