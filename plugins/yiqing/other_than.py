# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 23:04
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : other_than.py
# @Software: PyCharm
from utils.http_utils import AsyncHttpx
from nonebot.adapters.onebot.v11 import MessageSegment
from typing import Optional
from services.log import logger
from utils.image_utils import text2image
from utils.message_builder import image
from json.decoder import JSONDecodeError
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


async def get_other_data(place: str, count: int = 0) -> Optional[MessageSegment]:
    """
    :param place: 地名
    :param count: 递归次数
    :return: 格式化字符串
    """
    if count == 5:
        return None
    try:
        html = (
            (await AsyncHttpx.get("https://news.ifeng.com/c/special/7uLj4F83Cqm"))
            .text.replace("\n", "")
            .replace(" ", "")
        )
        find_data = re.compile(r"varallData=(.*?);</script>")
        sum_ = re.findall(find_data, html)[0]
        sum_ = json.loads(sum_)
    except JSONDecodeError:
        return await get_other_data(place, count + 1)
    except Exception as e:
        logger.error(f"疫情查询发生错误 {type(e)}：{e}")
        return None
    try:
        other_country = sum_["yiqing_v2"]["dataList"][29]["child"]
        for country in other_country:
            if place == country["name2"]:
                return image(
                    b64=(await text2image(
                        f"  {place} 疫情数据：\n"
                        "——————————————\n"
                        f"    新增病例：<f font_color=red>{intcomma(country['quezhen_add'])}</f>\n"
                        f"    现有确诊：<f font_color=red>{intcomma(country['quezhen_xianyou'])}</f>\n"
                        f"    累计确诊：<f font_color=red>{intcomma(country['quezhen'])}</f>\n"
                        f"    累计治愈：<f font_color=#39de4b>{intcomma(country['zhiyu'])}</f>\n"
                        f"    死亡：{intcomma(country['siwang'])}\n"
                        "——————————————"
                        # f"更新时间：{country['sys_publishDateTime']}"
                        # 时间无法精确到分钟，网页用了js我暂时找不到
                        ,
                        font_size=30,
                        color="#f9f6f2",
                        padding=15
                    )).pic2bs4()
                )
            else:
                for city in country["child"]:
                    if place == city["name3"]:
                        return image(
                            b64=(await text2image(
                                f"\n{place} 疫情数据：\n"
                                "——————————————\n"
                                f"\t新增病例：<f font_color=red>{intcomma(city['quezhen_add'])}</f>\n"
                                f"\t累计确诊：<f font_color=red>{intcomma(city['quezhen'])}</f>\n"
                                f"\t累计治愈：<f font_color=#39de4b>{intcomma(city['zhiyu'])}</f>\n"
                                f"\t死亡：{intcomma(city['siwang'])}\n"
                                "——————————————\n",
                                font_size=30,
                                color="#f9f6f2",
                                padding=15
                            )).pic2bs4()
                        )
    except Exception as e:
        logger.error(f"疫情查询发生错误 {type(e)}：{e}")
    return None
