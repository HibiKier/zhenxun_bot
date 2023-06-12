import random
from asyncio.exceptions import TimeoutError
from datetime import datetime
from typing import Optional, Tuple

# from .utils import get_videos
from bilireq import dynamic
from bilireq.exceptions import ResponseCodeError
from bilireq.live import get_room_info_by_id
from bilireq.user import get_videos
from nonebot.adapters.onebot.v11 import MessageSegment

from configs.path_config import IMAGE_PATH, TEMP_PATH
from services.log import logger
from utils.browser import get_browser
from utils.http_utils import AsyncHttpx, AsyncPlaywright
from utils.manager import resources_manager
from utils.message_builder import image
from utils.utils import get_bot

from .model import BilibiliSub
from .utils import get_meta, get_user_card

SEARCH_URL = "https://api.bilibili.com/x/web-interface/search/all/v2"

DYNAMIC_PATH = IMAGE_PATH / "bilibili_sub" / "dynamic"
DYNAMIC_PATH.mkdir(exist_ok=True, parents=True)


resources_manager.add_temp_dir(DYNAMIC_PATH)


async def add_live_sub(live_id: str, sub_user: str) -> str:
    """
    添加直播订阅
    :param live_id: 直播房间号
    :param sub_user: 订阅用户 id # 7384933:private or 7384933:2342344(group)
    :return:
    """
    try:
        if await BilibiliSub.exists(
            sub_type="live", sub_id=live_id, sub_users__contains=sub_user + ","
        ):
            return "该订阅Id已存在..."
        try:
            """bilibili_api.live库的LiveRoom类中get_room_info改为bilireq.live库的get_room_info_by_id方法"""
            live_info = await get_room_info_by_id(live_id)
        except ResponseCodeError:
            return f"未找到房间号Id：{live_id} 的信息，请检查Id是否正确"
        uid = str(live_info["uid"])
        room_id = live_info["room_id"]
        short_id = live_info["short_id"]
        title = live_info["title"]
        live_status = live_info["live_status"]
        if await BilibiliSub.sub_handle(
            room_id,
            "live",
            sub_user,
            uid=uid,
            live_short_id=short_id,
            live_status=live_status,
        ):
            try:
                await _get_up_status(room_id)
            except Exception as e:
                logger.error(f"获取主播UP信息失败: {live_id} 错误", e=e)
            if data := await BilibiliSub.get_or_none(sub_id=room_id):
                uname = data.uname
                return (
                    "已成功订阅主播：\n"
                    f"\ttitle：{title}\n"
                    f"\tname： {uname}\n"
                    f"\tlive_id：{room_id}\n"
                    f"\tuid：{uid}"
                )
        return "添加订阅失败..."
    except Exception as e:
        logger.error(f"订阅主播live_id: {live_id} 错误", e=e)
    return "添加订阅失败..."


async def add_up_sub(uid: str, sub_user: str) -> str:
    """
    添加订阅 UP
    :param uid: UP uid
    :param sub_user: 订阅用户
    """
    uname = uid
    dynamic_upload_time = 0
    latest_video_created = 0
    try:
        if await BilibiliSub.exists(
            sub_type="up", sub_id=uid, sub_users__contains=sub_user + ","
        ):
            return "该订阅Id已存在..."
        try:
            """bilibili_api.user库中User类的get_user_info改为bilireq.user库的get_user_info方法"""
            user_info = await get_user_card(uid)
        except ResponseCodeError:
            return f"未找到UpId：{uid} 的信息，请检查Id是否正确"
        uname = user_info["name"]
        """bilibili_api.user库中User类的get_dynamics改为bilireq.dynamic库的get_user_dynamics方法"""
        dynamic_info = await dynamic.get_user_dynamics(int(uid))
        if dynamic_info.get("cards"):
            dynamic_upload_time = dynamic_info["cards"][0]["desc"]["timestamp"]
        """bilibili_api.user库中User类的get_videos改为bilireq.user库的get_videos方法"""
        video_info = await get_videos(int(uid))
        if video_info["list"].get("vlist"):
            latest_video_created = video_info["list"]["vlist"][0]["created"]
    except Exception as e:
        logger.error(f"订阅Up uid: {uid} 错误", e=e)
    if await BilibiliSub.sub_handle(
        uid,
        "up",
        sub_user,
        uid=uid,
        uname=uname,
        dynamic_upload_time=dynamic_upload_time,
        latest_video_created=latest_video_created,
    ):
        return "已成功订阅UP：\n" f"\tname: {uname}\n" f"\tuid：{uid}"
    else:
        return "添加订阅失败..."


async def add_season_sub(media_id: str, sub_user: str) -> str:
    """
    添加订阅 UP
    :param media_id: 番剧 media_id
    :param sub_user: 订阅用户
    """
    try:
        if await BilibiliSub.exists(
            sub_type="season", sub_id=media_id, sub_users__contains=sub_user + ","
        ):
            return "该订阅Id已存在..."
        try:
            """bilibili_api.bangumi库中get_meta改为bilireq.bangumi库的get_meta方法"""
            season_info = await get_meta(media_id)
        except ResponseCodeError:
            return f"未找到media_id：{media_id} 的信息，请检查Id是否正确"
        season_id = season_info["media"]["season_id"]
        season_current_episode = season_info["media"]["new_ep"]["index"]
        season_name = season_info["media"]["title"]
        if await BilibiliSub.sub_handle(
            media_id,
            "season",
            sub_user,
            season_name=season_name,
            season_id=season_id,
            season_current_episode=season_current_episode,
        ):
            return (
                "已成功订阅番剧：\n"
                f"\ttitle: {season_name}\n"
                f"\tcurrent_episode: {season_current_episode}"
            )
        else:
            return "添加订阅失败..."
    except Exception as e:
        logger.error(f"订阅番剧 media_id: {media_id} 错误", e=e)
    return "添加订阅失败..."


async def delete_sub(sub_id: str, sub_user: str) -> str:
    """
    删除订阅
    :param sub_id: 订阅 id
    :param sub_user: 订阅用户 id # 7384933:private or 7384933:2342344(group)
    """
    if await BilibiliSub.delete_bilibili_sub(sub_id, sub_user):
        return f"已成功取消订阅：{sub_id}"
    else:
        return f"取消订阅：{sub_id} 失败，请检查是否订阅过该Id...."


async def get_media_id(keyword: str) -> Optional[dict]:
    """
    获取番剧的 media_id
    :param keyword: 番剧名称
    """
    params = {"keyword": keyword}
    for _ in range(3):
        try:
            _season_data = {}
            response = await AsyncHttpx.get(SEARCH_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    for item in data["data"]["result"]:
                        if item["result_type"] == "media_bangumi":
                            idx = 0
                            for x in item["data"]:
                                _season_data[idx] = {
                                    "media_id": x["media_id"],
                                    "title": x["title"]
                                    .replace('<em class="keyword">', "")
                                    .replace("</em>", ""),
                                }
                                idx += 1
                            return _season_data
        except TimeoutError:
            pass
        return {}


async def get_sub_status(id_: str, sub_type: str) -> Optional[str]:
    """
    获取订阅状态
    :param id_: 订阅 id
    :param sub_type: 订阅类型
    """
    try:
        if sub_type == "live":
            return await _get_live_status(id_)
        elif sub_type == "up":
            return await _get_up_status(id_)
        elif sub_type == "season":
            return await _get_season_status(id_)
    except ResponseCodeError as e:
        logger.error(f"Id：{id_} 获取信息失败...", e=e)
        # return f"Id：{id_} 获取信息失败...请检查订阅Id是否存在或稍后再试..."
    except Exception as e:
        logger.error(f"获取订阅状态发生预料之外的错误 Id_：{id_}", e=e)
    #     return "发生了预料之外的错误..请稍后再试或联系管理员....."


async def _get_live_status(id_: str) -> Optional[str]:
    """
    获取直播订阅状态
    :param id_: 直播间 id
    """
    """bilibili_api.live库的LiveRoom类中get_room_info改为bilireq.live库的get_room_info_by_id方法"""
    live_info = await get_room_info_by_id(id_)
    title = live_info["title"]
    room_id = live_info["room_id"]
    live_status = live_info["live_status"]
    cover = live_info["user_cover"]
    if sub := await BilibiliSub.get_or_none(sub_id=id_):
        if sub.live_status != live_status:
            await BilibiliSub.sub_handle(id_, live_status=live_status)
        if sub.live_status in [0, 2] and live_status == 1:
            return (
                f""
                f"{image(cover)}\n"
                f"{sub.uname} 开播啦！\n"
                f"标题：{title}\n"
                f"直链：https://live.bilibili.com/{room_id}"
            )
    return None


async def _get_up_status(id_: str) -> Optional[str]:
    """
    获取用户投稿状态
    :param id_: 订阅 id
    :return:
    """
    rst = ""
    if _user := await BilibiliSub.get_or_none(sub_id=id_):
        """bilibili_api.user库中User类的get_user_info改为bilireq.user库的get_user_info方法"""
        user_info = await get_user_card(_user.uid)
        uname = user_info["name"]
        """bilibili_api.user库中User类的get_videos改为bilireq.user库的get_videos方法"""
        video_info = await get_videos(int(_user.uid))
        latest_video_created = 0
        video = None
        dividing_line = "\n-------------\n"
        if _user.uname != uname:
            await BilibiliSub.sub_handle(id_, uname=uname)
        dynamic_img, dynamic_upload_time, link = await get_user_dynamic(
            _user.uid, _user
        )
        if video_info["list"].get("vlist"):
            video = video_info["list"]["vlist"][0]
            latest_video_created = video["created"]
        if dynamic_img:
            await BilibiliSub.sub_handle(id_, dynamic_upload_time=dynamic_upload_time)
            rst += f"{uname} 发布了动态！\n" f"{dynamic_img}\n{link}"
        if (
            latest_video_created
            and _user.latest_video_created
            and video
            and _user.latest_video_created < latest_video_created
        ):
            rst = rst + dividing_line if rst else rst
            await BilibiliSub.sub_handle(id_, latest_video_created=latest_video_created)
            rst += (
                f'{image(video["pic"])}\n'
                f"{uname} 投稿了新视频啦\n"
                f'标题：{video["title"]}\n'
                f'Bvid：{video["bvid"]}\n'
                f'直链：https://www.bilibili.com/video/{video["bvid"]}'
            )
        rst = None if rst == dividing_line else rst
    return rst


async def _get_season_status(id_: str) -> Optional[str]:
    """
    获取 番剧 更新状态
    :param id_: 番剧 id
    """
    """bilibili_api.bangumi库中get_meta改为bilireq.bangumi库的get_meta方法"""
    season_info = await get_meta(id_)
    title = season_info["media"]["title"]
    if data := await BilibiliSub.get_or_none(sub_id=id_):
        _idx = data.season_current_episode
        new_ep = season_info["media"]["new_ep"]["index"]
        if new_ep != _idx:
            await BilibiliSub.sub_handle(
                id_, season_current_episode=new_ep, season_update_time=datetime.now()
            )
            return (
                f'{image(season_info["media"]["cover"])}\n'
                f"[{title}]更新啦\n"
                f"最新集数：{new_ep}"
            )
    return None


async def get_user_dynamic(
    uid: str, local_user: BilibiliSub
) -> Tuple[Optional[MessageSegment], int, str]:
    """
    获取用户动态
    :param uid: 用户uid
    :param local_user: 数据库存储的用户数据
    :return: 最新动态截图与时间
    """
    """bilibili_api.user库中User类的get_dynamics改为bilireq.dynamic库的get_user_dynamics方法"""
    dynamic_info = await dynamic.get_user_dynamics(int(uid))
    if dynamic_info.get("cards"):
        dynamic_upload_time = dynamic_info["cards"][0]["desc"]["timestamp"]
        dynamic_id = dynamic_info["cards"][0]["desc"]["dynamic_id"]
        if local_user.dynamic_upload_time < dynamic_upload_time:
            image = await AsyncPlaywright.screenshot(
                f"https://t.bilibili.com/{dynamic_id}",
                DYNAMIC_PATH / f"sub_{local_user.sub_id}.png",
                ".bili-dyn-item__main",
                wait_until="networkidle",
            )
            return (
                image,
                dynamic_upload_time,
                f"https://t.bilibili.com/{dynamic_id}",
            )
    return None, 0, ""


class SubManager:
    def __init__(self):
        self.live_data = []
        self.up_data = []
        self.season_data = []
        self.current_index = -1

    async def reload_sub_data(self):
        """
        重载数据
        """
        if not self.live_data or not self.up_data or not self.season_data:
            (
                _live_data,
                _up_data,
                _season_data,
            ) = await BilibiliSub.get_all_sub_data()
            if not self.live_data:
                self.live_data = _live_data
            if not self.up_data:
                self.up_data = _up_data
            if not self.season_data:
                self.season_data = _season_data

    async def random_sub_data(self) -> Optional[BilibiliSub]:
        """
        随机获取一条数据
        :return:
        """
        sub = None
        if not self.live_data and not self.up_data and not self.season_data:
            return sub
        self.current_index += 1
        if self.current_index == 0:
            if self.live_data:
                sub = random.choice(self.live_data)
                self.live_data.remove(sub)
        elif self.current_index == 1:
            if self.up_data:
                sub = random.choice(self.up_data)
                self.up_data.remove(sub)
        elif self.current_index == 2:
            if self.season_data:
                sub = random.choice(self.season_data)
                self.season_data.remove(sub)
        else:
            self.current_index = -1
        if sub:
            return sub
        await self.reload_sub_data()
        return await self.random_sub_data()
