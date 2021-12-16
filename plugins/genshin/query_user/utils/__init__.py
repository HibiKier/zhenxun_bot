from configs.config import Config
import json
import time
import random
import hashlib


def _md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def get_ds(q: str = "", b: dict = None):
    if b:
        br = json.dumps(b)
    else:
        br = ""
    s = Config.get_config("genshin", "salt")
    t = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    c = _md5("salt=" + s + "&t=" + t + "&r=" + r + "&b=" + br + "&q=" + q)
    return t + "," + r + "," + c


element_mastery = {
    "anemo": "风",
    "pyro": "火",
    "geo": "岩",
    "electro": "雷",
    "cryo": "冰",
    "hydro": "水",
    "dendro": "草",
    "none": "无",
}
