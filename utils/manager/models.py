from typing import List, Optional, Dict, Literal, Tuple, Union
from pydantic import BaseModel
from configs.config import Config


class AdminSetting(BaseModel):
    """
    管理员设置
    """

    level: int
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

    status: bool  # 限制状态
    check_type: Literal["private", "group", "all"]  # 检查类型
    limit_type: Literal["user", "group"]  # 监听对象
    rst: Optional[str]  # 阻断时回复


class PluginCd(BaseModel):
    """
    插件阻断
    """

    cd: int  # cd
    status: bool  # 限制状态
    check_type: Literal["private", "group", "all"]  # 检查类型
    limit_type: Literal["user", "group"]  # 监听对象
    rst: Optional[str]  # 阻断时回复


class PluginCount(BaseModel):
    """
    插件阻断
    """

    max_count: int  # 次数
    status: bool  # 限制状态
    limit_type: Literal["user", "group"]  # 监听对象
    rst: Optional[str]  # 阻断时回复


class PluginSetting(BaseModel):
    """
    插件设置
    """

    cmd: Optional[List[str]] = []  # 命令 或 命令别名
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
