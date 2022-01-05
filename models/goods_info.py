from services.db_context import db
from typing import Optional, List
from services.log import logger


class GoodsInfo(db.Model):
    __tablename__ = "goods_info"

    id = db.Column(db.Integer(), primary_key=True)
    goods_name = db.Column(db.TEXT(), nullable=False)  # 名称
    goods_price = db.Column(db.Integer(), nullable=False)  # 价格
    goods_description = db.Column(db.TEXT(), nullable=False)  # 商品描述
    goods_discount = db.Column(db.Numeric(scale=3, asdecimal=False), default=1)  # 打折
    goods_limit_time = db.Column(db.BigInteger(), default=0)  # 限时

    _idx1 = db.Index("goods_group_users_idx1", "goods_name", unique=True)

    @classmethod
    async def add_goods(
        cls,
        goods_name: str,
        goods_price: int,
        goods_description: str,
        goods_discount: float = 1,
        goods_limit_time: int = 0,
    ) -> bool:
        """
        说明：
            添加商品
        参数：
            :param goods_name: 商品名称
            :param goods_price: 商品价格
            :param goods_description: 商品简介
            :param goods_discount: 商品折扣
            :param goods_limit_time: 商品限时
        """
        try:
            if not await cls.get_goods_info(goods_name):
                await cls.create(
                    goods_name=goods_name,
                    goods_price=goods_price,
                    goods_description=goods_description,
                    goods_discount=goods_discount,
                    goods_limit_time=goods_limit_time,
                )
                return True
        except Exception as e:
            logger.error(f"GoodsInfo add_goods 发生错误 {type(e)}：{e}")
        return False

    @classmethod
    async def delete_goods(cls, goods_name: str) -> bool:
        """
        说明：
            删除商品
        参数：
            :param goods_name: 商品名称
        """
        query = (
            await cls.query.where(cls.goods_name == goods_name)
            .with_for_update()
            .gino.first()
        )
        if not query:
            return False
        await query.delete()
        return True

    @classmethod
    async def update_goods(
        cls,
        goods_name: str,
        goods_price: Optional[int] = None,
        goods_description: Optional[str] = None,
        goods_discount: Optional[float] = None,
        goods_limit_time: Optional[int] = None,
    ) -> bool:
        """
        说明：
            更新商品信息
        参数：
            :param goods_name: 商品名称
            :param goods_price: 商品价格
            :param goods_description: 商品简介
            :param goods_discount: 商品折扣
            :param goods_limit_time: 商品限时时间
        """
        try:
            query = (
                await cls.query.where(cls.goods_name == goods_name)
                .with_for_update()
                .gino.first()
            )
            if not query:
                return False
            if goods_price:
                await query.update(goods_price=goods_price).apply()
            if goods_description:
                await query.update(goods_description=goods_description).apply()
            if goods_discount:
                await query.update(goods_discount=goods_discount).apply()
            if goods_limit_time:
                await query.update(goods_limit_time=goods_limit_time).apply()
            return True
        except Exception as e:
            logger.error(f"GoodsInfo update_goods 发生错误 {type(e)}：{e}")
            return False

    @classmethod
    async def get_goods_info(cls, goods_name: str) -> "GoodsInfo":
        """
        说明：
            获取商品对象
        参数：
            :param goods_name: 商品名称
        """
        query = await cls.query.where(cls.goods_name == goods_name).gino.first()
        return query

    @classmethod
    async def get_all_goods(cls) -> List["GoodsInfo"]:
        """
        说明：
            获得全部有序商品对象
        """
        query = await cls.query.gino.all()
        id_lst = [x.id for x in query]
        goods_lst = []
        for _ in range(len(query)):
            min_id = min(id_lst)
            goods_lst.append([x for x in query if x.id == min_id][0])
            id_lst.remove(min_id)
        return goods_lst
