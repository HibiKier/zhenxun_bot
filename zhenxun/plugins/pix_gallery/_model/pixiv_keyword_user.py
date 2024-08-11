from tortoise import fields

from zhenxun.services.db_context import Model


class PixivKeywordUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
    """群聊id"""
    keyword = fields.CharField(255, unique=True)
    """关键词"""
    is_pass = fields.BooleanField()
    """是否通过"""

    class Meta:
        table = "pixiv_keyword_users"
        table_description = "pixiv关键词数据表"

    @classmethod
    async def get_current_keyword(cls) -> tuple[list[str], list[str]]:
        """获取当前通过与未通过的关键词"""
        pass_keyword = []
        not_pass_keyword = []
        for data in await cls.all().values_list("keyword", "is_pass"):
            if data[1]:
                pass_keyword.append(data[0])
            else:
                not_pass_keyword.append(data[0])
        return pass_keyword, not_pass_keyword

    @classmethod
    async def get_black_pid(cls) -> list[str]:
        """获取黑名单PID"""
        black_pid = []
        keyword_list = await cls.filter(user_id="114514").values_list(
            "keyword", flat=True
        )
        for image in keyword_list:
            black_pid.append(image[6:])
        return black_pid

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE pixiv_keyword_users RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE pixiv_keyword_users ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE pixiv_keyword_users ALTER COLUMN group_id TYPE character varying(255);",
        ]
