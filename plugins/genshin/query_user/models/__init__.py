from services.db_context import db
from typing import Optional, Union


class Genshin(db.Model):
    __tablename__ = "genshin"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    uid = db.Column(db.BigInteger())
    mys_id = db.Column(db.BigInteger())
    cookie = db.Column(db.String(), default="")
    today_query_uid = db.Column(db.String(), default="")  # 该cookie今日查询的uid
    auto_sign = db.Column(db.Boolean(), default=False)  # 自动签到

    _idx1 = db.Index("genshin_uid_idx1", "user_qq", "uid", unique=True)

    @classmethod
    async def add_uid(cls, user_qq: int, uid: int):
        """
        说明：
            添加一个uid
        参数：
            :param user_qq： 用户qq
            :param uid: 原神uid
        """
        query = cls.query.where((cls.user_qq == user_qq) & (cls.uid == uid))
        user = await query.gino.first()
        if not user:
            await cls.create(
                user_qq=user_qq,
                uid=uid,
            )
            return True
        return False

    @classmethod
    async def set_mys_id(cls, uid: int, mys_id: int) -> bool:
        """
        说明：
            设置米游社id
        参数：
            :param uid: 原神uid
            :param mys_id: 米游社id
        """
        query = cls.query.where(cls.uid == uid).with_for_update()
        user = await query.gino.first()
        if user:
            await user.update(mys_id=mys_id).apply()
            return True
        return False

    @classmethod
    async def set_cookie(cls, uid: int, cookie: str) -> bool:
        """
        说明：
            设置cookie
        参数：
            :param uid: 原神uid
            :param cookie: 米游社id
        """
        query = cls.query.where(cls.uid == uid).with_for_update()
        user = await query.gino.first()
        if user:
            await user.update(cookie=cookie).apply()
            return True
        return False

    @classmethod
    async def set_auto_sign(cls, uid: int, flag: bool) -> bool:
        """
        说明：
            设置米游社自动签到
        参数：
            :param uid: 原神uid
            :param flag: 开关状态
        """
        query = cls.query.where(cls.uid == uid).with_for_update()
        user = await query.gino.first()
        if user:
            await user.update(auto_sign=flag).apply()
            return True
        return False

    @classmethod
    async def get_query_cookie(cls, uid: int) -> Optional[str]:
        """
        说明：
            获取查询角色信息cookie
        参数：
            :param uid: 原神uid
        """
        # 查找用户今日是否已经查找过，防止重复
        query = cls.query.where(cls.today_query_uid.contains(str(uid)))
        x = await query.gino.first()
        if x:
            return x.cookie
        for u in [x for x in await cls.query.order_by(db.func.random()).gino.all() if x.cookie]:
            if not u.today_query_uid or len(u.today_query_uid[:-1].split()) < 30:
                await cls._add_query_uid(uid, u.uid)
                return u.cookie
        return None

    @classmethod
    async def get_user_cookie(cls, uid: int, flag: bool = False) -> Optional[str]:
        """
        说明：
            获取用户cookie
        参数：
            :param uid：原神uid
            :param flag：必须使用自己的cookie
        """
        cookie = await cls._get_user_data(None, uid, "cookie")
        if not cookie and not flag:
            cookie = await cls.get_query_cookie(uid)
        return cookie

    @classmethod
    async def get_user_uid(cls, user_qq: int) -> Optional[int]:
        """
        说明：
            获取用户uid
        参数：
            :param user_qq：用户qq
        """
        return await cls._get_user_data(user_qq, None, "uid")

    @classmethod
    async def get_user_mys_id(cls, uid: int) -> Optional[int]:
        """
        说嘛：
            获取用户米游社id
        参数：
            :param uid：原神id
        """
        return await cls._get_user_data(None, uid, "mys_id")

    @classmethod
    async def delete_user_cookie(cls, uid: int):
        """
        说明：
            删除用户cookie
        参数：
            :param uid: 原神uid
        """
        query = cls.query.where(cls.uid == uid).with_for_update()
        user = await query.gino.first()
        if user:
            await user.update(cookie="").apply()

    @classmethod
    async def delete_user(cls, user_qq: int):
        """
        说明：
            删除用户数据
        参数：
            :param user_qq： 用户qq
        """
        query = cls.query.where(cls.user_qq == user_qq).with_for_update()
        user = await query.gino.first()
        if not user:
            return False
        await user.delete()
        return True

    @classmethod
    async def _add_query_uid(cls, uid: int, cookie_uid: int):
        """
        说明：
            添加每日查询重复uid的cookie
        参数：
            :param uid: 原神uid
            :param cookie_uid: cookie的uid
        """
        query = cls.query.where(cls.uid == cookie_uid).with_for_update()
        user = await query.gino.first()
        await user.update(today_query_uid=cls.today_query_uid + f"{uid} ").apply()

    @classmethod
    async def _get_user_data(
        cls, user_qq: Optional[int], uid: Optional[int], type_: str
    ) -> Optional[Union[int, str]]:
        """
        说明：
            获取用户数据
        参数：
            :param user_qq： 用户qq
            :param uid: uid
            :param type_: 数据类型
        """
        if type_ == "uid":
            user = await cls.query.where(cls.user_qq == user_qq).gino.first()
            return user.uid if user else None
        user = await cls.query.where(cls.uid == uid).gino.first()
        if not user:
            return None
        if type_ == "mys_id":
            return user.mys_id
        elif type_ == "cookie":
            return user.cookie

    @classmethod
    async def reset_today_query_uid(cls):
        for u in await cls.query.with_for_update().gino.all():
            if u.today_query_uid:
                await u.update(
                    today_query_uid=""
                ).apply()
