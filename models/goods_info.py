
from services.db_context import db


class GoodsInfo(db.Model):
    __tablename__ = 'goods_info'

    id = db.Column(db.Integer(), primary_key=True)
    goods_name = db.Column(db.TEXT(), nullable=False)                            # 名称
    goods_price = db.Column(db.Integer(), nullable=False)                        # 价格
    goods_description = db.Column(db.TEXT(), nullable=False)                     # 商品描述
    goods_discount = db.Column(db.Numeric(scale=3, asdecimal=False), default=1)  # 打折
    goods_limit_time = db.Column(db.BigInteger(), default=0)                     # 限时

    _idx1 = db.Index('goods_group_users_idx1', 'goods_name', unique=True)

    @classmethod
    async def add_goods(cls, goods_name: str, goods_price: int,
                        goods_description: str, goods_discount: float = 1, goods_limit_time: int = 0) -> bool:
        # try:
        await cls.create(
            goods_name=goods_name,
            goods_price=goods_price,
            goods_description=goods_description,
            goods_discount=goods_discount,
            goods_limit_time=goods_limit_time
        )
        return True
        # except Exception:
        #     return False

    @classmethod
    async def del_goods(cls, goods_name: str) -> bool:
        query = await cls.query.where(
            cls.goods_name == goods_name
        ).with_for_update().gino.first()
        if not query:
            return False
        await query.delete()
        return True

    @classmethod
    async def update_goods(cls, goods_name: str, goods_price: int = None,
                           goods_description: str = None, goods_discount: float = None,
                           goods_limit_time: int = None) -> bool:
        try:
            query = await cls.query.where(
                cls.goods_name == goods_name
            ).with_for_update().gino.first()
            if not query:
                return False
            if goods_price:
                await query.update(
                    goods_price=goods_price
                ).apply()
            if goods_description:
                await query.update(
                    goods_description=goods_description
                ).apply()
            if goods_discount:
                await query.update(
                    goods_discount=goods_discount
                ).apply()
            if goods_limit_time:
                await query.update(
                    goods_limit_time=goods_limit_time
                ).apply()
            return True
        except Exception:
            return False

    @classmethod
    async def get_goods_info(cls, goods_name: str) -> 'GoodsInfo':
        query = await cls.query.where(
            cls.goods_name == goods_name
        ).gino.first()
        return query

    @classmethod
    async def get_all_goods(cls) -> list:
        query = await cls.query.gino.all()
        id_lst = [x.id for x in query]
        goods_lst = []
        for _ in range(len(query)):
            min_id = min(id_lst)
            goods_lst.append([x for x in query if x.id == min_id][0])
            id_lst.remove(min_id)
        return goods_lst










