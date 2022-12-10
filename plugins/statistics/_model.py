from datetime import datetime
from typing import Optional

from services.db_context import db


class Statistics(db.Model):
    __tablename__ = "statistics"
    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger())
    plugin_name = db.Column(db.String(), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    async def add_statistic(cls, user_qq: int, group_id: Optional[int], plugin_name: str):
        """
        说明:
            添加记录
        参数:
            :param user_qq: qq
            :param group_id: 群号
            :param plugin_name: 插件model
        """
        await cls.create(
            user_qq=user_qq,
            group_id=group_id,
            plugin_name=plugin_name,
            create_time=datetime.now(),
        )
