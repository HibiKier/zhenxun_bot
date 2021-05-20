
from services.db_context import db


class GroupInfo(db.Model):
    __tablename__ = 'group_info'

    group_id = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    group_name = db.Column(db.Unicode(), nullable=False, default="")
    max_member_count = db.Column(db.Integer(), nullable=False, default=0)
    member_count = db.Column(db.Integer(), nullable=False, default=0)

    _idx1 = db.Index('group_info_idx1', 'group_id', unique=True)

    @classmethod
    async def get_group_info(cls, group_id: int) -> 'GroupInfo':
        query = cls.query.where(
            cls.group_id == group_id
        )
        return await query.gino.first()

    @classmethod
    async def add_group_info(cls, group_id: int, group_name: str, max_member_count: int, member_count: int) -> bool:
        try:
            group = await cls.query.where(
                cls.group_id == group_id
            ).with_for_update().gino.first()
            if group:
                await cls.update(
                    group_id=group_id,
                    group_name=group_name,
                    max_member_count=max_member_count,
                    member_count=member_count,
                ).apply()
            else:
                await cls.create(
                    group_id=group_id,
                    group_name=group_name,
                    max_member_count=max_member_count,
                    member_count=member_count,
                )
            return True
        except Exception:
            return False

    @classmethod
    async def delete_group_info(cls, group_id: int) -> bool:
        try:
            await cls.delete.where(
                cls.group_id == group_id
            ).gino.status()
            return True
        except Exception:
            return False


