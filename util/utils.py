import time
from datetime import datetime, timedelta
from collections import defaultdict
from nonebot import require
import nonebot
import json
import pytz
from configs.path_config import TXT_PATH
from configs.config import system_proxy
import pypinyin


scheduler = require('nonebot_plugin_apscheduler').scheduler


# 次数检测
class CountLimiter:
    def __init__(self, max):
        self.count = defaultdict(int)
        self.max = max

    def add(self, key):
        self.count[key] += 1

    def check(self, key) -> bool:
        if self.count[key] >= self.max:
            self.count[key] = 0
            return True
        return False


# 用户正在执行此命令
class UserExistLimiter:
    def __init__(self):
        self.mbool = defaultdict(bool)
        self.time = time.time()

    def set_True(self, key):
        self.time = time.time()
        self.mbool[key] = True

    def set_False(self, key):
        self.mbool[key] = False

    def check(self, key):
        if time.time() - self.time > 30:
            self.set_False(key)
            return False
        return self.mbool[key]


# 命令cd
class FreqLimiter:
    def __init__(self, default_cd_seconds):
        self.next_time = defaultdict(float)
        self.default_cd = default_cd_seconds

    def check(self, key) -> bool:
        return time.time() >= self.next_time[key]

    def start_cd(self, key, cd_time=0):
        self.next_time[key] = time.time() + (cd_time if cd_time > 0 else self.default_cd)

    def left_time(self, key) -> float:
        return self.next_time[key] - time.time()


static_flmt = FreqLimiter(15)


# 恶意触发命令检测
class BanCheckLimiter:
    def __init__(self, default_check_time: float = 5, default_count: int = 4):
        self.mint = defaultdict(int)
        self.mtime = defaultdict(float)
        self.default_check_time = default_check_time
        self.default_count = default_count

    def add(self, key):
        if self.mint[key] == 1:
            self.mtime[key] = time.time()
        self.mint[key] += 1

    def check(self, key) -> bool:
        # print(self.mint[key])
        # print(time.time() - self.mtime[key])
        if time.time() - self.mtime[key] > self.default_check_time:
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return False
        if self.mint[key] >= self.default_count and time.time() - self.mtime[key] < self.default_check_time:
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return True
        return False


# 每日次数
class DailyNumberLimiter:
    tz = pytz.timezone('Asia/Shanghai')

    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        now = datetime.now(self.tz)
        day = (now - timedelta(hours=5)).day
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


def is_number(s) -> bool:
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


# 获取bot
def get_bot():
    return list(nonebot.get_bots().values())[0]


def get_message_at(data: str) -> list:
    qq_list = []
    data = json.loads(data)
    try:
        for msg in data['message']:
            if msg['type'] == 'at':
                qq_list.append(int(msg['data']['qq']))
        return qq_list
    except Exception:
        return []


def get_message_imgs(data: str) -> list:
    img_list = []
    data = json.loads(data)
    try:
        for msg in data['message']:
            if msg['type'] == 'image':
                img_list.append(msg['data']['url'])
        return img_list
    except Exception:
        return []


def get_message_text(data: str) -> str:
    data = json.loads(data)
    result = ''
    try:
        for msg in data['message']:
            if msg['type'] == 'text':
                result += msg['data']['text'].strip() + ' '
        return result.strip()
    except Exception:
        return ''


def get_message_type(data: str) -> str:
    return json.loads(data)['message_type']


def get_message_record(data: str) -> str:
    data = json.loads(data)
    try:
        for msg in data['message']:
            if msg['type'] == 'record':
                return msg['data']['url']
        return ''
    except Exception:
        return ''


def get_message_json(data: str) -> dict:
    data = json.loads(data)
    try:
        for msg in data['message']:
            if msg['type'] == 'json':
                return msg['data']
        return {}
    except Exception:
        return {}


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


# 获取文本加密后的cookie
def get_cookie_text(cookie_name: str) -> str:
    with open(TXT_PATH + "cookie/" + cookie_name + ".txt", 'r') as f:
        return f.read()


# 获取本地http代理
def get_local_proxy():
    # from urllib.request import getproxies
    # import platform
    # proxy = getproxies()['http']
    # if platform.system() != 'Windows':
    #     proxy = 'http://' + proxy
    return system_proxy if system_proxy else None


# 判断是否为中文
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def user_avatar(qq):
    return f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160'


def group_avatar(group_id):
    return f'http://p.qlogo.cn/gh/{group_id}/{group_id}/640/'


def cn2py(word) -> str:
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        temp += ''.join(i)
    return temp

