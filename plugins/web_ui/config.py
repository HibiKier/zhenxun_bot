from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import nonebot
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strenum import StrEnum

app = nonebot.get_app()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


AVA_URL = "http://q1.qlogo.cn/g?b=qq&nk={}&s=160"

GROUP_AVA_URL = "http://p.qlogo.cn/gh/{}/{}/640/"


class QueryDateType(StrEnum):

    """
    查询日期类型
    """

    DAY = "day"
    """日"""
    WEEK = "week"
    """周"""
    MONTH = "month"
    """月"""
    YEAR = "year"
    """年"""


# class SystemNetwork(BaseModel):
#     """
#     系统网络状态
#     """

#     baidu: int
#     google: int


# class SystemFolderSize(BaseModel):
#     """
#     资源文件占比
#     """

#     font_dir_size: float
#     image_dir_size: float
#     text_dir_size: float
#     record_dir_size: float
#     temp_dir_size: float
#     data_dir_size: float
#     log_dir_size: float
#     check_time: datetime


# class SystemStatusList(BaseModel):
#     """
#     状态记录
#     """

#     cpu_data: List[Dict[str, Union[float, str]]]
#     memory_data: List[Dict[str, Union[float, str]]]
#     disk_data: List[Dict[str, Union[float, str]]]


# class SystemResult(BaseModel):
#     """
#     系统api返回
#     """

#     status: SystemStatus
#     network: SystemNetwork
#     disk: SystemFolderSize
#     check_time: datetime
