from utils.http_utils import AsyncHttpx
from configs.config import Config
from services.log import logger
from .._utils import random_hex, get_old_ds
from .._models import Genshin
from typing import Optional, Dict


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
            if status == "OK" and sign_info["is_sign"]:
                return f"\n原神签到成功！\n{get_im}\n本月漏签次数：{sign_info['sign_cnt_missed']}"
    else:
        return status
    return None


async def _sign(uid: int, server_id: str = "cn_gf01") -> Optional[Dict[str, str]]:
    """
    米游社签到
    :param uid: uid
    :param server_id: 服务器id
    """
    if str(uid)[0] == "5":
        server_id = "cn_qd01"
    try:
        req = await AsyncHttpx.post(
            url="https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign",
            headers={
                "User_Agent": "Mozilla/5.0 (Linux; Android 10; MIX 2 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 miHoYoBBS/2.3.0",
                "Cookie": await Genshin.get_user_cookie(int(uid), True),
                "x-rpc-device_id": random_hex(32),
                "Origin": "https://webstatic.mihoyo.com",
                "X_Requested_With": "com.mihoyo.hyperion",
                "DS": get_old_ds(),
                "x-rpc-client_type": "5",
                "Referer": "https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon",
                "x-rpc-app_version": "2.3.0",
            },
            json={"act_id": "e202009291139501", "uid": uid, "region": server_id},
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
