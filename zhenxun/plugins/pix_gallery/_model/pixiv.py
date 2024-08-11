from tortoise import fields
from tortoise.contrib.postgres.functions import Random

from zhenxun.services.db_context import Model


class Pixiv(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    pid = fields.BigIntField()
    """pid"""
    uid = fields.BigIntField()
    """uid"""
    author = fields.CharField(255)
    """作者"""
    title = fields.CharField(255)
    """标题"""
    width = fields.IntField()
    """宽度"""
    height = fields.IntField()
    """高度"""
    view = fields.IntField()
    """pixiv查看数"""
    bookmarks = fields.IntField()
    """收藏数"""
    tags = fields.TextField()
    """tags"""
    img_url = fields.CharField(255)
    """pixiv url链接"""
    img_p = fields.CharField(255)
    """图片pN"""
    is_r18 = fields.BooleanField()

    class Meta:
        table = "pixiv"
        table_description = "pix图库数据表"
        unique_together = ("pid", "img_url", "img_p")

    # 0：非r18  1：r18  2：混合
    @classmethod
    async def query_images(
        cls,
        keywords: list[str] | None = None,
        uid: int | None = None,
        pid: int | None = None,
        r18: int | None = 0,
        num: int = 100,
    ) -> list["Pixiv"]:
        """查找符合条件的图片

        参数:
            keywords: 关键词
            uid: 画师uid
            pid: 图片pid
            r18: 是否r18，0：非r18  1：r18  2：混合
            num: 查找图片的数量
        """
        if not num:
            return []
        query = cls
        if r18 == 0:
            query = query.filter(is_r18=False)
        elif r18 == 1:
            query = query.filter(is_r18=True)
        if keywords:
            for keyword in keywords:
                query = query.filter(tags__contains=keyword)
        elif uid:
            query = query.filter(uid=uid)
        elif pid:
            query = query.filter(pid=pid)
        query = query.annotate(rand=Random()).limit(num)
        return await query.all()  # type: ignore

    @classmethod
    async def get_keyword_num(cls, tags: list[str] | None = None) -> tuple[int, int]:
        """获取相关关键词(keyword, tag)在图库中的数量

        参数:
            tags: 关键词/Tag
        """
        query = cls
        if tags:
            for tag in tags:
                query = query.filter(tags__contains=tag)
        else:
            query = query.all()
        count = await query.filter(is_r18=False).count()
        r18_count = await query.filter(is_r18=True).count()
        return count, r18_count
