from typing import List, Optional, Tuple

from tortoise import fields
from tortoise.contrib.postgres.functions import Random

from services.db_context import Model


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
        keywords: Optional[List[str]] = None,
        uid: Optional[int] = None,
        pid: Optional[int] = None,
        r18: Optional[int] = 0,
        num: int = 100,
    ) -> List[Optional["Pixiv"]]:
        """
        说明:
            查找符合条件的图片
        参数:
            :param keywords: 关键词
            :param uid: 画师uid
            :param pid: 图片pid
            :param r18: 是否r18，0：非r18  1：r18  2：混合
            :param num: 查找图片的数量
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
    async def get_keyword_num(cls, tags: Optional[List[str]] = None) -> Tuple[int, int]:
        """
        说明:
            获取相关关键词(keyword, tag)在图库中的数量
        参数:
            :param tags: 关键词/Tag
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
