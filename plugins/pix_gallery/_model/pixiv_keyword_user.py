from typing import List, Set, Tuple

from tortoise import fields

from services.db_context import Model


class PixivKeywordUser(Model):
    __tablename__ = "pixiv_keyword_users"
    __table_args__ = {"extend_existing": True}

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_qq = fields.BigIntField()
    """用户id"""
    group_id = fields.BigIntField()
    """群聊id"""
    keyword = fields.CharField(255, unique=True)
    """关键词"""
    is_pass = fields.BooleanField()
    """是否通过"""

    class Meta:
        table = "pixiv_keyword_users"
        table_description = "pixiv关键词数据表"

    @classmethod
    async def get_current_keyword(cls) -> Tuple[List[str], List[str]]:
        """
        说明:
            获取当前通过与未通过的关键词
        """
        pass_keyword = []
        not_pass_keyword = []
        for data in await cls.all().values_list("keyword", "is_pass"):
            if data[1]:
                pass_keyword.append(data[0])
            else:
                not_pass_keyword.append(data[0])
        return pass_keyword, not_pass_keyword

    @classmethod
    async def get_black_pid(cls) -> List[str]:
        """
        说明:
            获取黑名单PID
        """
        black_pid = []
        keyword_list = await cls.filter(user_qq=114514).values_list(
            "keyword", flat=True
        )
        for image in keyword_list:
            black_pid.append(image[6:])
        return black_pid
