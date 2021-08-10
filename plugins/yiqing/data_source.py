from utils.user_agent import get_user_agent
from configs.path_config import TXT_PATH
from typing import List
from pathlib import Path
import ujson as json
import aiohttp

china_city = Path(TXT_PATH) / "china_city.json"

try:
    with open(china_city, "r", encoding="utf8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}


url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


async def get_yiqing_data(area: str):
    global data
    province = None
    city = None
    province_type = "省"
    if area == '中国':
        province = area
        province_type = ""
    elif area[-1] != '省':
        for p in data.keys():
            if area in data[p]:
                province = p
                city = area
    elif area in data.keys() or area[:-1] in data.keys():
        province = area if area[-1] != '省' else area[:-1]
        if len(data[province]) == 1:
            province_type = "市"
        city = ""
    if not province and not city:
        return "小真寻只支持国内的疫情查询喔..."
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        async with session.get(url, timeout=7) as response:
            epidemic_data = json.loads((await response.json())["data"])
            last_update_time = epidemic_data["lastUpdateTime"]
            if area == "中国":
                data_ = epidemic_data["areaTree"][0]
            else:
                data_ = [
                    x
                    for x in epidemic_data["areaTree"][0]["children"]
                    if x["name"] == province
                ][0]
                if city:
                    try:
                        data_ = [x for x in data_["children"] if x["name"] == city][0]
                    except IndexError:
                        return '未查询到...'
            confirm = data_["total"]["confirm"]  # 累计确诊
            heal = data_["total"]["heal"]  # 累计治愈
            dead = data_["total"]["dead"]  # 累计死亡
            dead_rate = data_["total"]["deadRate"]  # 死亡率
            heal_rate = data_["total"]["healRate"]  # 治愈率
            now_confirm = data_["total"]["nowConfirm"]  # 目前确诊
            suspect = data_["total"]["suspect"]  # 疑似
            add_confirm = data_["today"]["confirm"]  # 新增确诊
    x = f"{city}市" if city else f'{province}{province_type}'
    return (
        f"{x} 疫情数据：\n"
        f"\t目前确诊：\n"
        f"\t\t确诊人数：{now_confirm}(+{add_confirm})\n"
        f"\t\t疑似人数：{suspect}\n"
        f"==================\n"
        f"\t累计数据：\n"
        f"\t\t确诊人数：{confirm}\n"
        f"\t\t治愈人数：{heal}\n"
        f"\t\t死亡人数：{dead}\n"
        f"\t治愈率：{heal_rate}%\n"
        f"\t死亡率：{dead_rate}%\n"
        f"更新日期：{last_update_time}"
    )


def get_city_list() -> List[str]:
    global data
    city_list = []
    for p in data.keys():
        for c in data[p]:
            city_list.append(c)
    return city_list
