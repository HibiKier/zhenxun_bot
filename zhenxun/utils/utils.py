import os
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import pypinyin
import pytz

from zhenxun.services.log import logger


class WithdrawManager:
    """
    消息撤回
    """

    _data = {}

    @classmethod
    def append(cls, message_id: str, second: int):
        """添加一个撤回消息id和时间

        参数:
            message_id: 撤回消息id
            time: 延迟时间
        """
        cls._data[message_id] = second

    @classmethod
    def remove(cls, message_id: str):
        """删除一个数据

        参数:
            message_id: 撤回消息id
        """
        if message_id in cls._data:
            del cls._data[message_id]


class ResourceDirManager:
    """
    临时文件管理器
    """

    temp_path = []

    @classmethod
    def __tree_append(cls, path: Path):
        """递归添加文件夹

        参数:
            path: 文件夹路径
        """
        for f in os.listdir(path):
            file = path / f
            if file.is_dir():
                if file not in cls.temp_path:
                    cls.temp_path.append(file)
                    logger.debug(f"添加临时文件夹: {path}")
                cls.__tree_append(file)

    @classmethod
    def add_temp_dir(cls, path: str | Path, tree: bool = False):
        """添加临时清理文件夹，这些文件夹会被自动清理

        参数:
            path: 文件夹路径
            tree: 是否递归添加文件夹
        """
        if isinstance(path, str):
            path = Path(path)
        if path not in cls.temp_path:
            cls.temp_path.append(path)
            logger.debug(f"添加临时文件夹: {path}")
        if tree:
            cls.__tree_append(path)


class CountLimiter:
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


def cn2py(word: str) -> str:
    """将字符串转化为拼音

    参数:
        word: 文本
    """
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        temp += "".join(i)
    return temp


async def get_user_avatar(uid: int | str) -> bytes | None:
    """快捷获取用户头像

    参数:
        uid: 用户id
    """
    url = f"http://q1.qlogo.cn/g?b=qq&nk={uid}&s=160"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except Exception as e:
                logger.error("获取用户头像错误", "Util", target=uid)
    return None


async def get_group_avatar(gid: int | str) -> bytes | None:
    """快捷获取用群头像

    参数:
        :param gid: 群号
    """
    url = f"http://p.qlogo.cn/gh/{gid}/{gid}/640/"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except Exception as e:
                logger.error("获取群头像错误", "Util", target=gid)
    return None
