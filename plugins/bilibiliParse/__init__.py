import time
import re
import ujson as json

from .InformationContainer import InformationContainer
from .parse_bili_url import parse_bili_url

from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.adapters.onebot.v11 import ActionFailed

from configs.config import Config
from utils.manager import group_manager
from services.log import logger
from utils.message_builder import image
from utils.utils import get_message_json, get_message_text

__zx_plugin_name__ = "B站内容解析"
__plugin_usage__ = """
usage：
    被动监听插件，解析B站视频、直播、专栏，支持小程序卡片及文本链接，5分钟内不解析相同内容
""".strip()
__plugin_des__ = "B站转发解析"
__plugin_type__ = ("其他",)
__plugin_version__ = 0.1
__plugin_author__ = "leekooyo"
__plugin_task__ = {"bilibili_parse": "b站转发解析"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_BILIBILI_PARSE",
    True,
    help_="被动 B站转发解析 进群默认开关状态",
    default_value=True,
    type=bool
)

async def plugin_on_checker(event: GroupMessageEvent) -> bool:
    """
    插件检查函数，检查是否开启 B站 转发解析功能

    Args:
        event (GroupMessageEvent): 群消息事件

    Returns:
        bool: 是否开启 B站 转发解析功能
    """
    return group_manager.get_plugin_status("parse_bilibili_json", event.group_id)

# 创建一个消息处理器
bilibiliParse = on_message(
    priority=5, permission=GROUP, block=False, rule=plugin_on_checker
)

# 临时变量，记录插件记录时间
_tmp = {}


@bilibiliParse.handle()
async def msgParse(event: GroupMessageEvent):
    """
    消息检查函数，检查消息是否和B站相关

    Args:
        event (GroupMessageEvent): 群消息事件

    """
    information_container = InformationContainer()
    # 判断文本消息内容是否相关
    match = None
    # 判断文本消息和小程序的内容是否指向一个b站链接
    get_url = None
    # 判断文本消息是否包含视频相关内容
    vd_flag = False
    # 设定时间阈值，阈值之下不会解析重复内容
    repet_second = 300
    # 尝试解析小程序消息
    if message_json := get_message_json(event.json()):
        try:
            data = json.loads(message_json[0].get("data", "{}"))
        except (IndexError, KeyError):
            data = None
        if data:
            # 获取相关数据
            meta_data = data.get('meta', {})
            news_value = meta_data.get("news", {})
            detail_1_value = meta_data.get("detail_1", {})
            qqdocurl_value = detail_1_value.get("qqdocurl", {})
            jumpUrl_value = news_value.get('jumpUrl', {})
            get_url = (qqdocurl_value if qqdocurl_value else jumpUrl_value).split("?")[0]

    # 解析文本消息
    elif msg := get_message_text(event.json()):
        # 消息中含有视频号
        if "bv" in msg.lower() or "av" in msg.lower():
            match = re.search(r'((?=(?:bv|av))([A-Za-z0-9]+))', msg, re.IGNORECASE)
            vd_flag = True
        
        # 消息中含有b23的链接，包括视频、专栏、动态、直播
        elif "https://b23.tv" in msg:
            match = re.search(r'https://b23\.tv/[^?\s]+', msg, re.IGNORECASE)

        # 检查消息中是否含有直播、专栏、动态链接
        elif any(keyword in msg for keyword in ["https://live.bilibili.com/", "https://www.bilibili.com/read/",
                                                "https://www.bilibili.com/opus/", "https://t.bilibili.com/"]):
            pattern = r'https://(live|www\.bilibili\.com/read|www\.bilibili\.com/opus|t\.bilibili\.com)/[^?\s]+'
            match = re.search(pattern, msg)

    # 匹配成功，则获取链接
    if match:
        if vd_flag:
            number = match.group(1)
            get_url = f"https://www.bilibili.com/video/{number}"
        else:
            get_url = match.group()
    

    if get_url:
        # 将链接统一发送给处理函数
        vd_info, live_info, vd_url, live_url, image_info, image_url = await parse_bili_url(get_url, information_container)
        if vd_info:
            # 判断一定时间内是否解析重复内容，或者是第一次解析
            if ((vd_url in _tmp.keys() and time.time()-_tmp[vd_url] > repet_second) 
                or vd_url not in _tmp.keys()
            ):
                pic = vd_info.get("pic", "") # 封面
                aid = vd_info.get("aid", "") # av号
                title = vd_info.get("title", "") # 标题
                author = vd_info.get("owner", {}).get("name", "") # UP主
                reply = vd_info.get("stat", {}).get("reply", "") # 回复
                favorite = vd_info.get("stat", {}).get("favorite", "") # 收藏
                coin = vd_info.get("stat", {}).get("coin", "") # 投币
                like = vd_info.get("stat", {}).get("like", "") # 点赞
                danmuku = vd_info.get("stat", {}).get("danmaku", "") # 弹幕
                ctime = vd_info["ctime"]
                date = time.strftime("%Y-%m-%d", time.localtime(ctime))
                try:
                    logger.info(
                        f"USER {event.user_id} GROUP {event.group_id} 解析bilibili转发 {vd_url}"
                    )
                    _tmp[vd_url] = time.time()
                    await bilibiliParse.finish(
                        f"[[_task|bilibili_parse]]"
                        + image(pic) +
                        f"av{aid}\n标题：{title}\n"
                        f"UP：{author}\n"
                        f"上传日期：{date}\n"
                        f"回复：{reply}，收藏：{favorite}，投币：{coin}\n"
                        f"点赞：{like}，弹幕：{danmuku}\n"
                        f"{vd_url}"
                    )
                except ActionFailed:
                    logger.warning(f"{event.group_id} 发送bilibili解析失败")

        elif live_info:
            if ((live_url in _tmp.keys() and time.time()-_tmp[live_url] > repet_second) 
                or live_url not in _tmp.keys()
            ):                
                uid = live_info.get("uid", "") # 主播uid
                title = live_info.get("title", "") # 直播间标题
                description = live_info.get("description", "") # 简介，可能会出现标签
                user_cover = live_info.get("user_cover", "") # 封面
                keyframe = live_info.get("keyframe", "") # 关键帧画面
                live_time = live_info.get("live_time", "") # 开播时间
                area_name = live_info.get("area_name", "") # 分区
                parent_area_name = live_info.get("parent_area_name", "") # 父分区
                try:
                    logger.info(
                        f"USER {event.user_id} GROUP {event.group_id} 解析bilibili转发 {live_url}"
                    )
                    _tmp[live_url] = time.time()
                    await bilibiliParse.finish(
                        f"[[_task|bilibili_parse]]"
                        + image(user_cover) +
                        f"开播用户：https://space.bilibili.com/{uid}"
                        f"\n开播时间：{live_time}"
                        f"\n直播分区：{parent_area_name}——>{area_name}"
                        f"\n标题：{title}"
                        f"\n简介：{description}"
                        f"\n直播截图：\n" 
                        + image(keyframe) +
                        f"{live_url}"
                    )
                except ActionFailed:
                    logger.warning(f"{event.group_id} 发送bilibili解析失败")

        elif image_info:
            if ((image_url in _tmp.keys() and time.time()-_tmp[image_url] > repet_second) 
                or image_url not in _tmp.keys()
            ):                
                try:
                    logger.info(
                        f"USER {event.user_id} GROUP {event.group_id} 解析bilibili转发 {image_url}"
                    )
                    _tmp[image_url] = time.time()
                    await bilibiliParse.finish(f"[[_task|bilibili_parse]]" + image_info)
                except ActionFailed:
                    logger.warning(f"{event.group_id} 发送bilibili解析失败")
              
