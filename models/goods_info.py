from services.db_context import db
from typing import Optional, List, Tuple
from services.log import logger


class GoodsInfo(db.Model):
    __tablename__ = "goods_info"

    id = db.Column(db.Integer(), primary_key=True)
    goods_name = db.Column(db.TEXT(), nullable=False)  # 名称
    goods_price = db.Column(db.Integer(), nullable=False)  # 价格
    goods_description = db.Column(db.TEXT(), nullable=False)  # 商品描述
    goods_discount = db.Column(db.Numeric(scale=3, asdecimal=False), default=1)  # 打折
    goods_limit_time = db.Column(db.BigInteger(), default=0)  # 限时
    daily_limit = db.Column(db.Integer(), nullable=False, default=0)  # 每日购买限制
    daily_purchase_limit = db.Column(
        db.JSON(), nullable=False, default={}
    )  # 每日购买限制数据存储

    _idx1 = db.Index("goods_group_users_idx1", "goods_name", unique=True)

    @classmethod
    async def add_goods(
            cls,
            goods_name: str,
            goods_price: int,
            goods_description: str,
            goods_discount: float = 1,
            goods_limit_time: int = 0,
            daily_limit: int = 0,
    ) -> bool:
        """
        说明:
            添加商品
        参数:
            :param goods_name: 商品名称
            :param goods_price: 商品价格
            :param goods_description: 商品简介
            :param goods_discount: 商品折扣
            :param goods_limit_time: 商品限时
            :param daily_limit: 每日购买限制
        """
        try:
            if not await cls.get_goods_info(goods_name):
                await cls.create(
                    goods_name=goods_name,
                    goods_price=goods_price,
                    goods_description=goods_description,
                    goods_discount=goods_discount,
                    goods_limit_time=goods_limit_time,
                    daily_limit=daily_limit,
                )
                return True
        except Exception as e:
            logger.error(f"GoodsInfo add_goods 发生错误 {type(e)}：{e}")
        return False

    @classmethod
    async def delete_goods(cls, goods_name: str) -> bool:
        """
        说明:
            删除商品
        参数:
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
            daily_limit: Optional[int] = None
    ) -> bool:
        """
        说明:
            更新商品信息
        参数:
            :param goods_name: 商品名称
            :param goods_price: 商品价格
            :param goods_description: 商品简介
            :param goods_discount: 商品折扣
            :param goods_limit_time: 商品限时时间
            :param daily_limit: 每日次数限制
        """
        try:
            query = (
                await cls.query.where(cls.goods_name == goods_name)
                    .with_for_update()
                    .gino.first()
            )
            if not query:
                return False
            await query.update(
                goods_price=goods_price or query.goods_price,
                goods_description=goods_description or query.goods_description,
                goods_discount=goods_discount or query.goods_discount,
                goods_limit_time=goods_limit_time if goods_limit_time is not None else query.goods_limit_time,
                daily_limit=daily_limit if daily_limit is not None else query.daily_limit,
            ).apply()
            return True
        except Exception as e:
            logger.error(f"GoodsInfo update_goods 发生错误 {type(e)}：{e}")
        return False

    @classmethod
    async def get_goods_info(cls, goods_name: str) -> "GoodsInfo":
        """
        说明:
            获取商品对象
        参数:
            :param goods_name: 商品名称
        """
        return await cls.query.where(cls.goods_name == goods_name).gino.first()

    @classmethod
    async def get_all_goods(cls) -> List["GoodsInfo"]:
        """
        说明:
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

    @classmethod
    async def add_user_daily_purchase(
            cls, goods: "GoodsInfo", user_id: int, group_id: int, num: int = 1
    ):
        """
        说明:
            添加用户明日购买限制
        参数:
            :param goods: 商品
            :param user_id: 用户id
            :param group_id: 群号
            :param num: 数量
        """
        user_id = str(user_id)
        group_id = str(group_id)
        if goods and goods.daily_limit and goods.daily_limit > 0:
            if not goods.daily_purchase_limit.get(group_id):
                goods.daily_purchase_limit[group_id] = {}
            if not goods.daily_purchase_limit[group_id].get(user_id):
                goods.daily_purchase_limit[group_id][user_id] = 0
            goods.daily_purchase_limit[group_id][user_id] += num
            await goods.update(daily_purchase_limit=goods.daily_purchase_limit).apply()

    @classmethod
    async def check_user_daily_purchase(
            cls, goods: "GoodsInfo", user_id: int, group_id: int, num: int = 1
    ) -> Tuple[bool, int]:
        """
        说明:
            检测用户每日购买上限
        参数:
            :param goods: 商品
            :param user_id: 用户id
            :param group_id: 群号
            :param num: 数量
        """
        user_id = str(user_id)
        group_id = str(group_id)
        if goods and goods.daily_limit > 0:
            if (
                not goods.daily_limit
                or not goods.daily_purchase_limit.get(group_id)
                or not goods.daily_purchase_limit[group_id].get(user_id)
            ):
                return goods.daily_limit - num < 0, goods.daily_limit
            if goods.daily_purchase_limit[group_id][user_id] + num > goods.daily_limit:
                return (
                    True,
                    goods.daily_limit - goods.daily_purchase_limit[group_id][user_id],
                )
        return False, 0

    @classmethod
    async def reset_daily_purchase(cls):
        """
        重置每次次数限制
        """
        await cls.update.values(daily_purchase_limit={}).gino.status()
