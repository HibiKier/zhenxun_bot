from datetime import datetime
from typing import List, Optional, Tuple

from tortoise import fields

from services.db_context import Model
from services.log import logger


class BilibiliSub(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    sub_id = fields.IntField()
    """订阅id"""
    sub_type = fields.CharField(255)
    """订阅类型"""
    sub_users = fields.TextField()
    """订阅用户"""
    live_short_id = fields.IntField(null=True)
    """直播短id"""
    live_status = fields.IntField(null=True)
    """直播状态 0: 停播  1: 直播"""
    uid = fields.BigIntField(null=True)
    """主播/UP UID"""
    uname = fields.CharField(255, null=True)
    """主播/UP 名称"""
    latest_video_created = fields.BigIntField(null=True)
    """最后视频上传时间"""
    dynamic_upload_time = fields.BigIntField(null=True, default=0)
    """动态发布时间"""
    season_name = fields.CharField(255, null=True)
    """番剧名称"""
    season_id = fields.IntField(null=True)
    """番剧id"""
    season_current_episode = fields.CharField(255, null=True)
    """番剧最新集数"""
    season_update_time = fields.DateField(null=True)
    """番剧更新日期"""

    class Meta:
        table = "bilibili_sub"
        table_description = "B站订阅数据表"
        unique_together = ("sub_id", "sub_type")

    @classmethod
    async def sub_handle(
        cls,
        sub_id: int,
        sub_type: Optional[str] = None,
        sub_user: str = "",
        *,
        live_short_id: Optional[int] = None,
        live_status: Optional[int] = None,
        dynamic_upload_time: int = 0,
        uid: Optional[int] = None,
        uname: Optional[str] = None,
        latest_video_created: Optional[int] = None,
        season_name: Optional[str] = None,
        season_id: Optional[int] = None,
        season_current_episode: Optional[str] = None,
        season_update_time: Optional[datetime] = None,
    ) -> bool:
        """
        说明:
            添加订阅
        参数:
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
        # try:
        data = {
            "sub_type": sub_type,
            "sub_user": sub_user,
            "live_short_id": live_short_id,
            "live_status": live_status,
            "dynamic_upload_time": dynamic_upload_time,
            "uid": uid,
            "uname": uname,
            "latest_video_created": latest_video_created,
            "season_name": season_name,
            "season_id": season_id,
            "season_current_episode": season_current_episode,
            "season_update_time": season_update_time,
        }
        if sub_user:
            sub_user = sub_user if sub_user[-1] == "," else f"{sub_user},"
        sub = None
        if sub_type:
            sub = await cls.get_or_none(sub_id=sub_id, sub_type=sub_type)
        else:
            sub = await cls.get_or_none(sub_id=sub_id)
        if sub:
            sub_users = sub.sub_users + sub_user
            data["sub_type"] = sub_type or sub.sub_type
            data["sub_users"] = sub_users
            data["live_short_id"] = live_short_id or sub.live_short_id
            data["live_status"] = (
                live_status if live_status is not None else sub.live_status
            )
            data["dynamic_upload_time"] = dynamic_upload_time or sub.dynamic_upload_time
            data["uid"] = uid or sub.uid
            data["uname"] = uname or sub.uname
            data["latest_video_created"] = (
                latest_video_created or sub.latest_video_created
            )
            data["season_name"] = season_name or sub.season_name
            data["season_id"] = season_id or sub.season_id
            data["season_current_episode"] = (
                season_current_episode or sub.season_current_episode
            )
            data["season_update_time"] = season_update_time or sub.season_update_time
        else:
            await cls.create(sub_id=sub_id, sub_type=sub_type, sub_users=sub_user)
        await cls.update_or_create(sub_id=sub_id, defaults=data)
        return True
        # except Exception as e:
        #     logger.info(f"bilibili_sub 添加订阅错误 {type(e)}: {e}")
        # return False

    @classmethod
    async def delete_bilibili_sub(
        cls, sub_id: int, sub_user: str, sub_type: Optional[str] = None
    ) -> bool:
        """
        说明:
            删除订阅
        参数:
            :param sub_id: 订阅名称
            :param sub_user: 删除此条目的用户
        """
        try:
            if sub_type:
                sub = await cls.filter(
                    sub_id=sub_id, sub_type=sub_type, sub_users__contains=sub_user
                ).first()
            else:
                sub = await cls.filter(
                    sub_id=sub_id, sub_users__contains=sub_user
                ).first()
            if not sub:
                return False
            sub.sub_users = sub.sub_users.replace(f"{sub_user},", "")
            if sub.sub_users.strip():
                await sub.save(update_fields=["sub_users"])
            else:
                await sub.delete()
            return True
        except Exception as e:
            logger.info(f"bilibili_sub 删除订阅错误 {type(e)}: {e}")
        return False

    @classmethod
    async def get_all_sub_data(
        cls,
    ) -> Tuple[List["BilibiliSub"], List["BilibiliSub"], List["BilibiliSub"]]:
        """
        说明:
            分类获取所有数据
        """
        live_data = []
        up_data = []
        season_data = []
        query = await cls.all()
        for x in query:
            if x.sub_type == "live":
                live_data.append(x)
            if x.sub_type == "up":
                up_data.append(x)
            if x.sub_type == "season":
                season_data.append(x)
        return live_data, up_data, season_data

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE bilibili_sub ALTER COLUMN season_update_time TYPE timestamp with time zone USING season_update_time::timestamp with time zone;",
        ]
