from asyncio.exceptions import TimeoutError
from datetime import datetime
from typing import Optional

import nonebot

from configs.config import Config
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.http_utils import AsyncHttpx
from utils.utils import broadcast_group, cn2py

from .config import *
from .models.buff_prices import BuffPrice
from .models.buff_skin import BuffSkin
from .models.open_cases_user import OpenCasesUser

url = "https://buff.163.com/api/market/goods"
# proxies = 'http://49.75.59.242:3128'

driver = nonebot.get_driver()


async def util_get_buff_price(case_name: str = "狂牙大行动") -> str:
    cookie = {"session": Config.get_config("open_cases", "COOKIE")}
    failed_list = []
    case = cn2py(case_name)
    if case_name == "狂牙大行动":
        case_id = 1
    elif case_name == "突围大行动":
        case_id = 2
    elif case_name == "命悬一线":
        case_id = 3
    elif case_name == "裂空":
        case_id = 4
    elif case_name == "光谱":
        case_id = 5
    else:
        return "未查询到武器箱"
    case = case.upper()
    CASE_KNIFE = eval(case + "_CASE_KNIFE")
    CASE_RED = eval(case + "_CASE_RED")
    CASE_PINK = eval(case + "_CASE_PINK")
    CASE_PURPLE = eval(case + "_CASE_PURPLE")
    CASE_BLUE = eval(case + "_CASE_BLUE")
    for total_list in [CASE_KNIFE, CASE_RED, CASE_PINK, CASE_PURPLE, CASE_BLUE]:
        for skin in total_list:
            if skin in [
                "蝴蝶刀 | 无涂装",
                "求生匕首 | 无涂装",
                "流浪者匕首 | 无涂装",
                "系绳匕首 | 无涂装",
                "骷髅匕首 | 无涂装",
            ]:
                skin = skin.split("|")[0].strip()
            name_list = []
            price_list = []
            parameter = {"game": "csgo", "page_num": "1", "search": skin}
            try:
                response = await AsyncHttpx.get(
                    url,
                    proxy=Config.get_config("open_cases", "BUFF_PROXY"),
                    params=parameter,
                    cookies=cookie,
                )
                if response.status_code == 200:
                    data = response.json()["data"]
                    total_page = data["total_page"]
                    data = data["items"]
                    flag = False
                    if (
                        skin.find("|") == -1
                    ):  # in ['蝴蝶刀', '求生匕首', '流浪者匕首', '系绳匕首', '骷髅匕首']:
                        for i in range(1, total_page + 1):
                            name_list = []
                            price_list = []
                            parameter = {
                                "game": "csgo",
                                "page_num": f"{i}",
                                "search": skin,
                            }
                            res = await AsyncHttpx.get(
                                url, params=parameter, cookies=cookie
                            )
                            data = res.json()["data"]["items"]
                            for j in range(len(data)):
                                if data[j]["name"] in [f"{skin}（★）"]:
                                    name = data[j]["name"]
                                    price = data[j]["sell_reference_price"]
                                    name_list.append(
                                        name.split("（")[0].strip() + " | 无涂装"
                                    )
                                    price_list.append(price)
                                    flag = True
                                    break
                            if flag:
                                break
                    else:
                        try:
                            for _ in range(total_page):
                                for i in range(len(data)):
                                    name = data[i]["name"]
                                    price = data[i]["sell_reference_price"]
                                    name_list.append(name)
                                    price_list.append(price)
                        except Exception as e:
                            failed_list.append(skin)
                            logger.warning(f"{skin}更新失败")
                else:
                    failed_list.append(skin)
                    logger.warning(f"{skin}更新失败")
            except Exception:
                failed_list.append(skin)
                logger.warning(f"{skin}更新失败")
                continue
            for i in range(len(name_list)):
                name = name_list[i].strip()
                price = float(price_list[i])
                if name.find("（★）") != -1:
                    name = name[: name.find("（")] + name[name.find("）") + 1 :]
                if name.find("消音") != -1 and name.find("（S") != -1:
                    name = name.split("（")[0][:-4] + "（" + name.split("（")[1]
                    name = (
                        name.split("|")[0].strip() + " | " + name.split("|")[1].strip()
                    )
                elif name.find("消音") != -1:
                    name = (
                        name.split("|")[0][:-5].strip()
                        + " | "
                        + name.split("|")[1].strip()
                    )
                if name.find(" 18 ") != -1 and name.find("（S") != -1:
                    name = name.split("（")[0][:-5] + "（" + name.split("（")[1]
                    name = (
                        name.split("|")[0].strip() + " | " + name.split("|")[1].strip()
                    )
                elif name.find(" 18 ") != -1:
                    name = (
                        name.split("|")[0][:-6].strip()
                        + " | "
                        + name.split("|")[1].strip()
                    )
                if dbskin := await BuffPrice.get_or_none(skin_name=name):
                    if dbskin.update_date.date() == datetime.now().date():
                        continue
                    dbskin.case_id = case_id
                    dbskin.skin_price = price
                    dbskin.update_date = datetime.now()
                    await dbskin.save(
                        update_fields=["case_id", "skin_price", "update_date"]
                    )
                    logger.info(f"{name_list[i]}---------->成功更新")
    result = None
    if failed_list:
        result = ""
        for fail_skin in failed_list:
            result += fail_skin + "\n"
    return result[:-1] if result else "更新价格成功"


async def util_get_buff_img(case_name: str = "狂牙大行动") -> str:
    cookie = {"session": Config.get_config("open_cases", "COOKIE")}
    error_list = []
    case = cn2py(case_name)
    path = IMAGE_PATH / "cases/" / case
    path.mkdir(exist_ok=True, parents=True)
    case = case.upper()
    CASE_KNIFE = eval(case + "_CASE_KNIFE")
    CASE_RED = eval(case + "_CASE_RED")
    CASE_PINK = eval(case + "_CASE_PINK")
    CASE_PURPLE = eval(case + "_CASE_PURPLE")
    CASE_BLUE = eval(case + "_CASE_BLUE")
    for total_list in [CASE_KNIFE, CASE_RED, CASE_PINK, CASE_PURPLE, CASE_BLUE]:
        for skin in total_list:
            parameter = {"game": "csgo", "page_num": "1", "search": skin}
            if skin in [
                "蝴蝶刀 | 无涂装",
                "求生匕首 | 无涂装",
                "流浪者匕首 | 无涂装",
                "系绳匕首 | 无涂装",
                "骷髅匕首 | 无涂装",
            ]:
                skin = skin.split("|")[0].strip()
            logger.info(f"开始更新----->{skin}")
            skin_name = ""
            # try:
            response = await AsyncHttpx.get(
                url,
                proxy=Config.get_config("open_cases", "BUFF_PROXY"),
                params=parameter,
            )
            if response.status_code == 200:
                data = response.json()["data"]
                total_page = data["total_page"]
                flag = False
                if skin.find("|") == -1:  # in ['蝴蝶刀', '求生匕首', '流浪者匕首', '系绳匕首', '骷髅匕首']:
                    for i in range(1, total_page + 1):
                        res = await AsyncHttpx.get(url, params=parameter)
                        data = res.json()["data"]["items"]
                        for j in range(len(data)):
                            if data[j]["name"] in [f"{skin}（★）"]:
                                img_url = data[j]["goods_info"]["icon_url"]
                                skin_name = cn2py(skin + "无涂装")
                                await AsyncHttpx.download_file(
                                    img_url, path / f"{skin_name}.png"
                                )
                                flag = True
                                break
                        if flag:
                            break
                else:
                    img_url = (await response.json())["data"]["items"][0]["goods_info"][
                        "icon_url"
                    ]
                    skin_name += cn2py(skin.replace("|", "-").strip())
                    if await AsyncHttpx.download_file(
                        img_url, path / f"{skin_name}.png"
                    ):
                        logger.info(f"------->写入 {skin} 成功")
                    else:
                        logger.info(f"------->写入 {skin} 失败")
    result = None
    if error_list:
        result = ""
        for err_skin in error_list:
            result += err_skin + "\n"
    return result[:-1] if result else "更新图片成功"


async def get_price(d_name):
    cookie = {"session": Config.get_config("open_cases", "COOKIE")}
    name_list = []
    price_list = []
    parameter = {"game": "csgo", "page_num": "1", "search": d_name}
    try:
        response = await AsyncHttpx.get(url, cookies=cookie, params=parameter)
        if response.status_code == 200:
            try:
                data = response.json()["data"]
                total_page = data["total_page"]
                data = data["items"]
                for _ in range(total_page):
                    for i in range(len(data)):
                        name = data[i]["name"]
                        price = data[i]["sell_reference_price"]
                        name_list.append(name)
                        price_list.append(price)
            except Exception as e:
                return "没有查询到...", 998
        else:
            return "访问失败！", response.status_code
    except TimeoutError as e:
        return "访问超时! 请重试或稍后再试!", 997
    result = f"皮肤: {d_name}({len(name_list)})\n"
    for i in range(len(name_list)):
        result += name_list[i] + ": " + price_list[i] + "\n"
    return result[:-1], 999


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


def get_color(case_name: str, name: str, skin_name: str) -> Optional[str]:
    case_py = cn2py(case_name).upper()
    color_map = {}
    color_map["KNIFE"] = eval(case_py + "_CASE_KNIFE")
    color_map["RED"] = eval(case_py + "_CASE_RED")
    color_map["PINK"] = eval(case_py + "_CASE_PINK")
    color_map["PURPLE"] = eval(case_py + "_CASE_PURPLE")
    color_map["BLUE"] = eval(case_py + "_CASE_BLUE")
    for key in color_map:
        for skin in color_map[key]:
            if name in skin and skin_name in skin:
                return key
    return None


@driver.on_startup
async def _():
    """
    将旧表数据移动到新表
    """
    if not await BuffSkin.first() and await BuffPrice.first():
        logger.debug("开始移动旧表数据 BuffPrice -> BuffSkin")
        id2name = {1: "狂牙大行动", 2: "突围大行动", 3: "命悬一线", 4: "裂空", 5: "光谱"}
        data_list: List[BuffSkin] = []
        for data in await BuffPrice.all():
            logger.debug(f"移动旧表数据: {data.skin_name}")
            case_name = id2name[data.case_id]
            name = data.skin_name
            is_stattrak = "StatTrak" in name
            name = name.replace("（★ StatTrak™）", "").replace("（StatTrak™）", "").strip()
            name, skin_name = name.split("|")
            abrasion = "无涂装"
            if "(" in skin_name:
                skin_name, abrasion = skin_name.split("(")
                if abrasion.endswith(")"):
                    abrasion = abrasion[:-1]
            color = get_color(case_name, name.strip(), skin_name.strip())
            if not color:
                search_list = [
                    x
                    for x in data_list
                    if x.skin_name == skin_name.strip() and x.name == name.strip()
                ]
                if search_list:
                    color = get_color(
                        case_name, search_list[0].name, search_list[0].skin_name
                    )
                if not color:
                    logger.debug(
                        f"箱子: [{case_name}] 皮肤: [{name}|{skin_name}] 未获取到皮肤品质，跳过..."
                    )
                    continue
            data_list.append(
                BuffSkin(
                    case_name=case_name,
                    name=name.strip(),
                    skin_name=skin_name.strip(),
                    is_stattrak=is_stattrak,
                    abrasion=abrasion.strip(),
                    skin_price=data.skin_price,
                    color=color,
                    create_time=datetime.now(),
                    update_time=datetime.now(),
                )
            )
        await BuffSkin.bulk_create(data_list, batch_size=10)
        logger.debug("完成移动旧表数据 BuffPrice -> BuffSkin")


# 蝴蝶刀（★） | 噩梦之夜 (久经沙场)
if __name__ == "__main__":
    print(util_get_buff_img("xxxx/"))
