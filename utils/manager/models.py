from pathlib import Path
from typing import List, Optional, Dict, Literal, Tuple, Union, Any
from pydantic import BaseModel
from configs.config import Config
from enum import Enum


class AdminSetting(BaseModel):
    """
    管理员设置
    """

    level: int = 5
    cmd: Optional[List[str]]


class BaseGroup(BaseModel):
    """
    基础群聊信息
    """

    level: int = Config.get_config("group_manager", "DEFAULT_GROUP_LEVEL")  # 群等级
    status: bool = Config.get_config(
        "group_manager", "DEFAULT_GROUP_BOT_STATUS"
    )  # 总开关状态
    close_plugins: List[str] = []  # 已关闭插件
    group_task_status: Dict[str, bool] = {}  # 被动状态


class BaseData(BaseModel):
    """
    群基本信息
    """

    white_group: List[int] = []  # 白名单
    group_manager: Dict[str, BaseGroup] = {}  # 群组管理
    task: Dict[str, str] = {}  # 被动任务 【英文：中文】


class PluginBlock(BaseModel):
    """
    插件阻断
    """

    status: bool = True  # 限制状态
    check_type: Literal["private", "group", "all"] = "all"  # 检查类型
    limit_type: Literal["user", "group"] = "user"  # 监听对象
    rst: Optional[str]  # 阻断时回复


class PluginCd(BaseModel):
    """
    插件阻断
    """

    cd: int = 5  # cd
    status: bool = True  # 限制状态
    check_type: Literal["private", "group", "all"] = "all"  # 检查类型
    limit_type: Literal["user", "group"] = "user"  # 监听对象
    rst: Optional[str]  # 阻断时回复


class PluginCount(BaseModel):
    """
    插件阻断
    """

    max_count: int  # 次数
    status: bool = True  # 限制状态
    limit_type: Literal["user", "group"] = "user"  # 监听对象
    rst: Optional[str]  # 阻断时回复


class PluginSetting(BaseModel):
    """
    插件设置
    """

    cmd: List[str] = []  # 命令 或 命令别名
    default_status: bool = True  # 默认开关状态
    level: int = 5  # 功能权限等级
    limit_superuser: bool = False  # 功能状态是否限制超级用户
    plugin_type: Tuple[Union[str, int], ...] = ("normal",)  # 插件类型
    cost_gold: int = 0  # 需要消费的金币


class Plugin(BaseModel):
    """
    插件数据
    """

    plugin_name: str  # 模块名
    status: Optional[bool] = True  # 开关状态
    error: Optional[bool] = False  # 是否加载报错
    block_type: Optional[str] = None  # 关闭类型
    author: Optional[str] = None  # 作者
    version: Optional[Union[int, str]] = None  # 版本


class PluginType(Enum):
    """
    插件类型
    """

    NORMAL = "normal"
    ADMIN = "admin"
    HIDDEN = "hidden"
    SUPERUSER = "superuser"


class PluginData(BaseModel):
    model: str
    name: str
    plugin_type: PluginType  # 插件内部类型，根据name [Hidden] [Admin] [SUPERUSER]
    usage: Optional[str]
    des: Optional[str]
    task: Optional[Dict[str, str]]
    menu_type: Tuple[Union[str, int], ...] = ("normal",)  # 菜单类型
    plugin_setting: Optional[PluginSetting]
    plugin_cd: Optional[PluginCd]
    plugin_block: Optional[PluginBlock]
    plugin_count: Optional[PluginCount]
    plugin_resources: Optional[Dict[str, Union[str, Path]]]
    plugin_configs: Optional[Dict[str, Dict[str, Any]]]
    plugin_status: Plugin

    class Config:
        arbitrary_types_allowed = True

    def __eq__(self, other: "PluginData"):
        return (
            isinstance(other, PluginData)
            and self.name == other.name
            and self.menu_type == other.menu_type
        )

    def __hash__(self):
        return hash(self.name + self.menu_type[0])
