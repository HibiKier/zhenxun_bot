from typing import Optional, List
from datetime import datetime
from services.db_context import db


class OmegaPixivIllusts(db.Model):
    __tablename__ = "omega_pixiv_illusts"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    pid = db.Column(db.BigInteger(), nullable=False)
    uid = db.Column(db.BigInteger(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    uname = db.Column(db.String(), nullable=False)
    nsfw_tag = db.Column(db.Integer(), nullable=False)
    width = db.Column(db.Integer(), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    tags = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True))

    _idx1 = db.Index("omega_pixiv_illusts_idx1", "pid", "url", unique=True)

    @classmethod
    async def add_image_data(
            cls,
            pid: int,
            title: str,
            width: int,
            height: int,
            url: str,
            uid: int,
            uname: str,
            nsfw_tag: int,
            tags: str,
            created_at: datetime,
            updated_at: datetime,
    ):
        """
        说明：
            添加图片信息
        参数：
            :param pid: pid
            :param title: 标题
            :param width: 宽度
            :param height: 长度
            :param url: url链接
            :param uid: 作者uid
            :param uname: 作者名称
            :param nsfw_tag: nsfw标签, 0=safe, 1=setu. 2=r18
            :param tags: 相关tag
            :param created_at: 创建日期
            :param updated_at: 更新日期
        """
        if not await cls.check_exists(pid):
            await cls.create(
                pid=pid,
                title=title,
                width=width,
                height=height,
                url=url,
                uid=uid,
                uname=uname,
                nsfw_tag=nsfw_tag,
                tags=tags,
            )
            return True
        return False

    @classmethod
    async def query_images(
            cls,
            keywords: Optional[List[str]] = None,
            uid: Optional[int] = None,
            pid: Optional[int] = None,
            nsfw_tag: Optional[int] = 0,
            num: int = 100
    ) -> List[Optional["OmegaPixivIllusts"]]:
        """
        说明：
            查找符合条件的图片
        参数：
            :param keywords: 关键词
            :param uid: 画师uid
            :param pid: 图片pid
            :param nsfw_tag: nsfw标签, 0=safe, 1=setu. 2=r18
            :param num: 获取图片数量
        """
        if nsfw_tag is not None:
            query = cls.query.where(cls.nsfw_tag == nsfw_tag)
        else:
            query = cls.query
        if keywords:
            for keyword in keywords:
                query = query.where(cls.tags.contains(keyword))
        elif uid:
            query = query.where(cls.uid == uid)
        elif pid:
            query = query.where(cls.uid == pid)
        query = query.order_by(db.func.random()).limit(num)
        return await query.gino.all()

    @classmethod
    async def check_exists(cls, pid: int) -> bool:
        """
        说明：
            检测pid是否已存在
        参数：
            :param pid: 图片PID
        """
        query = await cls.query.where(cls.pid == pid).gino.all()
        return bool(query)

    @classmethod
    async def get_keyword_num(cls, tags: List[str] = None) -> "int, int, int":
        """
        说明：
            获取相关关键词(keyword, tag)在图库中的数量
        参数：
            :param tags: 关键词/Tag
        """
        setattr(OmegaPixivIllusts, 'count', db.func.count(cls.pid).label('count'))
        query = cls.select('count')
        if tags:
            for tag in tags:
                query = query.where(cls.tags.contains(tag))
        count = await query.where(cls.nsfw_tag == 0).gino.first()
        setu_count = await query.where(cls.nsfw_tag == 1).gino.first()
        r18_count = await query.where(cls.nsfw_tag == 2).gino.first()
        return count[0], setu_count[0], r18_count[0]

    @classmethod
    async def get_all_pid(cls) -> List[int]:
        """
        说明：
            获取所有图片PID
        """
        data = await cls.select('pid').gino.all()
        return [x[0] for x in data]

    @classmethod
    async def test(cls, nsfw_tag: int = 1):
        if nsfw_tag is not None:
            query = cls.query.where(cls.nsfw_tag == nsfw_tag)
        else:
            query = cls.query
        query = query.where((cls.width - cls.height) < 50)
        for x in await query.gino.all():
            print(x.pid)



