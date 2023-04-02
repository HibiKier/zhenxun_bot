from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import nonebot
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = nonebot.get_app()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestResult(BaseModel):
    """
    好友/群组请求管理
    """

    oid: str
    id: int
    flag: str
    nickname: Optional[str]
    level: Optional[int]
    sex: Optional[str]
    age: Optional[int]
    from_: Optional[str]
    comment: Optional[str]
    invite_group: Optional[int]
    group_name: Optional[str]


class RequestParma(BaseModel):
    """
    操作请求接收数据
    """

    id: int
    handle: str
    type: str


class SystemStatus(BaseModel):
    """
    系统状态
    """

    cpu: int
    memory: int
    disk: int
    check_time: datetime


class SystemNetwork(BaseModel):
    """
    系统网络状态
    """

    baidu: int
    google: int


class SystemFolderSize(BaseModel):
    """
    资源文件占比
    """

    font_dir_size: float
    image_dir_size: float
    text_dir_size: float
    record_dir_size: float
    temp_dir_size: float
    data_dir_size: float
    log_dir_size: float
    check_time: datetime


class SystemStatusList(BaseModel):
    """
    状态记录
    """

    cpu_data: List[Dict[str, Union[float, str]]]
    memory_data: List[Dict[str, Union[float, str]]]
    disk_data: List[Dict[str, Union[float, str]]]


class SystemResult(BaseModel):
    """
    系统api返回
    """

    status: SystemStatus
    network: SystemNetwork
    disk: SystemFolderSize
    check_time: datetime
