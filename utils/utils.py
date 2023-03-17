import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, Optional, Set, Type, Union

import httpx
import nonebot
import pypinyin
import pytz
from nonebot import require
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher, matchers

from configs.config import SYSTEM_PROXY, Config
from services.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

scheduler = scheduler

# 全局字典
GDict = {
    "run_sql": [],  # 需要启动前运行的sql语句
    "_shop_before_handle": {},  # 商品使用前函数
    "_shop_after_handle": {},  # 商品使用后函数
}


CN2NUM = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "十一": 11,
    "十二": 12,
    "十三": 13,
    "十四": 14,
    "十五": 15,
    "十六": 16,
    "十七": 17,
    "十八": 18,
    "十九": 19,
    "二十": 20,
    "二十一": 21,
    "二十二": 22,
    "二十三": 23,
    "二十四": 24,
    "二十五": 25,
    "二十六": 26,
    "二十七": 27,
    "二十八": 28,
    "二十九": 29,
    "三十": 30,
}


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


def is_number(s: Union[int, str]) -> bool:
    """
    说明:
        检测 s 是否为数字
    参数:
        :param s: 文本
    """
    if isinstance(s, int):
        return True
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


def get_bot(id_: Optional[str] = None) -> Optional[Bot]:
    """
    说明:
        获取 bot 对象
    """
    try:
        return nonebot.get_bot(id_)
    except ValueError:
        return None


def get_matchers(distinct: bool = False) -> List[Type[Matcher]]:
    """
    说明:
        获取所有matcher
    参数:
        distinct: 去重
    """
    _matchers = []
    temp = []
    for i in matchers.keys():
        for matcher in matchers[i]:
            if distinct and matcher.plugin_name in temp:
                continue
            temp.append(matcher.plugin_name)
            _matchers.append(matcher)
    return _matchers


def get_message_at(data: Union[str, Message]) -> List[int]:
    """
    说明:
        获取消息中所有的 at 对象的 qq
    参数:
        :param data: event.json(), event.message
    """
    qq_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg and msg.get("type") == "at":
                    qq_list.append(int(msg["data"]["qq"]))
    else:
        for seg in data:
            if seg.type == "at":
                qq_list.append(seg.data["qq"])
    return qq_list


def get_message_img(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 图片 的链接
    参数:
        :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "image":
                    img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list


def get_message_face(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 face Id
    参数:
        :param data: event.json()
    """
    face_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "face":
                    face_list.append(msg["data"]["id"])
    else:
        for seg in data["face"]:
            face_list.append(seg.data["id"])
    return face_list


def get_message_img_file(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 图片file
    参数:
        :param data: event.json()
    """
    file_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "image":
                    file_list.append(msg["data"]["file"])
    else:
        for seg in data["image"]:
            file_list.append(seg.data["file"])
    return file_list


def get_message_text(data: Union[str, Message]) -> str:
    """
    说明:
        获取消息中 纯文本 的信息
    参数:
        :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            if isinstance(message, str):
                return message.strip()
            for msg in message:
                if msg["type"] == "text":
                    result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result.strip()


def get_message_record(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有 语音 的链接
    参数:
        :param data: event.json()
    """
    record_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "record":
                    record_list.append(msg["data"]["url"])
    else:
        for seg in data["record"]:
            record_list.append(seg.data["url"])
    return record_list


def get_message_json(data: str) -> List[dict]:
    """
    说明:
        获取消息中所有 json
    参数:
        :param data: event.json()
    """
    try:
        json_list = []
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "json":
                    json_list.append(msg["data"])
        return json_list
    except KeyError:
        return []


def get_local_proxy() -> Optional[str]:
    """
    说明:
        获取 config.py 中设置的代理
    """
    return SYSTEM_PROXY or None


def is_chinese(word: str) -> bool:
    """
    说明:
        判断字符串是否为纯中文
    参数:
        :param word: 文本
    """
    for ch in word:
        if not "\u4e00" <= ch <= "\u9fff":
            return False
    return True


async def get_user_avatar(qq: int) -> Optional[bytes]:
    """
    说明:
        快捷获取用户头像
    参数:
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
    说明:
        快捷获取用群头像
    参数:
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
    说明:
        将字符串转化为拼音
    参数:
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
    说明:
        根据配置改变图片大小和反代链接
    参数:
        :param url: 图片原图链接
        :param size: 模式
        :param nginx_url: 反代
    """
    if size == "master":
        img_sp = url.rsplit(".", maxsplit=1)
        url = img_sp[0]
        img_type = img_sp[1]
        url = url.replace("original", "master") + f"_master1200.{img_type}"
    if not nginx_url:
        nginx_url = Config.get_config("pixiv", "PIXIV_NGINX_URL")
    if nginx_url:
        url = (
            url.replace("i.pximg.net", nginx_url)
            .replace("i.pixiv.cat", nginx_url)
            .replace("_webp", "")
        )
    return url


def change_img_md5(path_file: Union[str, Path]) -> bool:
    """
    说明:
        改变图片MD5
    参数:
    :param path_file: 图片路径
    """
    try:
        with open(path_file, "a") as f:
            f.write(str(int(time.time() * 1000)))
        return True
    except Exception as e:
        logger.warning(f"改变图片MD5错误 Path：{path_file}", e=e)
    return False


async def broadcast_group(
    message: Union[str, Message, MessageSegment],
    bot: Optional[Union[Bot, List[Bot]]] = None,
    bot_id: Optional[Union[str, Set[str]]] = None,
    ignore_group: Optional[Set[int]] = None,
    check_func: Optional[Callable[[int], bool]] = None,
    log_cmd: Optional[str] = None,
):
    """获取所有Bot或指定Bot对象广播群聊

    Args:
        message (Any): 广播消息内容
        bot (Optional[Bot], optional): 指定bot对象. Defaults to None.
        bot_id (Optional[str], optional): 指定bot id. Defaults to None.
        ignore_group (Optional[List[int]], optional): 忽略群聊列表. Defaults to None.
        check_func (Optional[Callable[[int], bool]], optional): 发送前对群聊检测方法，判断是否发送. Defaults to None.
        log_cmd (Optional[str], optional): 日志标记. Defaults to None.
    """
    if not message:
        raise ValueError("群聊广播消息不能为空")
    bot_dict = nonebot.get_bots()
    bot_list: List[Bot] = []
    if bot:
        if isinstance(bot, list):
            bot_list = bot
        else:
            bot_list.append(bot)
    elif bot_id:
        _bot_id_list = bot_id
        if isinstance(bot_id, str):
            _bot_id_list = [bot_id]
        for id_ in _bot_id_list:
            if bot_id in bot_dict:
                bot_list.append(bot_dict[bot_id])
            else:
                logger.warning(f"Bot:{id_} 对象未连接或不存在")
    else:
        bot_list = list(bot_dict.values())
    _used_group = []
    for _bot in bot_list:
        try:
            if _group_list := await _bot.get_group_list():
                group_id_list = [g["group_id"] for g in _group_list]
                for group_id in set(group_id_list):
                    try:
                        if (
                            ignore_group and group_id in ignore_group
                        ) or group_id in _used_group:
                            continue
                        if check_func and not check_func(group_id):
                            continue
                        _used_group.append(group_id)
                        await _bot.send_group_msg(group_id=group_id, message=message)
                    except Exception as e:
                        logger.error(
                            f"广播群发消息失败: {message}",
                            command=log_cmd,
                            group_id=group_id,
                            e=e,
                        )
        except Exception as e:
            logger.error(f"Bot: {_bot.self_id} 获取群聊列表失败", command=log_cmd, e=e)


async def broadcast_superuser(
    message: Union[str, Message, MessageSegment],
    bot: Optional[Union[Bot, List[Bot]]] = None,
    bot_id: Optional[Union[str, Set[str]]] = None,
    ignore_superuser: Optional[Set[int]] = None,
    check_func: Optional[Callable[[int], bool]] = None,
    log_cmd: Optional[str] = None,
):
    """获取所有Bot或指定Bot对象广播超级用户

    Args:
        message (Any): 广播消息内容
        bot (Optional[Bot], optional): 指定bot对象. Defaults to None.
        bot_id (Optional[str], optional): 指定bot id. Defaults to None.
        ignore_superuser (Optional[List[int]], optional): 忽略的超级用户id. Defaults to None.
        check_func (Optional[Callable[[int], bool]], optional): 发送前对群聊检测方法，判断是否发送. Defaults to None.
        log_cmd (Optional[str], optional): 日志标记. Defaults to None.
    """
    if not message:
        raise ValueError("超级用户广播消息不能为空")
    bot_dict = nonebot.get_bots()
    bot_list: List[Bot] = []
    if bot:
        if isinstance(bot, list):
            bot_list = bot
        else:
            bot_list.append(bot)
    elif bot_id:
        _bot_id_list = bot_id
        if isinstance(bot_id, str):
            _bot_id_list = [bot_id]
        for id_ in _bot_id_list:
            if bot_id in bot_dict:
                bot_list.append(bot_dict[bot_id])
            else:
                logger.warning(f"Bot:{id_} 对象未连接或不存在")
    else:
        bot_list = list(bot_dict.values())
    _used_user = []
    for _bot in bot_list:
        try:
            for user_id in _bot.config.superusers:
                try:
                    if (
                        ignore_superuser and int(user_id) in ignore_superuser
                    ) or user_id in _used_user:
                        continue
                    if check_func and not check_func(int(user_id)):
                        continue
                    _used_user.append(user_id)
                    await _bot.send_private_message(
                        user_id=int(user_id), message=message
                    )
                except Exception as e:
                    logger.error(
                        f"广播超级用户发消息失败: {message}",
                        command=log_cmd,
                        user_id=user_id,
                        e=e,
                    )
        except Exception as e:
            logger.error(f"Bot: {_bot.self_id} 获取群聊列表失败", command=log_cmd, e=e)
