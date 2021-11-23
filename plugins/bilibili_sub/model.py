from services.log import logger
from services.db_context import db
from datetime import datetime
from typing import Optional, List


class BilibiliSub(db.Model):
    __tablename__ = "bilibili_sub"

    id = db.Column(db.Integer(), primary_key=True)
    sub_id = db.Column(db.Integer(), nullable=False)
    sub_type = db.Column(db.String(), nullable=False)
    # 订阅用户
    sub_users = db.Column(db.String(), nullable=False)
    # 直播
    live_short_id = db.Column(db.Integer())
    live_status = db.Column(db.Integer)
    # 主播/UP
    uid = db.Column(db.BigInteger())
    uname = db.Column(db.String())
    latest_video_created = db.Column(db.BigInteger())  # 视频上传时间
    dynamic_upload_time = db.Column(db.BigInteger(), default=0)  # 动态发布时间
    # 番剧
    season_name = db.Column(db.String())
    season_id = db.Column(db.Integer())
    season_current_episode = db.Column(db.String())
    season_update_time = db.Column(db.DateTime())

    _idx1 = db.Index("bilibili_sub_idx1", "sub_id", "sub_type", unique=True)

    @classmethod
    async def add_bilibili_sub(
        cls,
        sub_id: int,
        sub_type: str,
        sub_user: str,
        *,
        live_short_id: Optional[int] = None,
        live_status: Optional[int] = None,
        dynamic_upload_time: Optional[int] = None,
        uid: Optional[int] = None,
        uname: Optional[str] = None,
        latest_video_created: Optional[int] = None,
        season_name: Optional[str] = None,
        season_id: Optional[int] = None,
        season_current_episode: Optional[str] = None,
        season_update_time: Optional[datetime] = None,
    ) -> bool:
        """
        说明：
            添加订阅
        参数：
            :param sub_id: 订阅名称，房间号，番剧号等
            :param sub_type: 订阅类型
            :param sub_user: 订阅此条目的用户
            :param live_short_id: 直接短 id
            :param live_status: 主播开播状态
            :param dynamic_upload_time: 主播/UP最新动态时间
            :param uid: 主播/UP uid
            :param uname: 用户名称
            :param latest_video_created: 最新视频上传时间
            :param season_name: 番剧名称
            :param season_id: 番剧 season_id
            :param season_current_episode: 番剧最新集数
            :param season_update_time: 番剧更新时间
        """
        try:
            async with db.transaction():
                query = (
                    await cls.query.where(cls.sub_id == sub_id)
                    .with_for_update()
                    .gino.first()
                )
                sub_user = sub_user if sub_user[-1] == "," else f"{sub_user},"
                if query:
                    if sub_user not in query.sub_users:
                        sub_users = query.sub_users + sub_user
                        await query.update(sub_users=sub_users).apply()
                else:
                    sub = await cls.create(
                        sub_id=sub_id, sub_type=sub_type, sub_users=sub_user
                    )
                    await sub.update(
                        live_short_id=live_short_id
                        if live_short_id
                        else sub.live_short_id,
                        live_status=live_status if live_status else sub.live_status,
                        dynamic_upload_time=dynamic_upload_time
                        if dynamic_upload_time
                        else sub.dynamic_upload_time,
                        uid=uid if uid else sub.uid,
                        uname=uname if uname else sub.uname,
                        latest_video_created=latest_video_created
                        if latest_video_created
                        else sub.latest_video_created,
                        season_update_time=season_update_time
                        if season_update_time
                        else sub.season_update_time,
                        season_current_episode=season_current_episode
                        if season_current_episode
                        else sub.season_current_episode,
                        season_id=season_id if season_id else sub.season_id,
                        season_name=season_name if season_name else sub.season_name,
                    ).apply()
                return True
        except Exception as e:
            logger.info(f"bilibili_sub 添加订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def delete_bilibili_sub(cls, sub_id: int, sub_user: str) -> bool:
        """
        说明：
            删除订阅
        参数：
            :param sub_id: 订阅名称
            :param sub_user: 删除此条目的用户
        """
        try:
            async with db.transaction():
                query = (
                    await cls.query.where(
                        (cls.sub_id == sub_id) & (cls.sub_users.contains(sub_user))
                    )
                    .with_for_update()
                    .gino.first()
                )
                if not query:
                    return False
                await query.update(
                    sub_users=query.sub_users.replace(f"{sub_user},", "")
                ).apply()
                if not query.sub_users.strip():
                    await query.delete()
                return True
        except Exception as e:
            logger.info(f"bilibili_sub 删除订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def get_sub(cls, sub_id: int) -> Optional["BilibiliSub"]:
        """
        说明：
            获取订阅对象
        参数：
            :param sub_id: 订阅 id
        """
        return await cls.query.where(cls.sub_id == sub_id).gino.first()

    @classmethod
    async def get_sub_data(cls, id_: str) -> List["BilibiliSub"]:
        """
        获取 id_ 订阅的所有内容
        :param id_: id
        """
        query = cls.query.where(cls.sub_users.contains(id_))
        return await query.gino.all()

    @classmethod
    async def update_sub_info(
        cls,
        sub_id: int,
        *,
        live_short_id: Optional[int] = None,
        live_status: Optional[int] = None,
        dynamic_upload_time: Optional[int] = None,
        uid: Optional[int] = None,
        uname: Optional[str] = None,
        latest_video_created: Optional[int] = None,
        season_name: Optional[str] = None,
        season_id: Optional[int] = None,
        season_current_episode: Optional[str] = None,
        season_update_time: Optional[datetime] = None,
    ) -> bool:
        """
        说明：
            更新订阅信息
        参数：
            :param sub_id: 订阅名称，房间号，番剧号等
            :param live_short_id: 直接短 id
            :param live_status: 主播开播状态
            :param dynamic_upload_time: 主播/UP最新动态时间
            :param uid: 主播/UP uid
            :param uname: 用户名称
            :param latest_video_created: 最新视频上传时间
            :param season_name: 番剧名称
            :param season_id: 番剧 season_id
            :param season_current_episode: 番剧最新集数
            :param season_update_time: 番剧更新时间
        """
        try:
            async with db.transaction():
                sub = (
                    await cls.query.where(cls.sub_id == sub_id)
                    .with_for_update()
                    .gino.first()
                )
                if sub:
                    await sub.update(
                        live_short_id=live_short_id
                        if live_short_id is not None
                        else sub.live_short_id,
                        live_status=live_status
                        if live_status is not None
                        else sub.live_status,
                        dynamic_upload_time=dynamic_upload_time
                        if dynamic_upload_time is not None
                        else sub.dynamic_upload_time,
                        uid=uid if uid is not None else sub.uid,
                        uname=uname if uname is not None else sub.uname,
                        latest_video_created=latest_video_created
                        if latest_video_created is not None
                        else sub.latest_video_created,
                        season_update_time=season_update_time
                        if season_update_time is not None
                        else sub.season_update_time,
                        season_current_episode=season_current_episode
                        if season_current_episode is not None
                        else sub.season_current_episode,
                        season_id=season_id if season_id is not None else sub.season_id,
                        season_name=season_name
                        if season_name is not None
                        else sub.season_name,
                    ).apply()
                    return True
        except Exception as e:
            logger.info(f"bilibili_sub 更新订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def get_all_sub_data(
        cls,
    ) -> "List[BilibiliSub], List[BilibiliSub], List[BilibiliSub]":
        """
        说明：
            分类获取所有数据
        """
        live_data = []
        up_data = []
        season_data = []
        query = await cls.query.gino.all()
        for x in query:
            if x.sub_type == "live":
                live_data.append(x)
            if x.sub_type == "up":
                up_data.append(x)
            if x.sub_type == "season":
                season_data.append(x)
        return live_data, up_data, season_data
