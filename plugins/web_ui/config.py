from typing import Optional, List, Any
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nonebot


app = nonebot.get_app()

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CdLimit(BaseModel):
    cd: int
    status: bool
    check_type: str
    limit_type: str
    rst: Optional[str]


class BlockLimit(BaseModel):
    status: bool
    check_type: str
    limit_type: str
    rst: Optional[str]


class CountLimit(BaseModel):
    max_count: int
    status: bool
    limit_type: bool
    rst: Optional[str]


class PluginManager(BaseModel):
    plugin_name: str  # 插件名称
    status: Optional[bool]  # 插件状态
    error: Optional[bool]  # 加载状态
    version: Optional[float]  # 版本
    author: Optional[str]  # 作者
    block_type: Optional[str]  # 禁用类型


class PluginSettings(BaseModel):
    level: Optional[int]  # 群权限等级
    default_status: Optional[bool]  # 默认开关
    limit_superuser: Optional[bool]  # 是否限制超级用户
    cmd: Optional[str]  # cmd别名
    cost_gold: Optional[int]  # 花费金币限制
    plugin_type: Optional[str]  # 帮助类型


class Plugin(BaseModel):
    model: str  # 模块
    plugin_settings: Optional[PluginSettings]
    plugin_manager: Optional[PluginManager]
    cd_limit: Optional[CdLimit]
    block_limit: Optional[BlockLimit]
    count_limit: Optional[CountLimit]


class Group(BaseModel):
    group_id: int
    group_name: str
    member_count: int
    max_member_count: int


class Task(BaseModel):
    name: str
    nameZh: str
    status: bool


class GroupResult(BaseModel):
    group: Group
    level: int
    status: bool
    close_plugins: List[str]
    task: List[Task]


class RequestResult(BaseModel):
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
    id: int
    handle: str
    type: str


class Result(BaseModel):
    code: int
    data: Any
