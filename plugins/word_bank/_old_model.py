from services.db_context import db
from typing import List


class WordBank(db.Model):
    __tablename__ = "word_bank"

    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.Integer())
    search_type = db.Column(db.Integer(), nullable=False, default=0)
    problem = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    format = db.Column(db.String())
    create_time = db.Column(db.DateTime(), nullable=False)
    update_time = db.Column(db.DateTime(), nullable=False)

    @classmethod
    async def get_all(cls) -> List['WordBank']:
        return await cls.query.gino.all()

