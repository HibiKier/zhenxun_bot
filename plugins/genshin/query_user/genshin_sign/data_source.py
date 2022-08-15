from utils.http_utils import AsyncHttpx
from configs.config import Config
from services.log import logger
from ..mihoyobbs_sign.setting import *
from .._models import Genshin
from typing import Optional, Dict
import hashlib
import random
import string
import uuid
import time


async def genshin_sign(uid: int) -> Optional[str]:
    """
    原神签到信息
    :param uid: uid
    """
    data = await _sign(uid)
    if not data:
        return "签到失败..."
    status = data["message"]
    if status == "OK":
        try:
            sign_info = await _get_sign_info(uid)
            if sign_info:
                sign_info = sign_info["data"]
                sign_list = await get_sign_reward_list()
                get_reward = sign_list["data"]["awards"][
                    int(sign_info["total_sign_day"]) - 1
                    ]["name"]
                reward_num = sign_list["data"]["awards"][
                    int(sign_info["total_sign_day"]) - 1
                    ]["cnt"]
                get_im = f"本次签到获得：{get_reward}x{reward_num}"
                logger.info("get_im:" + get_im + "\nsign_info:" + str(sign_info))
                if status == "OK" and sign_info["is_sign"]:
                    return f"原神签到成功！\n{get_im}\n本月漏签次数：{sign_info['sign_cnt_missed']}"
        except Exception as e:
            logger.error(f"原神签到发生错误 UID：{str(data)}")
            return f"原神签到发生错误: {str(data)}"
    else:
        return status
    if data["data"]["risk_code"] == 375:
        return "原神签到失败\n账号可能被风控，请前往米游社手动签到！"
    return str(data)


# 获取请求Header里的DS 当web为true则生成网页端的DS
def get_ds(web: bool) -> str:
    if web:
        n = mihoyobbs_Salt_web
    else:
        n = mihoyobbs_Salt
    i = str(timestamp())
    r = random_text(6)
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return f"{i},{r},{c}"


# 时间戳
def timestamp() -> int:
    return int(time.time())


def random_text(num: int) -> str:
    return ''.join(random.sample(string.ascii_lowercase + string.digits, num))


def md5(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


# 生成一个device id
def get_device_id(cookie) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_URL, cookie)).replace(
        '-', '').upper()


async def _sign(uid: int, server_id: str = "cn_gf01") -> Optional[Dict[str, str]]:
    """
    米游社签到
    :param uid: uid
    :param server_id: 服务器id
    """
    if str(uid)[0] == "5":
        server_id = "cn_qd01"
    try:
        cookie = await Genshin.get_user_cookie(uid, True)
        headers['DS'] = get_ds(web=True)
        headers['Referer'] = 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true' \
                             f'&act_id={genshin_Act_id}&utm_source=bbs&utm_medium=mys&utm_campaign=icon'
        headers['Cookie'] = cookie
        headers['x-rpc-device_id'] = get_device_id(cookie)
        req = await AsyncHttpx.post(
            url=genshin_Signurl,
            headers=headers,
            json={"act_id": genshin_Act_id, "uid": uid, "region": server_id},
        )
        return req.json()
    except Exception as e:
        logger.error(f"米游社签到发生错误 UID：{uid} {type(e)}：{e}")
    return None


async def get_sign_reward_list():
    """
    获取签到奖励列表
    """
    try:
        req = await AsyncHttpx.get(
            url="https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id=e202009291139501",
            headers={
                "x-rpc-app_version": str(Config.get_config("genshin", "mhyVersion")),
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1",
                "x-rpc-client_type": str(Config.get_config("genshin", "client_type")),
                "Referer": "https://webstatic.mihoyo.com/",
            },
        )
        return req.json()
    except Exception as e:
        logger.error(f"获取签到奖励列表发生错误 {type(e)}：{e}")
    return None


async def _get_sign_info(uid: int, server_id: str = "cn_gf01"):
    if str(uid)[0] == "5":
        server_id = "cn_qd01"
    try:
        req = await AsyncHttpx.get(
            url=f"https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?act_id=e202009291139501&region={server_id}&uid={uid}",
            headers={
                "x-rpc-app_version": str(Config.get_config("genshin", "mhyVersion")),
                "Cookie": await Genshin.get_user_cookie(int(uid), True),
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1",
                "x-rpc-client_type": str(Config.get_config("genshin", "client_type")),
                "Referer": "https://webstatic.mihoyo.com/",
            },
        )
        return req.json()
    except Exception as e:
        logger.error(f"获取签到信息发生错误 UID：{uid} {type(e)}：{e}")
    return None
