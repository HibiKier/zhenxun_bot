
from services.db_context import db


class UserBag(db.Model):
    __tablename__ = 'bag_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    belonging_group = db.Column(db.BigInteger(), nullable=False)
    gold = db.Column(db.Integer(), default=100)
    props = db.Column(db.TEXT(), nullable=False, default="")
    spend_total_gold = db.Column(db.Integer(), default=0)
    get_total_gold = db.Column(db.Integer(), default=0)
    get_today_gold = db.Column(db.Integer(), default=0)
    spend_today_gold = db.Column(db.Integer(), default=0)

    _idx1 = db.Index('bag_group_users_idx1', 'user_qq', 'belonging_group', unique=True)

    @classmethod
    async def get_my_total_gold(cls, user_qq: int, belonging_group: int) -> str:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        user = await query.gino.first()
        if not user:
            user = await cls.create(
                    user_qq=user_qq,
                    belonging_group=belonging_group,
                )
        return f'当前金币：{user.gold}\n今日获取金币：{user.get_today_gold}\n今日花费金币：{user.spend_today_gold}' \
               f'\n今日收益：{user.get_today_gold - user.spend_today_gold}' \
               f'\n总赚取金币：{user.get_total_gold}\n总花费金币：{user.spend_total_gold}'

    @classmethod
    async def get_gold(cls, user_qq: int, belonging_group: int) -> int:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        user = await query.gino.first()
        if user:
            return user.gold
        else:
            await cls.create(
                    user_qq=user_qq,
                    belonging_group=belonging_group,
                )
            return 100

    @classmethod
    async def get_props(cls, user_qq: int, belonging_group: int) -> str:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        user = await query.gino.first()
        if user:
            return user.props
        else:
            await cls.create(
                    user_qq=user_qq,
                    belonging_group=belonging_group,
                )
            return ''

    @classmethod
    async def add_glod(cls, user_qq: int, belonging_group: int, num: int) -> bool:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        try:
            if user:
                await user.update(
                    gold=user.gold + num,
                    get_total_gold=user.get_total_gold + num,
                    get_today_gold=user.get_today_gold + num
                ).apply()
            else:
                await cls.create(
                    user_qq=user_qq,
                    belonging_group=belonging_group,
                    gold=100 + num,
                    get_total_gold=num,
                    get_today_gold=num,
                )
            return True
        except Exception:
            return False

    @classmethod
    async def spend_glod(cls, user_qq: int, belonging_group: int, num: int) -> bool:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        try:
            if user:
                await user.update(
                    gold=user.gold - num,
                    spend_total_gold=user.spend_total_gold + num,
                    spend_today_gold=user.spend_today_gold + num
                ).apply()
            else:
                await cls.create(
                    user_qq=user_qq,
                    belonging_group=belonging_group,
                    gold=100 - num,
                    spend_total_gold=num,
                    spend_today_gold=num
                )
            return True
        except Exception:
            return False

    @classmethod
    async def add_props(cls, user_qq: int, belonging_group: int, name: str) -> bool:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        try:
            if user:
                await user.update(
                    props=user.props + f'{name},'
                ).apply()
            else:
                await cls.create(
                    user_qq=user_qq,
                    belonging_group=belonging_group,
                    props=f'{name},'
                )
            return True
        except Exception:
            return False

    @classmethod
    async def del_props(cls, user_qq: int, belonging_group: int, name: str) -> bool:
        query = cls.query.where(
            (cls.user_qq == user_qq) & (cls.belonging_group == belonging_group)
        )
        query = query.with_for_update()
        user = await query.gino.first()
        try:
            if user:
                rst = ''
                props = user.props
                if props.find(name) != -1:
                    props = props.split(',')
                    try:
                        index = props.index(name)
                    except ValueError:
                        return False
                    props = props[:index] + props[index + 1:]
                    for p in props:
                        if p != '':
                            rst += p + ','
                    await user.update(
                        props=rst
                    ).apply()
                    return True
                else:
                    return False
            else:
                return False
        except Exception:
            return False

    @classmethod
    async def get_user_all(cls, group_id: int = None) -> list:
        user_list = []
        if not group_id:
            query = await cls.query.gino.all()
        else:
            query = await cls.query.where(
                (cls.belonging_group == group_id)
            ).gino.all()
        for user in query:
            user_list.append(user)
        return user_list








