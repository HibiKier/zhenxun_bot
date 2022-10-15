from datetime import datetime

from services.db_context import db


class UserShopGoldLog(db.Model):
    __tablename__ = "user_shop_gold_log"
    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    type = db.Column(db.Integer(), nullable=False)  # 0: 购买，1: 使用，2: 插件
    name = db.Column(db.String())
    spend_gold = db.Column(db.Integer(), nullable=False)
    num = db.Column(db.Integer(), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), nullable=False)

    @classmethod
    async def add_shop_log(
        cls,
        user_qq: int,
        group_id: int,
        type_: int,
        name: str,
        num: int,
        spend_gold: int = 0,
    ):
        """
        说明:
            添加商店购买或使用日志
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
            :param type_: 类型
            :param name: 商品名称
            :param num: 数量
            :param spend_gold: 花费金币
        """
        await cls.create(
            user_qq=user_qq,
            group_id=group_id,
            type=type_,
            name=name,
            num=num,
            spend_gold=spend_gold,
            create_time=datetime.now(),
        )

    @classmethod
    async def get_user_log(cls, user_qq: int, group_id: int) -> "UserShopGoldLog":
        """
        说明:
            获取用户日志
        参数:
            :param user_qq: qq号
            :param group_id: 所在群号
        """
        return await cls.query.where(
            (cls.user_qq == user_qq) & (cls.group_qq == group_id)
        ).first()
