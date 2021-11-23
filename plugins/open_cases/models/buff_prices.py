
from datetime import datetime

from services.db_context import db

# 1.狂牙武器箱


class BuffPrice(db.Model):
    __tablename__ = 'buff_prices'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    case_id = db.Column(db.Integer(), nullable=False)
    skin_name = db.Column(db.Unicode(), nullable=False)
    skin_price = db.Column(db.Float(), nullable=False)
    update_date = db.Column(db.DateTime(), nullable=False)

    _idx1 = db.Index('buff_price_idx1', 'skin_name', unique=True)

    @classmethod
    async def ensure(cls, skin_name: str, for_update: bool = False) -> 'BuffPrice':
        query = cls.query.where(
            (cls.skin_name == skin_name)
        )
        if for_update:
            query = query.with_for_update()
        user = await query.gino.first()
        return user or await cls.create(
            case_id=1,
            skin_name=skin_name,
            skin_price=0,
            update_date=datetime.min,
        )

