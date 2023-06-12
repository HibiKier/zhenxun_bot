from typing import Any, List

from pydantic import BaseModel


class UpdatePlugin(BaseModel):
    """
    插件修改参数
    """

    module: str
    """模块"""
    default_status: bool
    """默认开关"""
    limit_superuser: bool
    """限制超级用户"""
    cost_gold: int
    """金币花费"""
    cmd: List[str]
    """插件别名"""
    menu_type: str
    """插件菜单类型"""
    group_level: int
    """插件所需群权限"""
    block_type: str
    """禁用类型"""


class UpdateConfig(BaseModel):
    """
    配置项修改参数
    """

    module: str
    """模块"""
    key: str
    """配置项key"""
    value: Any
    """配置项值"""


class UpdateGroup(BaseModel):

    group_id: str
    """群号"""
    status: bool
    """状态"""
    level: int
    """群权限"""


class HandleRequest(BaseModel):
    """
    操作请求接收数据
    """

    id: int
    handle: str
    type: str
