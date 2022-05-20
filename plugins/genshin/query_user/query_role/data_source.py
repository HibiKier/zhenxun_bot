from typing import Optional, List, Dict, Union
from .draw_image import init_image, get_genshin_image
from nonebot.adapters.onebot.v11 import MessageSegment
from .._utils import get_ds, element_mastery
from services.log import logger
from utils.http_utils import AsyncHttpx
from configs.config import Config
from .._models import Genshin

try:
    import ujson as json
except ModuleNotFoundError:
    import json


async def query_role_data(
    user_id: int, uid: int, mys_id: Optional[str] = None, nickname: Optional[str] = None
) -> Optional[Union[MessageSegment, str]]:
    uid = str(uid)
    if uid[0] == "1" or uid[0] == "2":
        server_id = "cn_gf01"
    elif uid[0] == "5":
        server_id = "cn_qd01"
    else:
        return None
    return await get_image(user_id, uid, server_id, mys_id, nickname)


async def get_image(
    user_id: int,
    uid: str,
    server_id: str,
    mys_id: Optional[str] = None,
    nickname: Optional[str] = None,
) -> Optional[Union[MessageSegment, str]]:
    """
    生成图片
    :param user_id：用户qq
    :param uid: 用户uid
    :param server_id: 服务器
    :param mys_id: 米游社id
    :param nickname: QQ昵称
    :return:
    """
    data, code = await get_info(uid, server_id)
    if code != 200:
        return data
    if data:
        char_data_list, role_data, world_data_dict, home_data_list = parsed_data(data)
        mys_data = await get_mys_data(uid, mys_id)
        if mys_data:
            nickname = None
        if char_data_list:
            char_detailed_data = await get_character(
                uid, [x["id"] for x in char_data_list], server_id
            )
            _x = {}
            if char_detailed_data:
                for char in char_detailed_data["avatars"]:
                    _x[char["name"]] = {
                        "weapon": char["weapon"]["name"],
                        "weapon_image": char["weapon"]["icon"],
                        "level": char["weapon"]["level"],
                        "affix_level": char["weapon"]["affix_level"],
                    }

            await init_image(world_data_dict, char_data_list, _x, home_data_list)
            return await get_genshin_image(
                user_id,
                uid,
                char_data_list,
                role_data,
                world_data_dict,
                home_data_list,
                _x,
                mys_data,
                nickname,
            )
    return "未找到用户数据..."


# Github-@lulu666lulu https://github.com/Azure99/GenshinPlayerQuery/issues/20
"""
{body:"",query:{"action_ticket": undefined, "game_biz": "hk4e_cn”}}
对应 https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn //查询米哈游账号下绑定的游戏(game_biz可留空)
{body:"",query:{"uid": 12345(被查询账号米哈游uid)}}
对应 https://api-takumi.mihoyo.com/game_record/app/card/wapi/getGameRecordCard?uid=
{body:"",query:{'role_id': '查询账号的uid(游戏里的)' ,'server': '游戏服务器'}}
对应 https://api-takumi.mihoyo.com/game_record/app/genshin/api/index?server= server信息 &role_id= 游戏uid
{body:"",query:{'role_id': '查询账号的uid(游戏里的)' , 'schedule_type': 1(我这边只看到出现过1和2), 'server': 'cn_gf01'}}
对应 https://api-takumi.mihoyo.com/game_record/app/genshin/api/spiralAbyss?schedule_type=1&server= server信息 &role_id= 游戏uid
{body:"",query:{game_id: 2(目前我知道有崩坏3是1原神是2)}}
对应 https://api-takumi.mihoyo.com/game_record/app/card/wapi/getAnnouncement?game_id=    这个是公告api
b=body q=query
其中b只在post的时候有内容，q只在get的时候有内容
"""


async def get_info(uid_: str, server_id: str) -> "Optional[Union[dict, str]], int":
    try:
        req = await AsyncHttpx.get(
            url=f"https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/index?server={server_id}&role_id={uid_}",
            headers={
                "Accept": "application/json, text/plain, */*",
                "DS": get_ds(f"role_id={uid_}&server={server_id}"),
                "Origin": "https://webstatic.mihoyo.com",
                "x-rpc-app_version": Config.get_config("genshin", "mhyVersion"),
                "User-Agent": "Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0",
                "x-rpc-client_type": Config.get_config("genshin", "client_type"),
                "Referer": "https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "X-Requested-With": "com.mihoyo.hyperion",
                "Cookie": await Genshin.get_user_cookie(int(uid_))
            },
        )
        data = req.json()
        if data["message"] == "OK":
            return data["data"], 200
        return data["message"], 999
    except Exception as e:
        logger.error(f"访问失败，请重试！ {type(e)}: {e}")
    return None, -1


async def get_character(
    uid: str, character_ids: List[str], server_id="cn_gf01"
) -> Optional[dict]:
    try:
        req = await AsyncHttpx.post(
            url="https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/character",
            headers={
                "Accept": "application/json, text/plain, */*",
                "DS": get_ds(
                    "",
                    {
                        "character_ids": character_ids,
                        "role_id": uid,
                        "server": server_id,
                    },
                ),
                "Origin": "https://webstatic.mihoyo.com",
                "Cookie": await Genshin.get_user_cookie(int(uid)),
                "x-rpc-app_version": Config.get_config("genshin", "mhyVersion"),
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1",
                "x-rpc-client_type": "5",
                "Referer": "https://webstatic.mihoyo.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,en-US;q=0.8",
                "X-Requested-With": "com.mihoyo.hyperion",
            },
            json={"character_ids": character_ids, "role_id": uid, "server": server_id},
        )
        data = req.json()
        if data["message"] == "OK":
            return data["data"]
    except Exception as e:
        logger.error(f"访问失败，请重试！ {type(e)}: {e}")
    return None


def parsed_data(
    data: dict,
) -> "Optional[List[Dict[str, str]]], Dict[str, str], Optional[List[Dict[str, str]]], Optional[List[Dict[str, str]]]":
    """
    解析数据
    :param data: 数据
    """
    char_data_list = []
    for char in data["avatars"]:
        _x = {
            "id": char["id"],
            "image": char["image"],
            "name": char["name"],
            "element": element_mastery[char["element"].lower()],
            "fetter": char["fetter"],
            "level": char["level"],
            "rarity": char["rarity"],
            "actived_constellation_num": char["actived_constellation_num"],
        }
        char_data_list.append(_x)
    role_data = {
        "active_day_number": data["stats"]["active_day_number"],  # 活跃天数
        "achievement_number": data["stats"]["achievement_number"],  # 达成成就数量
        "win_rate": data["stats"]["win_rate"],
        "anemoculus_number": data["stats"]["anemoculus_number"],  # 风神瞳已收集
        "geoculus_number": data["stats"]["geoculus_number"],  # 岩神瞳已收集
        "avatar_number": data["stats"]["avatar_number"],  # 获得角色数量
        "way_point_number": data["stats"]["way_point_number"],  # 传送点已解锁
        "domain_number": data["stats"]["domain_number"],  # 秘境解锁数量
        "spiral_abyss": data["stats"]["spiral_abyss"],  # 深渊当期进度
        "precious_chest_number": data["stats"]["precious_chest_number"],  # 珍贵宝箱
        "luxurious_chest_number": data["stats"]["luxurious_chest_number"],  # 华丽宝箱
        "exquisite_chest_number": data["stats"]["exquisite_chest_number"],  # 精致宝箱
        "magic_chest_number": data["stats"]["magic_chest_number"],  # 奇馈宝箱
        "common_chest_number": data["stats"]["common_chest_number"],  # 普通宝箱
        "electroculus_number": data["stats"]["electroculus_number"],  # 雷神瞳已收集
    }
    world_data_dict = {}
    for world in data["world_explorations"]:
        _x = {
            "level": world["level"],  # 声望等级
            "exploration_percentage": world["exploration_percentage"],  # 探索进度
            "image": world["icon"],
            "name": world["name"],
            "offerings": world["offerings"],
            "icon": world["icon"]
        }
        world_data_dict[world["name"]] = _x
    home_data_list = []
    for home in data["homes"]:
        _x = {
            "level": home["level"],  # 最大信任等级
            "visit_num": home["visit_num"],  # 最高历史访客数
            "comfort_num": home["comfort_num"],  # 最高洞天仙力
            "item_num": home["item_num"],  # 已获得摆件数量
            "name": home["name"],
            "icon": home["icon"],
            "comfort_level_name": home["comfort_level_name"],
            "comfort_level_icon": home["comfort_level_icon"],
        }
        home_data_list.append(_x)
    return char_data_list, role_data, world_data_dict, home_data_list


async def get_mys_data(uid: str, mys_id: Optional[str]) -> Optional[List[Dict]]:
    """
    获取用户米游社数据
    :param uid: 原神uid
    :param mys_id: 米游社id
    """
    if mys_id:
        try:
            req = await AsyncHttpx.get(
                url=f"https://api-takumi-record.mihoyo.com/game_record/card/wapi/getGameRecordCard?uid={mys_id}",
                headers={
                    "DS": get_ds(f"uid={mys_id}"),
                    "x-rpc-app_version": Config.get_config("genshin", "mhyVersion"),
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.11.1",
                    "x-rpc-client_type": "5",
                    "Referer": "https://webstatic.mihoyo.com/",
                    "Cookie": await Genshin.get_user_cookie(int(uid))
                },
            )
            data = req.json()
            if data["message"] == "OK":
                return data["data"]["list"]
        except Exception as e:
            logger.error(f"访问失败，请重试！ {type(e)}: {e}")
    return None
