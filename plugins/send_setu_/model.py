from services.db_context import db
from typing import List, Optional


class Setu(db.Model):
    __tablename__ = "setu"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer(), primary_key=True)
    local_id = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    pid = db.Column(db.BigInteger(), nullable=False)
    img_hash = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)
    is_r18 = db.Column(db.Boolean(), nullable=False)
    tags = db.Column(db.String())

    _idx1 = db.Index("setu_pid_img_url_idx1", "pid", "img_url", unique=True)

    @classmethod
    async def add_setu_data(
        cls,
        local_id: int,
        title: str,
        author: str,
        pid: int,
        img_hash: str,
        img_url: str,
        tags: str,
    ):
        """
        说明：
            添加一份色图数据
        参数：
            :param local_id: 本地存储id
            :param title: 标题
            :param author: 作者
            :param pid: 图片pid
            :param img_hash: 图片hash值
            :param img_url: 图片链接
            :param tags: 图片标签
        """
        if not await cls._check_exists(pid, img_url):
            await cls.create(
                local_id=local_id,
                title=title,
                author=author,
                pid=pid,
                img_hash=img_hash,
                img_url=img_url,
                is_r18=True if "R-18" in tags else False,
                tags=tags,
            )

    @classmethod
    async def query_image(
        cls,
        local_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
        r18: int = 0,
        limit: int = 50,
    ):
        """
        说明：
            通过tag查找色图
        参数：
            :param local_id: 本地色图 id
            :param tags: tags
            :param r18: 是否 r18，0：非r18  1：r18  2：混合
            :param limit: 获取数量
        """
        if local_id:
            flag = True if r18 == 1 else False
            return await cls.query.where(
                (cls.local_id == local_id) & (cls.is_r18 == flag)
            ).gino.first()
        if r18 == 0:
            query = cls.query.where(cls.is_r18 == False)
        elif r18 == 1:
            query = cls.query.where(cls.is_r18 == True)
        else:
            query = cls.query
        if tags:
            for tag in tags:
                query = query.where(cls.tags.contains(tag) | cls.title.contains(tag) | cls.author.contains(tag))
        query = query.order_by(db.func.random()).limit(limit)
        return await query.gino.all()

    @classmethod
    async def get_image_count(cls, r18: int = 0) -> int:
        """
        说明：
            查询图片数量
        """
        flag = False if r18 == 0 else True
        setattr(Setu, 'count', db.func.count(cls.local_id).label('count'))
        count = await cls.select('count').where(cls.is_r18 == flag).gino.first()
        return count[0]

    @classmethod
    async def get_image_in_hash(cls, img_hash: str) -> "Setu":
        """
        说明：
            通过图像hash获取图像信息
        参数：
            :param img_hash: = 图像hash值
        """
        query = await cls.query.where(cls.img_hash == img_hash).gino.first()
        return query

    @classmethod
    async def _check_exists(cls, pid: int, img_url: str) -> bool:
        """
        说明：
            检测图片是否存在
        参数：
            :param pid: 图片pid
            :param img_url: 图片链接
        """
        return bool(
            await cls.query.where(
                (cls.pid == pid) & (cls.img_url == img_url)
            ).gino.first()
        )

    @classmethod
    async def delete_image(cls, pid: int) -> int:
        """
        说明：
            删除图片并替换
        参数：
            :param pid: 图片pid
        """
        query = await cls.query.where(cls.pid == pid).gino.first()
        if query:
            is_r18 = query.is_r18
            num = await cls.get_image_count(is_r18)
            x = await cls.query.where((cls.is_r18 == is_r18) & (cls.local_id == num - 1)).gino.first()
            _tmp_local_id = x.local_id
            if x:
                x.update(local_id=query.local_id).apply()
            await cls.delete.where(cls.pid == pid).gino.status()
            return _tmp_local_id
        return -1


    @classmethod
    async def update_setu_data(
        cls,
        pid: int,
        *,
        local_id: Optional[int] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        img_hash: Optional[str] = None,
        img_url: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> bool:
        """
        说明：
            根据PID修改图片数据
        参数：
            :param local_id: 本地id
            :param pid: 图片pid
            :param title: 标题
            :param author: 作者
            :param img_hash: 图片hash值
            :param img_url: 图片链接
            :param tags: 图片标签
        """
        query = cls.query.where(cls.pid == pid).with_for_update()
        image_list = await query.gino.all()
        if image_list:
            for image in image_list:
                if local_id:
                    await image.update(local_id=local_id).apply()
                if title:
                    await image.update(title=title).apply()
                if author:
                    await image.update(author=author).apply()
                if img_hash:
                    await image.update(img_hash=img_hash).apply()
                if img_url:
                    await image.update(img_url=img_url).apply()
                if tags:
                    await image.update(tags=tags).apply()
            return True
        return False

    @classmethod
    async def get_all_setu(cls) -> List["Setu"]:
        """
        说明：
            获取所有图片对象
        """
        return await cls.query.gino.all()

