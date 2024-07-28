import re
import time
import uuid
from pathlib import Path
from typing import Any

import aiohttp
import ujson as json
from bilireq import video
from nonebot_plugin_alconna import Hyper
from nonebot_plugin_saa import Image, MessageFactory, Text

from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncPlaywright
from zhenxun.utils.user_agent import get_user_agent


class Parser:

    time_watch: dict[str, float] = {}

    @classmethod
    async def parse(cls, data: Any, raw: str | None = None) -> MessageFactory | None:
        """解析

        参数:
            data: data数据
            raw: 文本.

        返回:
            MessageFactory | None: 返回信息
        """
        if isinstance(data, Hyper) and data.raw:
            json_data = json.loads(data.raw)
            if video_info := await cls.__parse_video_share(json_data):
                return await cls.__handle_video_info(video_info)
            if path := await cls.__parse_news_share(json_data):
                return MessageFactory([Image(path)])
        if raw:
            return await cls.__search(raw)
        return None

    @classmethod
    async def __search(cls, message: str) -> MessageFactory | None:
        """根据bv，av，链接获取视频信息

        参数:
            message: 文本内容

        返回:
            MessageFactory | None: 返回信息
        """
        if "BV" in message:
            index = message.find("BV")
            if len(message[index + 2 :]) >= 10:
                msg = message[index : index + 12]
                url = f"https://www.bilibili.com/video/{msg}"
                return await cls.__handle_video_info(
                    await video.get_video_base_info(msg), url
                )
        elif "av" in message:
            index = message.find("av")
            if len(message[index + 2 :]) >= 1:
                if r := re.search(r"av(\d+)", message):
                    url = f"https://www.bilibili.com/video/av{r.group(1)}"
                    return await cls.__handle_video_info(
                        await video.get_video_base_info(f"av{r.group(1)}"), url
                    )
        elif "https://b23.tv" in message:
            url = (
                "https://"
                + message[message.find("b23.tv") : message.find("b23.tv") + 14]
            )
            async with aiohttp.ClientSession(headers=get_user_agent()) as session:
                async with session.get(
                    url,
                    timeout=7,
                ) as response:
                    url = (str(response.url).split("?")[0]).strip("/")
                    bvid = url.split("/")[-1]
                    return await cls.__handle_video_info(
                        await video.get_video_base_info(bvid), url
                    )
        return None

    @classmethod
    async def __handle_video_info(
        cls, vd_info: dict, url: str = ""
    ) -> MessageFactory | None:
        """处理视频信息

        参数:
            vd_info: 视频数据
            url: 视频url.

        返回:
            MessageFactory | None: 返回信息
        """
        if url:
            if url in cls.time_watch.keys() and time.time() - cls.time_watch[url] < 30:
                logger.debug("b站 url 解析在30秒内重复， 跳过解析...")
                return None
            cls.time_watch[url] = time.time()
        aid = vd_info["aid"]
        title = vd_info["title"]
        author = vd_info["owner"]["name"]
        reply = vd_info["stat"]["reply"]  # 回复
        favorite = vd_info["stat"]["favorite"]  # 收藏
        coin = vd_info["stat"]["coin"]  # 投币
        # like = vd_info['stat']['like']      # 点赞
        # danmu = vd_info['stat']['danmaku']  # 弹幕
        date = time.strftime("%Y-%m-%d", time.localtime(vd_info["ctime"]))
        return MessageFactory(
            [
                Image(vd_info["pic"]),
                Text(
                    f"\nav{aid}\n标题：{title}\nUP：{author}\n上传日期：{date}\n回复：{reply}，收藏：{favorite}，投币：{coin}\n{url}"
                ),
            ]
        )

    @classmethod
    async def __parse_video_share(cls, data: dict) -> dict | None:
        """解析视频转发

        参数:
            data: data数据

        返回:
            dict | None: 视频信息
        """
        try:
            if data["meta"]["detail_1"]["title"] == "哔哩哔哩":
                try:
                    async with aiohttp.ClientSession(
                        headers=get_user_agent()
                    ) as session:
                        async with session.get(
                            data["meta"]["detail_1"]["qqdocurl"],
                            timeout=7,
                        ) as response:
                            url = str(response.url).split("?")[0]
                            if url[-1] == "/":
                                url = url[:-1]
                            bvid = url.split("/")[-1]
                            return await video.get_video_base_info(bvid)
                except Exception as e:
                    logger.warning("解析b站视频失败", e=e)
        except Exception as e:
            pass
        return None

    @classmethod
    async def __parse_news_share(cls, data: dict) -> Path | None:
        """解析b站专栏

        参数:
            data: data数据

        返回:
            Path | None: 截图路径
        """
        try:
            if data["meta"]["news"]["desc"] == "哔哩哔哩专栏":
                try:
                    url = data["meta"]["news"]["jumpUrl"]
                    async with AsyncPlaywright.new_page() as page:
                        await page.goto(url, wait_until="networkidle", timeout=10000)
                        await page.set_viewport_size({"width": 2560, "height": 1080})
                        try:
                            await page.locator("div.bili-mini-close-icon").click()
                        except Exception:
                            pass
                        if div := await page.query_selector("#app > div"):
                            path = TEMP_PATH / f"bl_share_{uuid.uuid1()}.png"
                            await div.screenshot(
                                path=path,
                                timeout=100000,
                            )
                            return path
                except Exception as e:
                    logger.warning("解析b站专栏失败", e=e)
        except Exception as e:
            pass
        return None
