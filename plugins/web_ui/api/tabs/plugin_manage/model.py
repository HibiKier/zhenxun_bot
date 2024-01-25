from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from utils.manager.models import Plugin as PluginManager
from utils.manager.models import PluginBlock, PluginCd, PluginCount, PluginSetting
from utils.typing import BLOCK_TYPE


class PluginSwitch(BaseModel):
    """
    插件开关
    """

    module: str
    """模块"""
    status: bool
    """开关状态"""


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
    menu_type: str
    """插件菜单类型"""
    level: int
    """插件所需群权限"""
    block_type: Optional[BLOCK_TYPE] = None
    """禁用类型"""
    configs: Optional[Dict[str, Any]] = None
    """配置项"""


class PluginInfo(BaseModel):
    """
    基本插件信息
    """

    module: str
    """插件名称"""
    plugin_name: str
    """插件中文名称"""
    default_status: bool
    """默认开关"""
    limit_superuser: bool
    """限制超级用户"""
    cost_gold: int
    """花费金币"""
    menu_type: str
    """插件菜单类型"""
    version: Union[int, str, float]
    """插件版本"""
    level: int
    """群权限"""
    status: bool
    """当前状态"""
    author: Optional[str] = None
    """作者"""
    block_type: BLOCK_TYPE = None
    """禁用类型"""


class PluginConfig(BaseModel):
    """
    插件配置项
    """

    module: str
    """模块"""
    key: str
    """键"""
    value: Any
    """值"""
    help: Optional[str] = None
    """帮助"""
    default_value: Any
    """默认值"""
    type: Optional[Any] = None
    """值类型"""
    type_inner: Optional[List[str]] = None
    """List Tuple等内部类型检验"""
    


class Plugin(BaseModel):
    """
    插件
    """

    module: str
    """模块名称"""
    plugin_settings: Optional[PluginSetting]
    """settings"""
    plugin_manager: Optional[PluginManager]
    """manager"""
    plugin_config: Optional[Dict[str, PluginConfig]]
    """配置项"""
    cd_limit: Optional[PluginCd]
    """cd限制"""
    block_limit: Optional[PluginBlock]
    """阻断限制"""
    count_limit: Optional[PluginCount]
    """次数限制"""

class PluginCount(BaseModel):
    """
    插件数量
    """

    normal: int = 0
    """普通插件"""
    admin: int = 0
    """管理员插件"""
    superuser: int = 0
    """超级用户插件"""
    other: int = 0
    """其他插件"""


class PluginDetail(PluginInfo):
    """
    插件详情
    """

    config_list: List[PluginConfig]