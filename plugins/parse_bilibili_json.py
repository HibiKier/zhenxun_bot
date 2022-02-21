from nonebot import on_message
from services.log import logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from utils.utils import get_message_json, get_local_proxy, is_number, get_message_text
from nonebot.adapters.onebot.v11.permission import GROUP
from bilibili_api import video
from utils.message_builder import image
from nonebot.adapters.onebot.v11.exception import ActionFailed
from utils.image_utils import BuildImage
from utils.browser import get_browser
from configs.path_config import IMAGE_PATH
from utils.http_utils import AsyncHttpx
from configs.config import Config
from utils.user_agent import get_user_agent
import aiohttp
import asyncio
import time
from bilibili_api import settings
import ujson as json


__zx_plugin_name__ = "B站转发解析"
__plugin_usage__ = """
usage：
    B站转发解析，解析b站分享信息，支持bv，bilibili链接，b站手机端转发卡片，cv，b23.tv，且5分钟内不解析相同url
""".strip()
__plugin_des__ = "B站转发解析"
__plugin_type__ = ("其他",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"bilibili_parse": "b站转发解析"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_BILIBILI_PARSE",
    True,
    help_="被动 B站转发解析 进群默认开关状态",
    default_value=True,
)


if get_local_proxy():
    settings.proxy = get_local_proxy()

parse_bilibili_json = on_message(priority=1, permission=GROUP, block=False)

_tmp = {}


@parse_bilibili_json.handle()
async def _(event: GroupMessageEvent):
    vd_info = None
    url = None
    if get_message_json(event.json()):
        try:
            data = json.loads(get_message_json(event.json())[0]["data"])
        except (IndexError, KeyError):
            data = None
        if data:
            # 转发视频
            if data.get("desc") == "哔哩哔哩":
                async with aiohttp.ClientSession(
                    headers=get_user_agent()
                ) as session:
                    async with session.get(
                            data["meta"]["detail_1"]["qqdocurl"],
                            proxy=get_local_proxy(),
                            timeout=7,
                    ) as response:
                        url = str(response.url).split("?")[0]
                        bvid = url.split("/")[-1]
                        vd_info = await video.Video(bvid=bvid).get_info()
                # response = await AsyncHttpx.get(
                #     data["meta"]["detail_1"]["qqdocurl"], timeout=7
                # )
                # url = str(response.url).split("?")[0]
                # bvid = url.split("/")[-1]
                # vd_info = await video.Video(bvid=bvid).get_info()
            # 转发专栏
            if (
                data.get("meta")
                and data["meta"].get("news")
                and data["meta"]["news"].get("desc") == "哔哩哔哩专栏"
            ):
                url = data["meta"]["news"]["jumpUrl"]
                page = None
                try:
                    browser = await get_browser()
                    if not browser:
                        return
                    page = await browser.new_page(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        " (KHTML, like Gecko) Chrome/93.0.4530.0 Safari/537.36"
                    )
                    await page.goto(url, wait_until="networkidle", timeout=10000)
                    await page.set_viewport_size({"width": 2560, "height": 1080})
                    await page.click("#app > div")
                    div = await page.query_selector("#app > div")
                    await div.screenshot(
                        path=f"{IMAGE_PATH}/temp/cv_{event.user_id}.png",
                        timeout=100000,
                    )
                    await asyncio.get_event_loop().run_in_executor(
                        None, resize, f"{IMAGE_PATH}/temp/cv_{event.user_id}.png"
                    )
                    await parse_bilibili_json.send(
                        "[[_task|bilibili_parse]]" + image(f"cv_{event.user_id}.png", "temp")
                    )
                    await page.close()
                    logger.info(
                        f"USER {event.user_id} GROUP {event.group_id} 解析bilibili转发 {url}"
                    )
                except Exception as e:
                    logger.error(f"尝试解析bilibili专栏 {url} 失败 {type(e)}：{e}")
                    if page:
                        await page.close()
                return
    # BV
    if msg := get_message_text(event.json()):
        if "BV" in msg:
            index = msg.find("BV")
            if len(msg[index + 2 :]) >= 10:
                msg = msg[index : index + 12]
                url = f"https://www.bilibili.com/video/{msg}"
                vd_info = await video.Video(bvid=msg).get_info()
        elif "av" in msg:
            index = msg.find("av")
            if len(msg[index + 2 :]) >= 9:
                msg = msg[index + 2 : index + 11]
                if is_number(msg):
                    url = f"https://www.bilibili.com/video/{msg}"
                    vd_info = await video.Video(aid=int(msg)).get_info()
        elif "https://b23.tv" in msg:
            url = "https://" + msg[msg.find("b23.tv") : msg.find("b23.tv") + 13]
            res = await AsyncHttpx.get(url, timeout=7)
            url = str(res.url).split("?")[0]
            bvid = url.split("/")[-1]
            vd_info = await video.Video(bvid=bvid).get_info()
    if vd_info:
        if (
            url in _tmp.keys() and time.time() - _tmp[url] > 30
        ) or url not in _tmp.keys():
            _tmp[url] = time.time()
            aid = vd_info["aid"]
            title = vd_info["title"]
            author = vd_info["owner"]["name"]
            reply = vd_info["stat"]["reply"]  # 回复
            favorite = vd_info["stat"]["favorite"]  # 收藏
            coin = vd_info["stat"]["coin"]  # 投币
            # like = vd_info['stat']['like']      # 点赞
            # danmu = vd_info['stat']['danmaku']  # 弹幕
            date = time.strftime("%Y-%m-%d", time.localtime(vd_info["ctime"]))
            try:
                await parse_bilibili_json.send(
                    "[[_task|bilibili_parse]]" +
                    image(vd_info["pic"]) + f"\nav{aid}\n标题：{title}\n"
                    f"UP：{author}\n"
                    f"上传日期：{date}\n"
                    f"回复：{reply}，收藏：{favorite}，投币：{coin}\n"
                    f"{url}"
                )
            except ActionFailed:
                logger.warning(f"{event.group_id} 发送bilibili解析失败")
            else:
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 解析bilibili转发 {url}"
                )


def resize(path: str):
    A = BuildImage(0, 0, background=path, ratio=0.5)
    A.save(path)
