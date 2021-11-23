from services.db_context import db
from typing import Set, List


class PixivKeywordUser(db.Model):
    __tablename__ = "pixiv_keyword_users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.BigInteger(), nullable=False)
    keyword = db.Column(db.String(), nullable=False)
    is_pass = db.Column(db.Boolean(), default=False)

    _idx1 = db.Index("pixiv_keyword_users_idx1", "keyword", unique=True)

    @classmethod
    async def add_keyword(
        cls, user_qq: int, group_id: int, keyword: str, superusers: Set[str]
    ) -> bool:
        """
        说明：
            添加搜图的关键词
        参数：
            :param user_qq: qq号
            :param group_id: 群号
            :param keyword: 关键词
            :param superusers: 是否为超级用户
        """
        is_pass = True if str(user_qq) in superusers else False
        if not await cls._check_keyword_exists(keyword):
            await cls.create(
                user_qq=user_qq, group_id=group_id, keyword=keyword, is_pass=is_pass
            )
            return True
        return False

    @classmethod
    async def delete_keyword(cls, keyword: str) -> bool:
        """
        说明：
            删除关键词
        参数：
            :param keyword: 关键词
        """
        if await cls._check_keyword_exists(keyword):
            query = cls.query.where(cls.keyword == keyword).with_for_update()
            query = await query.gino.first()
            await query.delete()
            return True
        return False

    @classmethod
    async def set_keyword_pass(cls, keyword: str, is_pass: bool) -> "int, int":
        """
        说明：
            通过或禁用关键词
        参数：
            :param keyword: 关键词
            :param is_pass: 通过状态
        """
        if await cls._check_keyword_exists(keyword):
            query = cls.query.where(cls.keyword == keyword).with_for_update()
            query = await query.gino.first()
            await query.update(
                is_pass=is_pass,
            ).apply()
            return query.user_qq, query.group_id
        return 0, 0

    @classmethod
    async def get_all_user_dict(cls) -> dict:
        """
        说明：
            获取关键词数据库各个用户贡献的关键词字典
        """
        tmp = {}
        query = await cls.query.gino.all()
        for user in query:
            if not tmp.get(user.user_qq):
                tmp[user.user_qq] = {"keyword": []}
            tmp[user.user_qq]["keyword"].append(user.keyword)
        return tmp

    @classmethod
    async def get_current_keyword(cls) -> "List[str], List[str]":
        """
        说明：
            获取当前通过与未通过的关键词
        """
        pass_keyword = []
        not_pass_keyword = []
        query = await cls.query.gino.all()
        for user in query:
            if user.is_pass:
                pass_keyword.append(user.keyword)
            else:
                not_pass_keyword.append(user.keyword)
        return pass_keyword, not_pass_keyword

    @classmethod
    async def get_black_pid(cls) -> List[str]:
        """
        说明：
            获取黑名单PID
        """
        black_pid = []
        query = await cls.query.where(cls.user_qq == 114514).gino.all()
        for image in query:
            black_pid.append(image.keyword[6:])
        return black_pid

    @classmethod
    async def _check_keyword_exists(cls, keyword: str) -> bool:
        """
        说明：
            检测关键词是否已存在
        参数：
            :param keyword: 关键词
        """
        current_keyword = []
        query = await cls.query.gino.all()
        for user in query:
            current_keyword.append(user.keyword)
        if keyword in current_keyword:
            return True
        return False
