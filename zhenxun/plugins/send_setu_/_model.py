from tortoise import fields
from tortoise.contrib.postgres.functions import Random
from tortoise.expressions import Q
from typing_extensions import Self

from zhenxun.services.db_context import Model


class Setu(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    local_id = fields.IntField()
    """本地存储下标"""
    title = fields.CharField(255)
    """标题"""
    author = fields.CharField(255)
    """作者"""
    pid = fields.BigIntField()
    """pid"""
    img_hash = fields.TextField()
    """图片hash"""
    img_url = fields.CharField(255)
    """pixiv url链接"""
    is_r18 = fields.BooleanField()
    """是否r18"""
    tags = fields.TextField()
    """tags"""

    class Meta:
        table = "setu"
        table_description = "色图数据表"
        unique_together = ("pid", "img_url")

    @classmethod
    async def query_image(
        cls,
        local_id: int | None = None,
        tags: list[str] | None = None,
        r18: bool = False,
        limit: int = 50,
    ) -> list[Self] | Self | None:
        """通过tag查找色图

        参数:
            local_id: 本地色图 id
            tags: tags
            r18: 是否 r18，0：非r18  1：r18  2：混合
            limit: 获取数量

        返回:
            list[Self] | Self | None: 色图数据
        """
        if local_id:
            return await cls.filter(is_r18=r18, local_id=local_id).first()
        query = cls.filter(is_r18=r18)
        if tags:
            for tag in tags:
                query = query.filter(
                    Q(tags__contains=tag)
                    | Q(title__contains=tag)
                    | Q(author__contains=tag)
                )
        query = query.annotate(rand=Random()).limit(limit)
        return await query.all()

    @classmethod
    async def delete_image(cls, pid: int, img_url: str) -> int:
        """删除图片并替换

        参数:
            pid: 图片pid

        返回:
            int: 删除返回的本地id
        """
        print(pid)
        return_id = -1
        if query := await cls.get_or_none(pid=pid, img_url=img_url):
            num = await cls.filter(is_r18=query.is_r18).count()
            last_image = await cls.get_or_none(is_r18=query.is_r18, local_id=num - 1)
            if last_image:
                return_id = last_image.local_id
                last_image.local_id = query.local_id
                await last_image.save(update_fields=["local_id"])
            await query.delete()
        return return_id
