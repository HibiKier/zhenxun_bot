from configs.path_config import TEXT_PATH
from typing import List, Union
from utils.http_utils import AsyncHttpx
from utils.image_utils import text2image
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import MessageSegment
import ujson as json

china_city = TEXT_PATH / "china_city.json"

data = {}


url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


async def get_yiqing_data(area: str) -> Union[str, MessageSegment]:
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
        try:
            data_ = [
                x
                for x in epidemic_data["areaTree"][0]["children"]
                if x["name"] == province
            ][0]
            if city:
                data_ = [x for x in data_["children"] if x["name"] == city][0]
        except IndexError:
            return "未查询到..."
    confirm = data_["total"]["confirm"]  # 累计确诊
    heal = data_["total"]["heal"]  # 累计治愈
    dead = data_["total"]["dead"]  # 累计死亡
    now_confirm = data_["total"]["nowConfirm"]  # 目前确诊
    add_confirm = data_["today"]["confirm"]  # 新增确诊
    grade = ""
    _grade_color = ""
    if data_["total"].get("grade"):
        grade = data_["total"]["grade"]
        if "中风险" in grade:
            _grade_color = "#fa9424"
        else:
            _grade_color = "red"

    dead_rate = f"{dead / confirm * 100:.2f}"  # 死亡率
    heal_rate = f"{heal / confirm * 100:.2f}"  # 治愈率

    x = f"{city}市" if city else f"{province}{province_type}"
    return image(b64=(await text2image(
            f"""
    {x} 疫情数据 {f"(<f font_color={_grade_color}>{grade}</f>)" if grade else ""}：
    目前确诊：
      确诊人数：<f font_color=red>{now_confirm}(+{add_confirm})</f>
    -----------------       
    累计数据：
      确诊人数：<f font_color=red>{confirm}</f>
      治愈人数：<f font_color=#39de4b>{heal}</f>
      死亡人数：<f font_color=#191d19>{dead}</f>
    治愈率：{heal_rate}%
    死亡率：{dead_rate}%
    更新日期：{last_update_time}   
        """, font_size=30, color="#f9f6f2"
            )).pic2bs4())


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
