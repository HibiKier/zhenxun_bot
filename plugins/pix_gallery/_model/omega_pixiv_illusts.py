from typing import List, Optional, Tuple

from tortoise import fields
from tortoise.contrib.postgres.functions import Random

from services.db_context import Model


class OmegaPixivIllusts(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    pid = fields.BigIntField()
    """pid"""
    uid = fields.BigIntField()
    """uid"""
    title = fields.CharField(255)
    """标题"""
    uname = fields.CharField(255)
    """画师名称"""
    classified = fields.IntField()
    """标记标签, 0=未标记, 1=已人工标记或从可信已标记来源获取"""
    nsfw_tag = fields.IntField()
    """nsfw标签,-1=未标记, 0=safe, 1=setu. 2=r18"""
    width = fields.IntField()
    """宽度"""
    height = fields.IntField()
    """高度"""
    tags = fields.TextField()
    """tags"""
    url = fields.CharField(255)
    """pixiv url链接"""

    class Meta:
        table = "omega_pixiv_illusts"
        table_description = "omega图库数据表"
        unique_together = ("pid", "url")

    @classmethod
    async def query_images(
        cls,
        keywords: Optional[List[str]] = None,
        uid: Optional[int] = None,
        pid: Optional[int] = None,
        nsfw_tag: Optional[int] = 0,
        num: int = 100,
    ) -> List["OmegaPixivIllusts"]:
        """
        说明:
            查找符合条件的图片
        参数:
            :param keywords: 关键词
            :param uid: 画师uid
            :param pid: 图片pid
            :param nsfw_tag: nsfw标签, 0=safe, 1=setu. 2=r18
            :param num: 获取图片数量
        """
        if not num:
            return []
        query = cls
        if nsfw_tag is not None:
            query = cls.filter(nsfw_tag=nsfw_tag)
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
    async def get_keyword_num(
        cls, tags: Optional[List[str]] = None
    ) -> Tuple[int, int, int]:
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
        count = await query.filter(nsfw_tag=0).count()
        setu_count = await query.filter(nsfw_tag=1).count()
        r18_count = await query.filter(nsfw_tag=2).count()
        return count, setu_count, r18_count
