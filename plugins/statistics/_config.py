from enum import Enum
from typing import NamedTuple


class SearchType(Enum):

    """
    查询类型
    """

    DAY = "day_statistics"
    """天"""
    WEEK = "week_statistics"
    """周"""
    MONTH = "month_statistics"
    """月"""
    TOTAL = "total_statistics"
    """总数"""


class ParseData(NamedTuple):
    
    global_search: bool
    """是否全局搜索"""
    search_type: SearchType
    """搜索类型"""
