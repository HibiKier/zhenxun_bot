import asyncio
import random
import time
from datetime import datetime
from typing import List, Tuple, Union

import nonebot

from configs.config import Config
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.http_utils import AsyncHttpx
from utils.utils import broadcast_group, cn2py

from .config import CASE2ID
from .models.buff_skin import BuffSkin
from .models.buff_skin_log import BuffSkinLog
from .models.open_cases_user import OpenCasesUser

URL = "https://buff.163.com/api/market/goods"
# proxies = 'http://49.75.59.242:3128'

NAME2COLOR = {"军规级": "BLUE", "受限": "PURPLE", "保密": "PINK", "隐秘": "RED", "非凡": "KNIFE"}

CURRENT_CASES = []

driver = nonebot.get_driver()

BASE_PATH = IMAGE_PATH / "csgo_cases"


class CaseManager:

    CURRENT_CASES = []

    @classmethod
    async def reload(cls):
        cls.CURRENT_CASES = (
            await BuffSkin.annotate().distinct().values_list("case_name", flat=True)  # type: ignore
        )


async def update_case_data(case_name: str) -> str:
    """更新皮肤数据

    Args:
        case_name (str): 箱子名称

    Returns:
        _type_: _description_
    """
    if case_name not in CASE2ID:
        return "未在当前指定武器箱捏"
    session = Config.get_config("open_cases", "COOKIE")
    if not session:
        return "BUFF COOKIE为空捏!"
    db_skin_list = await BuffSkin.filter(case_name=case_name).all()
    db_skin_name_list = [
        skin.name + skin.skin_name + skin.abrasion for skin in db_skin_list
    ]
    data_list, total = await search_skin_page(case_name, 1)
    if isinstance(data_list, str):
        return data_list
    for page in range(2, total + 1):
        rand_time = random.randint(10, 50)
        logger.debug(f"访问随机等待时间: {rand_time}", "开箱更新")
        await asyncio.sleep(rand_time)
        data_list_, total = await search_skin_page(case_name, page)
        if isinstance(data_list_, list):
            data_list += data_list_
    create_list = []
    update_list = []
    log_list = []
    case_name_py = cn2py(case_name)
    now = datetime.now()
    for skin in data_list:
        name = skin.name + skin.skin_name + skin.abrasion
        skin.create_time = now
        skin.update_time = now
        if name in db_skin_name_list:
            update_list.append(skin)
        else:
            create_list.append(skin)
        log_list.append(
            BuffSkinLog(
                name=skin.name,
                case_name=skin.case_name,
                skin_name=skin.skin_name,
                is_stattrak=skin.is_stattrak,
                abrasion=skin.abrasion,
                color=skin.color,
                steam_price=skin.steam_price,
                weapon_type=skin.weapon_type,
                buy_max_price=skin.buy_max_price,
                buy_num=skin.buy_num,
                sell_min_price=skin.sell_min_price,
                sell_num=skin.sell_num,
                sell_reference_price=skin.sell_reference_price,
                create_time=now,
            )
        )
        name = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
        file_path = BASE_PATH / case_name_py / f"{cn2py(name)}.jpg"
        if not file_path.exists():
            logger.debug(f"下载皮肤 {name} 图片: {skin.img_url}...", "开箱更新")
            await AsyncHttpx.download_file(skin.img_url, file_path)
            rand_time = random.randint(1, 10)
            await asyncio.sleep(rand_time)
            logger.debug(f"图片下载随机等待时间: {rand_time}", "开箱更新")
        else:
            logger.debug(f"皮肤 {name} 图片已存在...", "开箱更新")
    if create_list:
        logger.debug(f"更新武器箱: [<u><e>{case_name}</e></u>], 创建 {len(create_list)} 个皮肤!")
        await BuffSkin.bulk_create(create_list, 10)
    if update_list:
        logger.debug(f"更新武器箱: [<u><c>{case_name}</c></u>], 更新 {len(create_list)} 个皮肤!")
        await BuffSkin.bulk_update(
            update_list,
            [
                "skin_price",
                "steam_price",
                "buy_max_price",
                "buy_num",
                "sell_min_price",
                "sell_num",
                "sell_reference_price",
                "update_time",
            ],
            10,
        )
    if log_list:
        logger.debug(f"更新武器箱: [<u><e>{case_name}</e></u>], 新增 {len(log_list)} 条皮肤日志!")
        await BuffSkinLog.bulk_create(log_list)
    if case_name not in CaseManager.CURRENT_CASES:
        CaseManager.CURRENT_CASES.append(case_name)  # type: ignore
    return f"更新武器箱: [{case_name}] 成功, 共更新 {len(update_list)} 个皮肤, 新创建 {len(create_list)} 个皮肤!"


async def search_skin_page(
    case_name: str, page_index: int
) -> Tuple[Union[List[BuffSkin], str], int]:
    """查询箱子皮肤

    Args:
        case_name (str): 箱子名称
        page_index (int): 页数

    Returns:
        Union[List[BuffSkin], str]: BuffSkin
    """
    logger.debug(
        f"尝试访问武器箱: [<u><e>{case_name}</e></u>] 页数: [<u><y>{page_index}</y></u>]", "开箱更新"
    )
    cookie = {"session": Config.get_config("open_cases", "COOKIE")}
    params = {
        "game": "csgo",
        "page_num": page_index,
        "page_size": 80,
        "itemset": CASE2ID[case_name],
        "_": time.time(),
        "use_suggestio": 0,
    }
    proxy = None
    if ip := Config.get_config("open_cases", "BUFF_PROXY"):
        proxy = {"http://": ip, "https://": ip}
    response = await AsyncHttpx.get(
        URL,
        proxy=proxy,
        params=params,
        cookies=cookie,  # type: ignore
    )
    json_data = response.json()
    update_data = []
    if json_data["code"] == "OK":
        data_list = json_data["data"]["items"]
        for data in data_list:
            obj = {"case_name": case_name}
            name = data["name"]
            logger.debug(
                f"武器箱: [<u><e>{case_name}</e></u>] 页数: [<u><y>{page_index}</y></u>] 正在收录皮肤: [<u><c>{name}</c></u>]...",
                "开箱更新",
            )
            obj["buy_max_price"] = data["buy_max_price"]  # 求购最大金额
            obj["buy_num"] = data["buy_num"]  # 当前求购
            goods_info = data["goods_info"]
            info = goods_info["info"]
            tags = info["tags"]
            obj["weapon_type"] = tags["type"]["localized_name"]  # 枪械类型
            if obj["weapon_type"] in ["音乐盒", "印花", "武器箱"]:
                continue
            if obj["weapon_type"] in ["匕首", "手套"]:
                obj["color"] = "KNIFE"
                obj["name"] = data["short_name"].split("（")[0].strip()  # 名称
            else:
                obj["color"] = NAME2COLOR[tags["rarity"]["localized_name"]]
                obj["name"] = tags["weapon"]["localized_name"]  # 名称
            obj["skin_name"] = data["short_name"].split("|")[-1].strip()  # 皮肤名称
            obj["img_url"] = goods_info["original_icon_url"]  # 图片url
            obj["steam_price"] = goods_info["steam_price_cny"]  # steam价格
            obj["abrasion"] = tags["exterior"]["localized_name"]  # 磨损
            obj["color"] = NAME2COLOR[tags["rarity"]["localized_name"]]  # 品质颜色
            obj["is_stattrak"] = "StatTrak" in tags["quality"]["localized_name"]  # type: ignore # 是否暗金
            obj["sell_min_price"] = data["sell_min_price"]  # 售卖最低价格
            obj["sell_num"] = data["sell_num"]  # 售卖数量
            obj["sell_reference_price"] = data["sell_reference_price"]  # 参考价格
            update_data.append(BuffSkin(**obj))
        logger.debug(
            f"访问武器箱: [<u><e>{case_name}</e></u>] 页数: [<u><y>{page_index}</y></u>] 成功并收录完成",
            "开箱更新",
        )
        return update_data, json_data["data"]["total_page"]
    else:
        logger.warning(f'访问BUFF失败: {json_data["msg"]}')
    return f'访问失败: {json_data["msg"]}', -1


async def reset_count_daily():
    """
    重置每日开箱
    """
    try:
        await OpenCasesUser.all().update(today_open_total=0)
        await broadcast_group(
            "[[_task|open_case_reset_remind]]今日开箱次数重置成功", log_cmd="开箱重置提醒"
        )
    except Exception as e:
        logger.error(f"开箱重置错误", e=e)


@driver.on_startup
async def _():
    await CaseManager.reload()


@driver.on_startup
async def _():
    """
    将旧表数据移动到新表
    """
    # if not await BuffSkin.first() and await BuffPrice.first():
    #     logger.debug("开始移动旧表数据 BuffPrice -> BuffSkin")
    #     id2name = {1: "狂牙大行动", 2: "突围大行动", 3: "命悬一线", 4: "裂空", 5: "光谱"}
    #     data_list: List[BuffSkin] = []
    #     for data in await BuffPrice.all():
    #         logger.debug(f"移动旧表数据: {data.skin_name}")
    #         case_name = id2name[data.case_id]
    #         name = data.skin_name
    #         is_stattrak = "StatTrak" in name
    #         name = name.replace("（★ StatTrak™）", "").replace("（StatTrak™）", "").strip()
    #         name, skin_name = name.split("|")
    #         abrasion = "无涂装"
    #         if "(" in skin_name:
    #             skin_name, abrasion = skin_name.split("(")
    #             if abrasion.endswith(")"):
    #                 abrasion = abrasion[:-1]
    #         color = get_color(case_name, name.strip(), skin_name.strip())
    #         if not color:
    #             search_list = [
    #                 x
    #                 for x in data_list
    #                 if x.skin_name == skin_name.strip() and x.name == name.strip()
    #             ]
    #             if search_list:
    #                 color = get_color(
    #                     case_name, search_list[0].name, search_list[0].skin_name
    #                 )
    #             if not color:
    #                 logger.debug(
    #                     f"箱子: [{case_name}] 皮肤: [{name}|{skin_name}] 未获取到皮肤品质，跳过..."
    #                 )
    #                 continue
    #         data_list.append(
    #             BuffSkin(
    #                 case_name=case_name,
    #                 name=name.strip(),
    #                 skin_name=skin_name.strip(),
    #                 is_stattrak=is_stattrak,
    #                 abrasion=abrasion.strip(),
    #                 skin_price=data.skin_price,
    #                 color=color,
    #                 create_time=datetime.now(),
    #                 update_time=datetime.now(),
    #             )
    #         )
    #     await BuffSkin.bulk_create(data_list, batch_size=10)
    #     logger.debug("完成移动旧表数据 BuffPrice -> BuffSkin")
