from typing import Optional, List
from services.db_context import db


class Pixiv(db.Model):
    __tablename__ = "pixiv"

    id = db.Column(db.Integer(), primary_key=True)
    pid = db.Column(db.BigInteger(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    width = db.Column(db.Integer(), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    view = db.Column(db.Integer(), nullable=False)
    bookmarks = db.Column(db.Integer(), nullable=False)
    img_url = db.Column(db.String(), nullable=False)
    img_p = db.Column(db.String(), nullable=False)
    uid = db.Column(db.BigInteger(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    is_r18 = db.Column(db.Boolean(), nullable=False)
    tags = db.Column(db.String(), nullable=False)

    _idx1 = db.Index("pixiv_idx1", "pid", "img_url", unique=True)

    @classmethod
    async def add_image_data(
            cls,
            pid: int,
            title: str,
            width: int,
            height: int,
            view: int,
            bookmarks: int,
            img_url: str,
            img_p: str,
            uid: int,
            author: str,
            tags: str,
    ):
        """
        说明：
            添加图片信息
        参数：
            :param pid: pid
            :param title: 标题
            :param width: 宽度
            :param height: 长度
            :param view: 被查看次数
            :param bookmarks: 收藏数
            :param img_url: url链接
            :param img_p: 张数
            :param uid: 作者uid
            :param author: 作者名称
            :param tags: 相关tag
        """
        if not await cls.check_exists(pid, img_p):
            await cls.create(
                pid=pid,
                title=title,
                width=width,
                height=height,
                view=view,
                bookmarks=bookmarks,
                img_url=img_url,
                img_p=img_p,
                uid=uid,
                author=author,
                is_r18=True if 'R-18' in tags else False,
                tags=tags,
            )
            return True
        return False

    @classmethod
    async def remove_image_data(cls, pid: int, img_p: str) -> bool:
        """
        说明：
            删除图片数据
        参数：
            :param pid: 图片pid
            :param img_p: 图片pid的张数，如：p0，p1
        """
        try:
            if img_p:
                await cls.delete.where(
                    (cls.pid == pid) & (cls.img_p == img_p)
                ).gino.status()
            else:
                await cls.delete.where(cls.pid == pid).gino.status()
            return True
        except Exception:
            return False

    @classmethod
    async def get_all_pid(cls) -> List[int]:
        """
        说明：
            获取所有PID
        """
        pid = []
        query = await cls.query.gino.all()
        for image in query:
            if image.pid not in pid:
                pid.append(image.pid)
        return pid

    # 0：非r18  1：r18  2：混合
    @classmethod
    async def query_images(
        cls,
        keyword: Optional[List[str]] = None,
        uid: Optional[int] = None,
        pid: Optional[int] = None,
        r18: int = 0,
    ) -> List[Optional["Pixiv"]]:
        """
        说明：
            查找符合条件的图片
        参数：
            :param keyword: 关键词
            :param uid: 画师uid
            :param pid: 图片pid
            :param r18: 是否r18，0：非r18  1：r18  2：混合
        """
        if r18 == 0:
            query = await cls.query.where(cls.is_r18 == False).gino.all()
        elif r18 == 1:
            query = await cls.query.where(cls.is_r18 == True).gino.all()
        else:
            query = await cls.query.gino.all()
        if keyword:
            query = [x for x in query if set(x.tags.split(',')) > set(keyword)]
        elif uid:
            query = [x for x in query if x.uid == uid]
        elif pid:
            query = [x for x in query if x.pid == pid]
        return query

    @classmethod
    async def check_exists(cls, pid: int, img_p: str) -> bool:
        """
        说明：
            检测pid是否已存在
        参数：
            :param pid: 图片PID
            :param img_p: 张数
        """
        query = await cls.query.where(
            (cls.pid == pid) & (cls.img_p == img_p)
        ).gino.all()
        return bool(query)

    @classmethod
    async def get_keyword_num(cls, keyword: List[str]) -> "int, int":
        """
        说明：
            获取相关关键词(keyword, tag)在图库中的数量
        参数：
            :param keyword: 关键词/Tag
        """
        query = await cls.query.gino.all()
        query = [x for x in query if set(x.tags.split(',')) > set(keyword)]
        r18_count = len([x for x in query if x.is_r18])
        return len(query) - r18_count, r18_count


