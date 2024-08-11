import asyncio
import os
import random
import re
import time
from datetime import datetime, timedelta

import nonebot
from tortoise.functions import Count

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import BuildImage, BuildMat, MatType
from zhenxun.utils.utils import cn2py

from .build_image import generate_skin
from .config import (
    CASE2ID,
    CASE_BACKGROUND,
    COLOR2NAME,
    KNIFE2ID,
    NAME2COLOR,
    UpdateType,
)
from .models.buff_skin import BuffSkin
from .models.buff_skin_log import BuffSkinLog
from .models.open_cases_user import OpenCasesUser

# from zhenxun.utils.utils import broadcast_group, cn2py


URL = "https://buff.163.com/api/market/goods"

SELL_URL = "https://buff.163.com/goods"


driver = nonebot.get_driver()

BASE_PATH = IMAGE_PATH / "csgo_cases"


class CaseManager:

    CURRENT_CASES = []

    @classmethod
    async def reload(cls):
        cls.CURRENT_CASES = []
        case_list = await BuffSkin.filter(color="CASE").values_list(
            "case_name", flat=True
        )
        for case_name in (
            await BuffSkin.filter(case_name__not="未知武器箱")
            .annotate()
            .distinct()
            .values_list("case_name", flat=True)
        ):
            for name in case_name.split(","):  # type: ignore
                if name not in cls.CURRENT_CASES and name in case_list:
                    cls.CURRENT_CASES.append(name)


async def update_skin_data(name: str, is_update_case_name: bool = False) -> str:
    """更新箱子内皮肤数据

    参数:
        name (str): 箱子名称
        is_update_case_name (bool): 是否必定更新所属箱子

    返回:
        str: 回复内容
    """
    type_ = None
    if name in CASE2ID:
        type_ = UpdateType.CASE
    if name in KNIFE2ID:
        type_ = UpdateType.WEAPON_TYPE
    if not type_:
        return "未在指定武器箱或指定武器类型内"
    session = Config.get_config("open_cases", "COOKIE")
    if not session:
        return "BUFF COOKIE为空捏!"
    weapon2case = {}
    if type_ == UpdateType.WEAPON_TYPE:
        db_data = await BuffSkin.filter(name__contains=name).all()
        weapon2case = {
            item.name + item.skin_name: item.case_name
            for item in db_data
            if item.case_name != "未知武器箱"
        }
    data_list, total = await search_skin_page(name, 1, type_)
    if isinstance(data_list, str):
        return data_list
    for page in range(2, total + 1):
        rand_time = random.randint(20, 50)
        logger.debug(f"访问随机等待时间: {rand_time}", "开箱更新")
        await asyncio.sleep(rand_time)
        data_list_, total = await search_skin_page(name, page, type_)
        if isinstance(data_list_, list):
            data_list += data_list_
    create_list: list[BuffSkin] = []
    update_list: list[BuffSkin] = []
    log_list = []
    now = datetime.now()
    exists_id_list = []
    new_weapon2case = {}
    for skin in data_list:
        if skin.skin_id in exists_id_list:
            continue
        if skin.case_name:
            skin.case_name = (
                skin.case_name.replace("”", "")
                .replace("“", "")
                .replace("武器箱", "")
                .replace(" ", "")
            )
        skin.name = skin.name.replace("（★ StatTrak™）", "").replace("（★）", "")
        exists_id_list.append(skin.skin_id)
        key = skin.name + skin.skin_name
        name_ = skin.name + skin.skin_name + skin.abrasion
        skin.create_time = now
        skin.update_time = now
        if UpdateType.WEAPON_TYPE and not skin.case_name:
            if is_update_case_name:
                case_name = new_weapon2case.get(key)
            else:
                case_name = weapon2case.get(key)
            if not case_name:
                if case_list := await get_skin_case(skin.skin_id):
                    case_name = ",".join(case_list)
                    rand = random.randint(10, 20)
                    logger.debug(
                        f"获取 {skin.name} | {skin.skin_name} 皮肤所属武器箱: {case_name}, 访问随机等待时间: {rand}",
                        "开箱更新",
                    )
                    await asyncio.sleep(rand)
            if not case_name:
                case_name = "未知武器箱"
            else:
                weapon2case[key] = case_name
                new_weapon2case[key] = case_name
            if skin.case_name == "反恐精英20周年":
                skin.case_name = "CS20"
            skin.case_name = case_name
        if await BuffSkin.exists(skin_id=skin.skin_id):
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
        name_ = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
        for c_name_ in skin.case_name.split(","):
            file_path = BASE_PATH / cn2py(c_name_) / f"{cn2py(name_)}.jpg"
            if not file_path.exists():
                logger.debug(f"下载皮肤 {name} 图片: {skin.img_url}...", "开箱更新")
                await AsyncHttpx.download_file(skin.img_url, file_path)
                rand_time = random.randint(1, 10)
                await asyncio.sleep(rand_time)
                logger.debug(f"图片下载随机等待时间: {rand_time}", "开箱更新")
            else:
                logger.debug(f"皮肤 {name_} 图片已存在...", "开箱更新")
    if create_list:
        logger.debug(
            f"更新武器箱/皮肤: [<u><e>{name}</e></u>], 创建 {len(create_list)} 个皮肤!"
        )
        await BuffSkin.bulk_create(set(create_list), 10)
    if update_list:
        abrasion_list = []
        name_list = []
        skin_name_list = []
        for skin in update_list:
            if skin.abrasion not in abrasion_list:
                abrasion_list.append(skin.abrasion)
            if skin.name not in name_list:
                name_list.append(skin.name)
            if skin.skin_name not in skin_name_list:
                skin_name_list.append(skin.skin_name)
        db_data = await BuffSkin.filter(
            case_name__contains=name,
            skin_name__in=skin_name_list,
            name__in=name_list,
            abrasion__in=abrasion_list,
        ).all()
        _update_list = []
        for data in db_data:
            for skin in update_list:
                if (
                    data.name == skin.name
                    and data.skin_name == skin.skin_name
                    and data.abrasion == skin.abrasion
                ):
                    data.steam_price = skin.steam_price
                    data.buy_max_price = skin.buy_max_price
                    data.buy_num = skin.buy_num
                    data.sell_min_price = skin.sell_min_price
                    data.sell_num = skin.sell_num
                    data.sell_reference_price = skin.sell_reference_price
                    data.update_time = skin.update_time
                    _update_list.append(data)
        logger.debug(
            f"更新武器箱/皮肤: [<u><c>{name}</c></u>], 更新 {len(create_list)} 个皮肤!"
        )
        await BuffSkin.bulk_update(
            _update_list,
            [
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
        logger.debug(
            f"更新武器箱/皮肤: [<u><e>{name}</e></u>], 新增 {len(log_list)} 条皮肤日志!"
        )
        await BuffSkinLog.bulk_create(log_list)
    if name not in CaseManager.CURRENT_CASES:
        CaseManager.CURRENT_CASES.append(name)  # type: ignore
    return f"更新武器箱/皮肤: [{name}] 成功, 共更新 {len(update_list)} 个皮肤, 新创建 {len(create_list)} 个皮肤!"


async def search_skin_page(
    s_name: str, page_index: int, type_: UpdateType
) -> tuple[list[BuffSkin] | str, int]:
    """查询箱子皮肤

    参数:
        s_name (str): 箱子/皮肤名称
        page_index (int): 页数

    返回:
        tuple[list[BuffSkin] | str, int]: BuffSkin
    """
    logger.debug(
        f"尝试访问武器箱/皮肤: [<u><e>{s_name}</e></u>] 页数: [<u><y>{page_index}</y></u>]",
        "开箱更新",
    )
    cookie = {"session": Config.get_config("open_cases", "COOKIE")}
    params = {
        "game": "csgo",
        "page_num": page_index,
        "page_size": 80,
        "_": time.time(),
        "use_suggestio": 0,
    }
    if type_ == UpdateType.CASE:
        params["itemset"] = CASE2ID[s_name]
    elif type_ == UpdateType.WEAPON_TYPE:
        params["category"] = KNIFE2ID[s_name]
    proxy = None
    if ip := Config.get_config("open_cases", "BUFF_PROXY"):
        proxy = {"http://": ip, "https://": ip}
    response = None
    error = ""
    for i in range(3):
        try:
            response = await AsyncHttpx.get(
                URL,
                proxy=proxy,
                params=params,
                cookies=cookie,  # type: ignore
            )
            if response.status_code == 200:
                break
            rand = random.randint(3, 7)
            logger.debug(
                f"尝试访问武器箱/皮肤第 {i+1} 次访问异常, code: {response.status_code}",
                "开箱更新",
            )
            await asyncio.sleep(rand)
        except Exception as e:
            logger.debug(
                f"尝试访问武器箱/皮肤第 {i+1} 次访问发生错误 {type(e)}: {e}", "开箱更新"
            )
            error = f"{type(e)}: {e}"
    if not response:
        return f"访问发生异常: {error}", -1
    if response.status_code == 200:
        # logger.debug(f"访问BUFF API: {response.text}", "开箱更新")
        json_data = response.json()
        update_data = []
        if json_data["code"] == "OK":
            data_list = json_data["data"]["items"]
            for data in data_list:
                obj = {}
                if type_ == UpdateType.CASE:
                    obj["case_name"] = s_name
                name = data["name"]
                try:
                    logger.debug(
                        f"武器箱: [<u><e>{s_name}</e></u>] 页数: [<u><y>{page_index}</y></u>] 正在收录皮肤: [<u><c>{name}</c></u>]...",
                        "开箱更新",
                    )
                    obj["skin_id"] = str(data["id"])
                    obj["buy_max_price"] = data["buy_max_price"]  # 求购最大金额
                    obj["buy_num"] = data["buy_num"]  # 当前求购
                    goods_info = data["goods_info"]
                    info = goods_info["info"]
                    tags = info["tags"]
                    obj["weapon_type"] = tags["type"]["localized_name"]  # 枪械类型
                    if obj["weapon_type"] in ["音乐盒", "印花", "探员"]:
                        continue
                    elif obj["weapon_type"] in ["匕首", "手套"]:
                        obj["color"] = "KNIFE"
                        obj["name"] = data["short_name"].split("（")[0].strip()  # 名称
                    elif obj["weapon_type"] in ["武器箱"]:
                        obj["color"] = "CASE"
                        obj["name"] = data["short_name"]
                    else:
                        obj["color"] = NAME2COLOR[tags["rarity"]["localized_name"]]
                        obj["name"] = tags["weapon"]["localized_name"]  # 名称
                    if obj["weapon_type"] not in ["武器箱"]:
                        obj["abrasion"] = tags["exterior"]["localized_name"]  # 磨损
                        obj["is_stattrak"] = "StatTrak" in tags["quality"]["localized_name"]  # type: ignore # 是否暗金
                        if not obj["color"]:
                            obj["color"] = NAME2COLOR[
                                tags["rarity"]["localized_name"]
                            ]  # 品质颜色
                    else:
                        obj["abrasion"] = "CASE"
                    obj["skin_name"] = (
                        data["short_name"].split("|")[-1].strip()
                    )  # 皮肤名称
                    obj["img_url"] = goods_info["original_icon_url"]  # 图片url
                    obj["steam_price"] = goods_info["steam_price_cny"]  # steam价格
                    obj["sell_min_price"] = data["sell_min_price"]  # 售卖最低价格
                    obj["sell_num"] = data["sell_num"]  # 售卖数量
                    obj["sell_reference_price"] = data[
                        "sell_reference_price"
                    ]  # 参考价格
                    update_data.append(BuffSkin(**obj))
                except Exception as e:
                    logger.error(
                        f"更新武器箱: [<u><e>{s_name}</e></u>] 皮肤: [<u><c>{s_name}</c></u>] 错误",
                        e=e,
                    )
            logger.debug(
                f"访问武器箱: [<u><e>{s_name}</e></u>] 页数: [<u><y>{page_index}</y></u>] 成功并收录完成",
                "开箱更新",
            )
            return update_data, json_data["data"]["total_page"]
        else:
            logger.warning(f'访问BUFF失败: {json_data["error"]}')
        return f'访问失败: {json_data["error"]}', -1
    return f"访问失败, 状态码: {response.status_code}", -1


async def build_case_image(case_name: str | None) -> BuildImage | str:
    """构造武器箱图片

    参数:
        case_name (str): 名称

    返回:
        BuildImage | str: 图片
    """
    background = random.choice(os.listdir(CASE_BACKGROUND))
    background_img = BuildImage(0, 0, background=CASE_BACKGROUND / background)
    if case_name:
        log_list = (
            await BuffSkinLog.filter(case_name__contains=case_name)
            .annotate(count=Count("id"))
            .group_by("skin_name")
            .values_list("skin_name", "count")
        )
        skin_list_ = await BuffSkin.filter(case_name__contains=case_name).all()
        skin2count = {item[0]: item[1] for item in log_list}
        case = None
        skin_list: list[BuffSkin] = []
        exists_name = []
        for skin in skin_list_:
            if skin.color == "CASE":
                case = skin
            else:
                name = skin.name + skin.skin_name
                if name not in exists_name:
                    skin_list.append(skin)
                    exists_name.append(name)
        generate_img = {}
        for skin in skin_list:
            skin_img = await generate_skin(skin, skin2count.get(skin.skin_name, 0))
            if skin_img:
                if not generate_img.get(skin.color):
                    generate_img[skin.color] = []
                generate_img[skin.color].append(skin_img)
        skin_image_list = []
        for color in COLOR2NAME:
            if generate_img.get(color):
                skin_image_list = skin_image_list + generate_img[color]
        img = skin_image_list[0]
        img_w, img_h = img.size
        total_size = (img_w + 25) * (img_h + 10) * len(skin_image_list)  # 总面积
        new_size = get_bk_image_size(total_size, background_img.size, img.size, 250)
        A = BuildImage(
            new_size[0] + 50, new_size[1], background=CASE_BACKGROUND / background
        )
        await A.filter("GaussianBlur", 2)
        if case:
            case_img = await generate_skin(
                case, skin2count.get(f"{case_name}武器箱", 0)
            )
            if case_img:
                await A.paste(case_img, (25, 25))
        w = 25
        h = 230
        skin_image_list.reverse()
        for image in skin_image_list:
            await A.paste(image, (w, h))
            w += image.width + 20
            if w + image.width - 25 > A.width:
                h += image.height + 10
                w = 25
        if h + img_h + 100 < A.height:
            await A.crop((0, 0, A.width, h + img_h + 100))
        return A
    else:
        log_list = (
            await BuffSkinLog.filter(color="CASE")
            .annotate(count=Count("id"))
            .group_by("case_name")
            .values_list("case_name", "count")
        )
        name2count = {item[0]: item[1] for item in log_list}
        skin_list = await BuffSkin.filter(color="CASE").all()
        image_list: list[BuildImage] = []
        for skin in skin_list:
            if img := await generate_skin(skin, name2count[skin.case_name]):
                image_list.append(img)
        if not image_list:
            return "未收录武器箱"
        w = 25
        h = 150
        img = image_list[0]
        img_w, img_h = img.size
        total_size = (img_w + 25) * (img_h + 10) * len(image_list)  # 总面积

        new_size = get_bk_image_size(total_size, background_img.size, img.size, 155)
        A = BuildImage(
            new_size[0] + 50, new_size[1], background=CASE_BACKGROUND / background
        )
        await A.filter("GaussianBlur", 2)
        bk_img = BuildImage(
            img_w, 120, color=(25, 25, 25, 100), font_size=60, font="CJGaoDeGuo.otf"
        )
        await bk_img.text(
            (0, 0),
            f"已收录 {len(image_list)} 个武器箱",
            (255, 255, 255),
            center_type="center",
        )
        await A.paste(bk_img, (10, 10), "width")
        for image in image_list:
            await A.paste(image, (w, h))
            w += image.width + 20
            if w + image.width - 25 > A.width:
                h += image.height + 10
                w = 25
        if h + img_h + 100 < A.height:
            await A.crop((0, 0, A.width, h + img_h + 100))
        return A


def get_bk_image_size(
    total_size: int,
    base_size: tuple[int, int],
    img_size: tuple[int, int],
    extra_height: int = 0,
) -> tuple[int, int]:
    """获取所需背景大小且不改变图片长宽比

    参数:
        total_size (int): 总面积
        base_size (Tuple[int, int]): 初始背景大小
        img_size (Tuple[int, int]): 贴图大小

    返回:
        tuple[int, int]: 满足所有贴图大小
    """
    bk_w, bk_h = base_size
    img_w, img_h = img_size
    is_add_title_size = False
    left_dis = 0
    right_dis = 0
    old_size = (0, 0)
    new_size = (0, 0)
    ratio = 1.1
    while 1:
        w_ = int(ratio * bk_w)
        h_ = int(ratio * bk_h)
        size = w_ * h_
        if size < total_size:
            left_dis = size
        else:
            right_dis = size
        r = w_ / (img_w + 25)
        if right_dis and r - int(r) < 0.1:
            if not is_add_title_size and extra_height:
                total_size = int(total_size + w_ * extra_height)
                is_add_title_size = True
                right_dis = 0
                continue
            if total_size - left_dis > right_dis - total_size:
                new_size = (w_, h_)
            else:
                new_size = old_size
            break
        old_size = (w_, h_)
        ratio += 0.1
    return new_size


async def get_skin_case(id_: str) -> list[str] | None:
    """获取皮肤所在箱子

    参数:
        id_ (str): 皮肤id

    返回:
        list[str] | None: 武器箱名称
    """
    url = f"{SELL_URL}/{id_}"
    proxy = None
    if ip := Config.get_config("open_cases", "BUFF_PROXY"):
        proxy = {"http://": ip, "https://": ip}
    response = await AsyncHttpx.get(
        url,
        proxy=proxy,
    )
    if response.status_code == 200:
        text = response.text
        if r := re.search('<meta name="description"(.*?)>', text):
            case_list = []
            for s in r.group(1).split(","):
                if "武器箱" in s:
                    case_list.append(
                        s.replace("”", "")
                        .replace("“", "")
                        .replace('"', "")
                        .replace("'", "")
                        .replace("武器箱", "")
                        .replace(" ", "")
                    )
            return case_list
    else:
        logger.debug(f"访问皮肤所属武器箱异常 url: {url} code: {response.status_code}")
    return None


async def init_skin_trends(
    name: str, skin: str, abrasion: str, day: int = 7
) -> BuildImage | None:
    date = datetime.now() - timedelta(days=day)
    log_list = (
        await BuffSkinLog.filter(
            name__contains=name.upper(),
            skin_name=skin,
            abrasion__contains=abrasion,
            create_time__gt=date,
            is_stattrak=False,
        )
        .order_by("create_time")
        .limit(day * 5)
        .all()
    )
    if not log_list:
        return None
    date_list = []
    price_list = []
    for log in log_list:
        date = str(log.create_time.date())
        if date not in date_list:
            date_list.append(date)
            price_list.append(log.sell_min_price)
    graph = BuildMat(MatType.LINE)
    graph.data = price_list
    graph.title = f"{name}({skin})价格趋势({day})"
    graph.x_index = date_list
    return await graph.build()


async def reset_count_daily():
    """
    重置每日开箱
    """
    try:
        await OpenCasesUser.all().update(today_open_total=0)
        # await broadcast_group(
        #     "[[_task|open_case_reset_remind]]今日开箱次数重置成功",
        #     log_cmd="开箱重置提醒",
        # )
    except Exception as e:
        logger.error(f"开箱重置错误", e=e)


async def download_image(case_name: str | None = None):
    """下载皮肤图片

    参数:
        case_name: 箱子名称.
    """
    skin_list = (
        await BuffSkin.filter(case_name=case_name).all()
        if case_name
        else await BuffSkin.all()
    )
    for skin in skin_list:
        name_ = skin.name + "-" + skin.skin_name + "-" + skin.abrasion
        for c_name_ in skin.case_name.split(","):
            try:
                pass
                # file_path = BASE_PATH / cn2py(c_name_) / f"{cn2py(name_)}.jpg"
                # if not file_path.exists():
                #     logger.debug(
                #         f"下载皮肤 {c_name_}/{skin.name} 图片: {skin.img_url}...",
                #         "开箱图片更新",
                #     )
                #     await AsyncHttpx.download_file(skin.img_url, file_path)
                #     rand_time = random.randint(1, 5)
                #     await asyncio.sleep(rand_time)
                #     logger.debug(f"图片下载随机等待时间: {rand_time}", "开箱图片更新")
                # else:
                #     logger.debug(
                #         f"皮肤 {c_name_}/{skin.name} 图片已存在...", "开箱图片更新"
                #     )
            except Exception as e:
                logger.error(
                    f"下载皮肤 {c_name_}/{skin.name} 图片: {skin.img_url}",
                    "开箱图片更新",
                    e=e,
                )


@driver.on_startup
async def _():
    await CaseManager.reload()
