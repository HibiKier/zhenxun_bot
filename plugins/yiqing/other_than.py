# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 23:04
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : other_than.py
# @Software: PyCharm
from utils.http_utils import AsyncHttpx
from typing import Optional
from services.log import logger
import re
import json

__doc__ = """爬虫实现国外疫情数据（找不到好接口）"""


def intcomma(value) -> str:
    """
    数字格式化
    """
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r"\g<1>,\g<2>", orig)
    return new if orig == new else intcomma(new)


async def get_other_data(place: str) -> Optional[str]:
    """
    :param place: 地名
    :return: 格式化字符串
    """
    try:
        html = (
            (await AsyncHttpx.get("https://news.ifeng.com/c/special/7uLj4F83Cqm"))
            .text.replace("\n", "")
            .replace(" ", "")
        )
    except Exception as e:
        logger.error(f"疫情查询发生错误 {type(e)}：{e}")
        return None
    find_data = re.compile(r"varallData=(.*?);</script>")
    sum_ = re.findall(find_data, html)[0]
    try:
        sum_ = json.loads(sum_)
        other_country = sum_["yiqing_v2"]["dataList"][29]["child"]
        for country in other_country:
            if place == country["name2"]:
                return (
                    f"{place} 疫情数据：\n"
                    "——————————————\n"
                    f"新增病例：{intcomma(country['quezhen_add'])}\n"
                    f"现有确诊：{intcomma(country['quezhen_xianyou'])}\n"
                    f"累计确诊：{intcomma(country['quezhen'])}\n"
                    f"累计治愈：{intcomma(country['zhiyu'])}\n"
                    f"死亡：{intcomma(country['siwang'])}\n"
                    "——————————————"
                    # f"更新时间：{country['sys_publishDateTime']}"
                    # 时间无法精确到分钟，网页用了js我暂时找不到
                )
            else:
                for city in country["child"]:
                    if place == city["name3"]:
                        return (
                            f"{place} 疫情数据：\n"
                            "——————————————\n"
                            f"新增病例：{intcomma(city['quezhen_add'])}\n"
                            f"累计确诊：{intcomma(city['quezhen'])}\n"
                            f"累计治愈：{intcomma(city['zhiyu'])}\n"
                            f"死亡：{intcomma(city['siwang'])}\n"
                            "——————————————"
                        )
    except Exception as e:
        logger.error(f"疫情查询发生错误 {type(e)}：{e}")
    return None
