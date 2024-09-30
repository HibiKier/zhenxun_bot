import copy
from typing import Any
from pathlib import Path
from collections.abc import Callable

import cattrs
from ruamel.yaml import YAML
from pydantic import BaseModel
from ruamel.yaml.scanner import ScannerError

from zhenxun.services.log import logger
from zhenxun.configs.path_config import DATA_PATH
from zhenxun.utils.enum import BlockType, PluginType, LimitWatchType, PluginLimitType

_yaml = YAML(pure=True)
_yaml.indent = 2
_yaml.allow_unicode = True


class Example(BaseModel):
    """
    示例
    """

    exec: str
    """执行命令"""
    description: str = ""
    """命令描述"""


class Command(BaseModel):
    """
    具体参数说明
    """

    command: str
    """命令"""
    params: list[str] = []
    """参数"""
    description: str = ""
    """描述"""
    examples: list[Example] = []
    """示例列表"""


class RegisterConfig(BaseModel):
    """
    注册配置项
    """

    key: str
    """配置项键"""
    value: Any
    """配置项值"""
    module: str | None = None
    """模块名"""
    help: str | None
    """配置注解"""
    default_value: Any | None = None
    """默认值"""
    type: Any = None
    """参数类型"""
    arg_parser: Callable | None = None
    """参数解析"""


class ConfigModel(BaseModel):
    """
    配置项
    """

    value: Any
    """配置项值"""
    help: str | None
    """配置注解"""
    default_value: Any | None = None
    """默认值"""
    type: Any = None
    """参数类型"""
    arg_parser: Callable | None = None
    """参数解析"""


class ConfigGroup(BaseModel):
    """
    配置组
    """

    module: str
    """模块名"""
    name: str | None = None
    """插件名"""
    configs: dict[str, ConfigModel] = {}
    """配置项列表"""

    def get(self, c: str, default: Any = None) -> Any:
        cfg = self.configs.get(c.upper())
        if cfg is not None:
            if cfg.value is not None:
                return cfg.value
            if cfg.default_value is not None:
                return cfg.default_value
        return default


class BaseBlock(BaseModel):
    """
    插件阻断基本类（插件阻断限制）
    """

    status: bool = True
    """限制状态"""
    check_type: BlockType = BlockType.ALL
    """检查类型"""
    watch_type: LimitWatchType = LimitWatchType.USER
    """监听对象"""
    result: str | None = None
    """阻断时回复内容"""
    _type: PluginLimitType = PluginLimitType.BLOCK
    """类型"""


class PluginCdBlock(BaseBlock):
    """
    插件cd限制
    """

    cd: int = 5
    """cd"""
    _type: PluginLimitType = PluginLimitType.CD
    """类型"""


class PluginCountBlock(BaseBlock):
    """
    插件次数限制
    """

    max_count: int
    """最大调用次数"""
    _type: PluginLimitType = PluginLimitType.COUNT
    """类型"""


class PluginSetting(BaseModel):
    """
    插件基本配置
    """

    level: int = 5
    """群权限等级"""
    default_status: bool = True
    """进群默认开关状态"""
    limit_superuser: bool = False
    """是否限制超级用户"""
    cost_gold: int = 0
    """调用插件花费金币"""


class Task(BaseBlock):
    module: str
    """被动技能模块名"""
    name: str
    """被动技能名称"""
    status: bool = True
    """全局开关状态"""
    create_status: bool = False
    """初次加载默认开关状态"""
    default_status: bool = True
    """进群时默认状态"""
    run_time: str | None = None
    """运行时间"""


class PluginExtraData(BaseModel):
    """
    插件扩展信息
    """

    author: str | None = None
    """作者"""
    version: str | None = None
    """版本"""
    plugin_type: PluginType = PluginType.NORMAL
    """插件类型"""
    menu_type: str = "功能"
    """菜单类型"""
    admin_level: int | None = None
    """管理员插件所需权限等级"""
    configs: list[RegisterConfig] | None = None
    """插件配置"""
    setting: PluginSetting | None = None
    """插件基本配置"""
    limits: list[BaseBlock | PluginCdBlock | PluginCountBlock] | None = None
    """插件限制"""
    commands: list[Command] = []
    """命令列表，用于说明帮助"""
    tasks: list[Task] | None = None
    """技能被动"""
    superuser_help: str | None = None
    """超级用户帮助"""
    aliases: set[str] = set()
    """额外名称"""
    sql_list: list[str] | None = None
    """常用sql"""


class NoSuchConfig(Exception):
    pass


class ConfigsManager:
    """
    插件配置 与 资源 管理器
    """

    def __init__(self, file: Path):
        self._data: dict[str, ConfigGroup] = {}
        self._simple_data: dict = {}
        self._simple_file = DATA_PATH / "config.yaml"
        _yaml = YAML()
        if file:
            file.parent.mkdir(exist_ok=True, parents=True)
            self.file = file
            self.load_data()
        if self._simple_file.exists():
            try:
                with self._simple_file.open(encoding="utf8") as f:
                    self._simple_data = _yaml.load(f)
            except ScannerError as e:
                raise ScannerError(
                    f"{e}\n**********************************************\n"
                    f"****** 可能为config.yaml配置文件填写不规范 ******\n"
                    f"**********************************************"
                ) from e

    def set_name(self, module: str, name: str):
        """设置插件配置中文名出

        参数:
            module: 模块名
            name: 中文名称

        异常:
            ValueError: module不能为为空
        """
        if not module:
            raise ValueError("set_name: module不能为为空")
        if data := self._data.get(module):
            data.name = name

    def add_plugin_config(
        self,
        module: str,
        key: str,
        value: Any,
        *,
        help: str | None = None,
        default_value: Any = None,
        type: type | None = None,
        arg_parser: Callable | None = None,
        _override: bool = False,
    ):
        """为插件添加一个配置，不会被覆盖，只有第一个生效

        参数:
            module: 模块
            key: 键
            value: 值
            help: 配置注解.
            default_value: 默认值.
            type: 值类型.
            arg_parser: 值解析器，一般与webui配合使用.
            _override: 强制覆盖值.

        异常:
            ValueError: module和key不能为为空
            ValueError: 填写错误
        """

        if not module or not key:
            raise ValueError("add_plugin_config: module和key不能为为空")
        if module in self._data and (config := self._data[module].configs.get(key)):
            config.help = help
            config.arg_parser = arg_parser
            config.type = type
            if _override:
                config.value = value
                config.default_value = default_value
        else:
            _module = None
            if ":" in module:
                module_split = module.split(":")
                if len(module_split) < 2:
                    raise ValueError(f"module: {module} 填写错误")
                _module = module_split[-1]
                module = module_split[0]
            key = key.upper()
            if not self._data.get(module):
                self._data[module] = ConfigGroup(module=module)
            self._data[module].configs[key] = ConfigModel(
                value=value,
                help=help,
                default_value=default_value,
                type=type,
            )

    def set_config(
        self,
        module: str,
        key: str,
        value: Any,
        auto_save: bool = False,
        save_simple_data: bool = True,
    ):
        """设置配置值

        参数:
            module: 模块名
            key: 配置名称
            value: 值
            auto_save: 自动保存.
            save_simple_data: 保存至config.yaml.
        """
        if module in self._data:
            data = self._data[module].configs.get(key)
            if data and data != value:
                self._data[module].configs[key].value = value
                self._simple_data[module][key] = value
            if auto_save:
                self.save(save_simple_data=save_simple_data)

    def get_config(self, module: str, key: str, default: Any = None) -> Any:
        """获取指定配置值

        参数:
            module: 模块名
            key: 配置键
            default: 没有key值内容的默认返回值.

        异常:
            NoSuchConfig: 未查询到配置

        返回:
            Any: 配置值
        """
        logger.debug(
            f"尝试获取配置MODULE: [<u><y>{module}</y></u>] | KEY: [<u><y>{key}</y></u>]"
        )
        key = key.upper()
        value = None
        if module in self._data.keys():
            config = self._data[module].configs.get(key) or self._data[
                module
            ].configs.get(key)
            if not config:
                raise NoSuchConfig(
                    f"未查询到配置项 MODULE: [ {module} ] | KEY: [ {key} ]"
                )
            try:
                if config.arg_parser:
                    value = config.arg_parser(value or config.default_value)
                elif config.value is not None:
                    # try:
                    value = (
                        cattrs.structure(config.value, config.type)
                        if config.type
                        else config.value
                    )
                elif config.default_value is not None:
                    value = (
                        cattrs.structure(config.default_value, config.type)
                        if config.type
                        else config.default_value
                    )
            except Exception as e:
                logger.warning(
                    f"配置项类型转换 MODULE: [<u><y>{module}</y></u>]"
                    " | KEY: [<u><y>{key}</y></u>]",
                    e=e,
                )
                value = config.value or config.default_value
        if value is None:
            value = default
        logger.debug(
            f"获取配置 MODULE: [<u><y>{module}</y></u>] | "
            f" KEY: [<u><y>{key}</y></u>] -> [<u><c>{value}</c></u>]"
        )
        return value

    def get(self, key: str) -> ConfigGroup:
        """获取插件配置数据

        参数:
            key: 键，一般为模块名

        返回:
            ConfigGroup: ConfigGroup
        """
        return self._data.get(key) or ConfigGroup(module="")

    def save(self, path: str | Path | None = None, save_simple_data: bool = False):
        """保存数据

        参数:
            path: 路径.
            save_simple_data: 同时保存至config.yaml.
        """
        if save_simple_data:
            with open(self._simple_file, "w", encoding="utf8") as f:
                _yaml.dump(self._simple_data, f)
        path = path or self.file
        data = {}
        for module in self._data:
            data[module] = {}
            for config in self._data[module].configs:
                value = self._data[module].configs[config].dict()
                del value["type"]
                del value["arg_parser"]
                data[module][config] = value
        with open(path, "w", encoding="utf8") as f:
            _yaml.dump(data, f)

    def reload(self):
        """重新加载配置文件"""
        if self._simple_file.exists():
            with open(self._simple_file, encoding="utf8") as f:
                self._simple_data = _yaml.load(f)
        for key in self._simple_data.keys():
            for k in self._simple_data[key].keys():
                self._data[key].configs[k].value = self._simple_data[key][k]
        self.save()

    def load_data(self):
        """加载数据

        异常:
            ValueError: 配置文件为空！
        """
        if not self.file.exists():
            return
        with open(self.file, encoding="utf8") as f:
            temp_data = _yaml.load(f)
        if not temp_data:
            self.file.unlink()
            raise ValueError(
                "配置文件为空！\n"
                "***********************************************************\n"
                "****** 配置文件 plugins2config.yaml 为空，已删除，请重启 ******\n"
                "***********************************************************"
            )
        count = 0
        for module in temp_data:
            config_group = ConfigGroup(module=module)
            for config in temp_data[module]:
                config_group.configs[config] = ConfigModel(**temp_data[module][config])
                count += 1
            self._data[module] = config_group
        logger.info(
            f"加载配置完成，共加载 <u><y>{len(temp_data)}</y></u> 个配置组及对应"
            f" <u><y>{count}</y></u> 个配置项"
        )

    def get_data(self) -> dict[str, ConfigGroup]:
        return copy.deepcopy(self._data)

    def is_empty(self) -> bool:
        return not bool(self._data)

    def keys(self):
        return self._data.keys()

    def __str__(self):
        return str(self._data)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]
