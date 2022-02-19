from datetime import datetime
from collections import defaultdict
from nonebot import require
from configs.config import SYSTEM_PROXY
from typing import List, Union, Optional, Type, Any
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.matcher import matchers, Matcher
import httpx
import nonebot
import pytz
import pypinyin
import time

try:
    import ujson as json
except ModuleNotFoundError:
    import json


scheduler = require("nonebot_plugin_apscheduler").scheduler


class CountLimiter:
    """
    次数检测工具，检测调用次数是否超过设定值
    """

    def __init__(self, max_count: int):
        self.count = defaultdict(int)
        self.max_count = max_count

    def add(self, key: Any):
        self.count[key] += 1

    def check(self, key: Any) -> bool:
        if self.count[key] >= self.max_count:
            self.count[key] = 0
            return True
        return False


class UserBlockLimiter:
    """
    检测用户是否正在调用命令
    """

    def __init__(self):
        self.flag_data = defaultdict(bool)
        self.time = time.time()

    def set_true(self, key: Any):
        self.time = time.time()
        self.flag_data[key] = True

    def set_false(self, key: Any):
        self.flag_data[key] = False

    def check(self, key: Any) -> bool:
        if time.time() - self.time > 30:
            self.set_false(key)
            return False
        return self.flag_data[key]


class FreqLimiter:
    """
    命令冷却，检测用户是否处于冷却状态
    """

    def __init__(self, default_cd_seconds: int):
        self.next_time = defaultdict(float)
        self.default_cd = default_cd_seconds

    def check(self, key: Any) -> bool:
        return time.time() >= self.next_time[key]

    def start_cd(self, key: Any, cd_time: int = 0):
        self.next_time[key] = time.time() + (
            cd_time if cd_time > 0 else self.default_cd
        )

    def left_time(self, key: Any) -> float:
        return self.next_time[key] - time.time()


static_flmt = FreqLimiter(15)


class BanCheckLimiter:
    """
    恶意命令触发检测
    """

    def __init__(self, default_check_time: float = 5, default_count: int = 4):
        self.mint = defaultdict(int)
        self.mtime = defaultdict(float)
        self.default_check_time = default_check_time
        self.default_count = default_count

    def add(self, key: Union[str, int, float]):
        if self.mint[key] == 1:
            self.mtime[key] = time.time()
        self.mint[key] += 1

    def check(self, key: Union[str, int, float]) -> bool:
        if time.time() - self.mtime[key] > self.default_check_time:
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return False
        if (
            self.mint[key] >= self.default_count
            and time.time() - self.mtime[key] < self.default_check_time
        ):
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return True
        return False


class DailyNumberLimiter:
    """
    每日调用命令次数限制
    """

    tz = pytz.timezone("Asia/Shanghai")

    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        day = datetime.now(self.tz).day
        if day != self.today:
            self.today = day
            self.count.clear()
        return bool(self.count[key] < self.max)

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, num=1):
        self.count[key] += num

    def reset(self, key):
        self.count[key] = 0


def is_number(s: str) -> bool:
    """
    说明：
        检测 s 是否为数字
    参数：
        :param s: 文本
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def get_bot() -> Optional[Bot]:
    """
    说明：
        获取 bot 对象
    """
    try:
        return list(nonebot.get_bots().values())[0]
    except IndexError:
        return None


def get_matchers() -> List[Type[Matcher]]:
    """
    获取所有插件
    """
    _matchers = []
    for i in matchers.keys():
        for matcher in matchers[i]:
            _matchers.append(matcher)
    return _matchers


def get_message_at(data: Union[str, Message]) -> List[int]:
    """
    说明：
        获取消息中所有的 at 对象的 qq
    参数：
        :param data: event.json()
    """
    qq_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                qq_list.append(int(msg["data"]["qq"]))
    else:
        for seg in data:
            if seg.type == "image":
                qq_list.append(seg.data["url"])
    return qq_list


def get_message_img(data: Union[str, Message]) -> List[str]:
    """
    说明：
        获取消息中所有的 图片 的链接
    参数：
        :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "image":
                img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list


def get_message_text(data: Union[str, Message]) -> str:
    """
    说明：
        获取消息中 纯文本 的信息
    参数：
        :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "text":
                result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result


def get_message_record(data: Union[str, Message]) -> List[str]:
    """
    说明：
        获取消息中所有 语音 的链接
    参数：
        :param data: event.json()
    """
    record_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "record":
                record_list.append(msg["data"]["url"])
    else:
        for seg in data["record"]:
            record_list.append(seg.data["url"])
    return record_list


def get_message_json(data: str) -> List[dict]:
    """
    说明：
        获取消息中所有 json
    参数：
        :param data: event.json()
    """
    try:
        json_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "json":
                json_list.append(msg["data"])
        return json_list
    except KeyError:
        return []


def get_local_proxy():
    """
    说明：
        获取 config.py 中设置的代理
    """
    return SYSTEM_PROXY if SYSTEM_PROXY else None


def is_chinese(word: str) -> bool:
    """
    说明：
        判断字符串是否为纯中文
    参数：
        :param word: 文本
    """
    for ch in word:
        if not "\u4e00" <= ch <= "\u9fff":
            return False
    return True


async def get_user_avatar(qq: int) -> Optional[bytes]:
    """
    说明：
        快捷获取用户头像
    参数：
        :param qq: qq号
    """
    url = f"http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except TimeoutError:
                pass
    return None


async def get_group_avatar(group_id: int) -> Optional[bytes]:
    """
    说明：
        快捷获取用群头像
    参数：
        :param group_id: 群号
    """
    url = f"http://p.qlogo.cn/gh/{group_id}/{group_id}/640/"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except TimeoutError:
                pass
    return None


def cn2py(word: str) -> str:
    """
    说明：
        将字符串转化为拼音
    参数：
        :param word: 文本
    """
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        temp += "".join(i)
    return temp


def change_pixiv_image_links(
    url: str, size: Optional[str] = None, nginx_url: Optional[str] = None
):
    """
    说明：
        根据配置改变图片大小和反代链接
    参数：
        :param url: 图片原图链接
        :param size: 模式
        :param nginx_url: 反代
    """
    if size == "master":
        img_sp = url.rsplit(".", maxsplit=1)
        url = img_sp[0]
        img_type = img_sp[1]
        url = url.replace("original", "master") + f"_master1200.{img_type}"
    if nginx_url:
        url = (
            url.replace("i.pximg.net", nginx_url)
            .replace("i.pixiv.cat", nginx_url)
            .replace("_webp", "")
        )
    return url
