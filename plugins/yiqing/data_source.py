from configs.path_config import TEXT_PATH
from typing import List
from pathlib import Path
from utils.http_utils import AsyncHttpx
import ujson as json

china_city = Path(TEXT_PATH) / "china_city.json"

data = {}


url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


async def get_yiqing_data(area: str):
    """
    查看疫情数据
    :param area: 省份/城市
    """
    global data
    province = None
    city = None
    province_type = "省"
    if area == "中国":
        province = area
        province_type = ""
    elif area[-1] == '省' or (area in data.keys() and area[-1] != "市"):
        province = area if area[-1] != "省" else area[:-1]
        if len(data[province]) == 1:
            province_type = "市"
        city = ""
    else:
        area = area[:-1] if area[-1] == "市" else area
        for p in data.keys():
            if area in data[p]:
                province = p
                city = area
    epidemic_data = json.loads((await AsyncHttpx.get(url)).json()["data"])
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
                return "未查询到..."
    confirm = data_["total"]["confirm"]  # 累计确诊
    heal = data_["total"]["heal"]  # 累计治愈
    dead = data_["total"]["dead"]  # 累计死亡
    dead_rate = data_["total"]["deadRate"]  # 死亡率
    heal_rate = data_["total"]["healRate"]  # 治愈率
    now_confirm = data_["total"]["nowConfirm"]  # 目前确诊
    suspect = data_["total"]["suspect"]  # 疑似
    add_confirm = data_["today"]["confirm"]  # 新增确诊
    x = f"{city}市" if city else f"{province}{province_type}"
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


def get_city_and_province_list() -> List[str]:
    """
    获取城市省份列表
    """
    global data
    if not data:
        try:
            with open(china_city, "r", encoding="utf8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
    city_list = ["中国"]
    for p in data.keys():
        for c in data[p]:
            city_list.append(c)
        city_list.append(p)
    return city_list
