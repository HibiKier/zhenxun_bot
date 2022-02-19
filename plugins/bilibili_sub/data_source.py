from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from utils.manager import resources_manager
from asyncio.exceptions import TimeoutError
from .model import BilibiliSub
from bilibili_api.live import LiveRoom
from bilibili_api import bangumi
from utils.message_builder import image
from bilibili_api.user import User
from bilibili_api import user
from typing import Optional
from configs.path_config import IMAGE_PATH
from datetime import datetime
from utils.browser import get_browser
from services.db_context import db
from services.log import logger
from utils.http_utils import AsyncHttpx
import random


bilibili_search_url = "https://api.bilibili.com/x/web-interface/search/all/v2"

dynamic_path = IMAGE_PATH / "bilibili_sub" / "dynamic"
dynamic_path.mkdir(exist_ok=True, parents=True)


resources_manager.add_temp_dir(dynamic_path)


async def add_live_sub(live_id: int, sub_user: str) -> str:
    """
    添加直播订阅
    :param live_id: 直播房间号
    :param sub_user: 订阅用户 id # 7384933:private or 7384933:2342344(group)
    :return:
    """
    try:
        async with db.transaction():
            try:
                live = LiveRoom(live_id)
                live_info = (await live.get_room_info())["room_info"]
            except ResponseCodeException:
                return f"未找到房间号Id：{live_id} 的信息，请检查Id是否正确"
            uid = live_info["uid"]
            room_id = live_info["room_id"]
            short_id = live_info["short_id"]
            title = live_info["title"]
            live_status = live_info["live_status"]
            if await BilibiliSub.add_bilibili_sub(
                room_id,
                "live",
                sub_user,
                uid=uid,
                live_short_id=short_id,
                live_status=live_status,
            ):
                await _get_up_status(live_id)
                uname = (await BilibiliSub.get_sub(live_id)).uname
                return (
                    "已成功订阅主播：\n"
                    f"\ttitle：{title}\n"
                    f"\tname： {uname}\n"
                    f"\tlive_id：{live_id}\n"
                    f"\tuid：{uid}"
                )
            else:
                return "添加订阅失败..."
    except Exception as e:
        logger.error(f"订阅主播live_id：{live_id} 发生了错误 {type(e)}：{e}")
    return "添加订阅失败..."


async def add_up_sub(uid: int, sub_user: str) -> str:
    """
    添加订阅 UP
    :param uid: UP uid
    :param sub_user: 订阅用户
    """
    try:
        async with db.transaction():
            try:
                u = user.User(uid)
                user_info = await u.get_user_info()
            except ResponseCodeException:
                return f"未找到UpId：{uid} 的信息，请检查Id是否正确"
            uname = user_info["name"]
            dynamic_info = await u.get_dynamics(0)
            dynamic_upload_time = 0
            if dynamic_info.get("cards"):
                dynamic_upload_time = dynamic_info["cards"][0]["desc"]["timestamp"]
            video_info = await u.get_videos()
            latest_video_created = 0
            if video_info["list"].get("vlist"):
                latest_video_created = video_info["list"]["vlist"][0]["created"]
            if await BilibiliSub.add_bilibili_sub(
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
    except Exception as e:
        logger.error(f"订阅Up uid：{uid} 发生了错误 {type(e)}：{e}")
    return "添加订阅失败..."


async def add_season_sub(media_id: int, sub_user: str) -> str:
    """
    添加订阅 UP
    :param media_id: 番剧 media_id
    :param sub_user: 订阅用户
    """
    try:
        async with db.transaction():
            try:
                season_info = await bangumi.get_meta(media_id)
            except ResponseCodeException:
                return f"未找到media_id：{media_id} 的信息，请检查Id是否正确"
            season_id = season_info["media"]["season_id"]
            season_current_episode = season_info["media"]["new_ep"]["index"]
            season_name = season_info["media"]["title"]
            if await BilibiliSub.add_bilibili_sub(
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
        logger.error(f"订阅番剧 media_id：{media_id} 发生了错误 {type(e)}：{e}")
    return "添加订阅失败..."


async def delete_sub(sub_id: str, sub_user: str) -> str:
    """
    删除订阅
    :param sub_id: 订阅 id
    :param sub_user: 订阅用户 id # 7384933:private or 7384933:2342344(group)
    """
    if await BilibiliSub.delete_bilibili_sub(int(sub_id), sub_user):
        return f"已成功取消订阅：{sub_id}"
    else:
        return f"取消订阅：{sub_id} 失败，请检查是否订阅过该Id...."


async def get_media_id(keyword: str) -> dict:
    """
    获取番剧的 media_id
    :param keyword: 番剧名称
    """
    params = {"keyword": keyword}
    for _ in range(3):
        try:
            _season_data = {}
            response = await AsyncHttpx.get(
                bilibili_search_url, params=params, timeout=5
            )
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


async def get_sub_status(id_: int, sub_type: str) -> Optional[str]:
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
    except ResponseCodeException:
        return f"Id：{id_} 获取信息失败...请检查订阅Id是否存在或稍后再试..."
    # except Exception as e:
    #     logger.error(f"获取订阅状态发生预料之外的错误 id_：{id_} {type(e)}：{e}")
    #     return "发生了预料之外的错误..请稍后再试或联系管理员....."


async def _get_live_status(id_: int) -> Optional[str]:
    """
    获取直播订阅状态
    :param id_: 直播间 id
    """
    live = LiveRoom(id_)
    live_info = (await live.get_room_info())["room_info"]
    title = live_info["title"]
    room_id = live_info["room_id"]
    live_status = live_info["live_status"]
    cover = live_info["cover"]
    sub = await BilibiliSub.get_sub(id_)
    if sub.live_status != live_status:
        await BilibiliSub.update_sub_info(id_, live_status=live_status)
    if sub.live_status == 0 and live_status == 1:
        return (
            f"{image(cover)}\n"
            f"{sub.uname} 开播啦！\n"
            f"标题：{title}\n"
            f"直链：https://live.bilibili.com/{room_id}"
        )
    return None


async def _get_up_status(id_: int) -> Optional[str]:
    """
    获取用户投稿状态
    :param id_: 用户 id
    :return:
    """
    _user = await BilibiliSub.get_sub(id_)
    u = user.User(_user.uid)
    user_info = await u.get_user_info()
    uname = user_info["name"]
    video_info = await u.get_videos()
    latest_video_created = 0
    video = None
    if _user.uname != uname:
        await BilibiliSub.update_sub_info(id_, uname=uname)
    dynamic_img, dynamic_upload_time = await get_user_dynamic(u, _user)
    if video_info["list"].get("vlist"):
        video = video_info["list"]["vlist"][0]
        latest_video_created = video["created"]
    rst = ""
    if dynamic_img:
        await BilibiliSub.update_sub_info(id_, dynamic_upload_time=dynamic_upload_time)
        rst += f"{uname} 发布了动态！\n" f"{dynamic_img}\n"
    if (
        latest_video_created
        and _user.latest_video_created
        and video
        and _user.latest_video_created < latest_video_created
    ):
        rst = rst + "-------------\n" if rst else rst
        await BilibiliSub.update_sub_info(
            id_, latest_video_created=latest_video_created
        )
        rst += (
            f'{image(video["pic"])}\n'
            f"{uname} 投稿了新视频啦\n"
            f'标题：{video["title"]}\n'
            f'Bvid：{video["bvid"]}\n'
            f'直链：https://www.bilibili.com/video/{video["bvid"]}'
        )
    rst = None if rst == "-------------\n" else rst
    return rst


async def _get_season_status(id_) -> Optional[str]:
    """
    获取 番剧 更新状态
    :param id_: 番剧 id
    """
    season_info = await bangumi.get_meta(id_)
    title = season_info["media"]["title"]
    _idx = (await BilibiliSub.get_sub(id_)).season_current_episode
    new_ep = season_info["media"]["new_ep"]["index"]
    if new_ep != _idx:
        await BilibiliSub.update_sub_info(
            id_, season_current_episode=new_ep, season_update_time=datetime.now()
        )
        return (
            f'{image(season_info["media"]["cover"])}\n'
            f"[{title}]更新啦\n"
            f"最新集数：{new_ep}"
        )
    return None


async def get_user_dynamic(
    u: User, local_user: BilibiliSub
) -> "Optional[MessageSegment], int":
    """
    获取用户动态
    :param u: 用户类
    :param local_user: 数据库存储的用户数据
    :return: 最新动态截图与时间
    """
    dynamic_info = await u.get_dynamics(0)
    browser = await get_browser()
    if dynamic_info.get("cards") and browser:
        dynamic_upload_time = dynamic_info["cards"][0]["desc"]["timestamp"]
        if local_user.dynamic_upload_time < dynamic_upload_time:
            page = await browser.new_page()
            await page.goto(
                f"https://space.bilibili.com/{local_user.uid}/dynamic",
                wait_until="networkidle",
                timeout=10000,
            )
            await page.set_viewport_size({"width": 2560, "height": 1080})
            # 删除置顶
            await page.evaluate(
                """
                xs = document.getElementsByClassName('first-card-with-title');
                for (x of xs) {
                  x.remove();
                }
            """
            )
            card = await page.query_selector(".card")
            # 截图并保存
            await card.screenshot(
                path=dynamic_path / f"{local_user.sub_id}_{dynamic_upload_time}.jpg",
                timeout=100000,
            )
            await page.close()
            return (
                image(
                    f"{local_user.sub_id}_{dynamic_upload_time}.jpg",
                    "bilibili_sub/dynamic",
                ),
                dynamic_upload_time,
            )
    return None, None


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
