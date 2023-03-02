import copy
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type, Union

import cattrs
from pydantic import BaseModel
from ruamel import yaml
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError

from services.log import logger


class Config(BaseModel):

    """
    配置项
    """

    value: Any
    """配置项值"""
    name: Optional[str]
    """插件名称"""
    help: Optional[str]
    """配置注解"""
    default_value: Optional[Any] = None
    """默认值"""
    level_module: Optional[str]
    """受权限模块"""
    type: Any = None
    """参数类型"""
    arg_parser: Optional[Callable] = None
    """参数解析"""


class ConfigGroup(BaseModel):

    """
    配置组
    """

    module: str
    """模块名"""
    configs: Dict[str, Config] = {}
    """配置项列表"""


class NoSuchConfig(Exception):
    pass


class ConfigsManager:
    """
    插件配置 与 资源 管理器
    """

    def __init__(self, file: Path):
        self._data: Dict[str, ConfigGroup] = {}
        self._simple_data: dict = {}
        self._admin_level_data = []
        self._simple_file = Path() / "configs" / "config.yaml"
        _yaml = YAML()
        if file:
            file.parent.mkdir(exist_ok=True, parents=True)
            self.file = file
            self.load_data()
        if self._simple_file.exists():
            try:
                with open(self._simple_file, "r", encoding="utf8") as f:
                    self._simple_data = _yaml.load(f)
            except ScannerError as e:
                raise ScannerError(
                    f"{e}\n**********************************************\n"
                    f"****** 可能为config.yaml配置文件填写不规范 ******\n"
                    f"**********************************************"
                )

    def add_plugin_config(
        self,
        module: str,
        key: str,
        value: Optional[Any],
        *,
        name: Optional[str] = None,
        help_: Optional[str] = None,
        default_value: Optional[Any] = None,
        type: Optional[Type] = None,
        arg_parser: Optional[Callable] = None,
        _override: bool = False,
    ):
        """
        为插件添加一个配置，不会被覆盖，只有第一个生效
        :param module: 模块
        :param key: 键
        :param value: 值
        :param name: 插件名称
        :param help_: 配置注解
        :param default_value: 默认值
        :param _override: 强制覆盖值
        """
        if not module or not key:
            raise ValueError("add_plugin_config: module和key不能为为空")
        if module in self._data and (config := self._data[module].configs.get(key)):
            config.help = help_
            config.arg_parser = arg_parser
            config.type = type
            if _override:
                config.value = value
                config.name = name
                config.default_value = default_value
        else:
            _module = None
            if ":" in module:
                module_split = module.split(":")
                if len(module_split) < 2:
                    raise ValueError(f"module: {module} 填写错误")
                _module = module_split[-1]
                module = module_split[0]
            if "[LEVEL]" in key and _module:
                key = key.replace("[LEVEL]", "").strip()
                self._admin_level_data.append((_module, value))
            key = key.upper()
            if not self._data.get(module):
                self._data[module] = ConfigGroup(module=module)
            self._data[module].configs[key] = Config(
                value=value,
                name=name,
                help=help_,
                default_value=default_value,
                level_module=_module,
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
        """
        设置配置值
        :param module: 模块名
        :param key: 配置名称
        :param value: 值
        :param auto_save: 自动保存
        :param save_simple_data: 保存至config.yaml
        """
        if module in self._data:
            if (
                self._data[module].configs.get(key)
                and self._data[module].configs[key] != value
            ):
                self._data[module].configs[key].value = value
                self._simple_data[module][key] = value
            if auto_save:
                self.save(save_simple_data=save_simple_data)

    def get_config(
        self, module: str, key: str, default: Optional[Any] = None
    ) -> Optional[Any]:
        """
        获取指定配置值
        :param module: 模块名
        :param key: 配置名称
        :param default: 没有key值内容的默认返回值
        """
        logger.debug(
            f"尝试获取配置 MODULE: [<u><y>{module}</y></u>] | KEY: [<u><y>{key}</y></u>]"
        )
        key = key.upper()
        value = None
        if module in self._data.keys():
            config = self._data[module].configs.get(key)
            if not config:
                config = self._data[module].configs.get(f"{key} [LEVEL]")
            if not config:
                raise NoSuchConfig(f"未查询到配置项 MODULE: [ {module} ] | KEY: [ {key} ]")
            if config.arg_parser:
                value = config.arg_parser(value or config.default_value)
            else:
                try:
                    if config.value is not None:
                        value = (
                            cattrs.structure(config.value, config.type)
                            if config.type
                            else config.value
                        )
                    else:
                        if config.default_value is not None:
                            value = (
                                cattrs.structure(config.default_value, config.type)
                                if config.type
                                else config.default_value
                            )
                except Exception as e:
                    logger.warning(
                        f"配置项类型转换 MODULE: [<u><y>{module}</y></u>] | KEY: [<u><y>{key}</y></u>]",
                        e=e,
                    )
                    value = config.value or config.default_value
        if value is None:
            value = default
        logger.debug(
            f"获取配置 MODULE: [<u><y>{module}</y></u>] | KEY: [<u><y>{key}</y></u>] -> [<u><c>{value}</c></u>]"
        )
        return value

    def get_level2module(self, module: str, key: str) -> Optional[str]:
        """
        获取指定key所绑定的module,一般为权限等级
        :param module: 模块名
        :param key: 配置名称
        :return:
        """
        if self._data.get(module) is not None:
            if config := self._data[module].configs.get(key):
                return config.level_module

    def get(self, key: str) -> Optional[ConfigGroup]:
        """
        获取插件配置数据
        :param key: 名称
        """
        return self._data.get(key)

    def save(
        self, path: Optional[Union[str, Path]] = None, save_simple_data: bool = False
    ):
        """
        保存数据
        :param path: 路径
        :param save_simple_data: 同时保存至config.yaml
        """
        if save_simple_data:
            with open(self._simple_file, "w", encoding="utf8") as f:
                yaml.dump(
                    self._simple_data,
                    f,
                    indent=2,
                    Dumper=yaml.RoundTripDumper,
                    allow_unicode=True,
                )
        path = path or self.file
        data = {}
        for module in self._data:
            data[module] = {}
            for config in self._data[module].configs:
                value = self._data[module].configs[config].dict()
                del value["type"]
                data[module][config] = value
        with open(path, "w", encoding="utf8") as f:
            yaml.dump(
                data, f, indent=2, Dumper=yaml.RoundTripDumper, allow_unicode=True
            )

    def reload(self):
        """
        重新加载配置文件
        """
        _yaml = YAML()
        if self._simple_file.exists():
            with open(self._simple_file, "r", encoding="utf8") as f:
                self._simple_data = _yaml.load(f)
        for key in self._simple_data.keys():
            for k in self._simple_data[key].keys():
                self._data[key].configs[k].value = self._simple_data[key][k]
        self.save()

    def load_data(self):
        """
        加载数据

        Raises:
            ValueError: _description_
        """
        if self.file.exists():
            _yaml = YAML()
            with open(self.file, "r", encoding="utf8") as f:
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
                    config_group.configs[config] = Config(**temp_data[module][config])
                    count += 1
                self._data[module] = config_group
            logger.info(
                f"加载配置完成，共加载 <u><y>{len(temp_data)}</y></u> 个配置组及对应 <u><y>{count}</y></u> 个配置项"
            )

    def get_admin_level_data(self):
        """
        获取管理插件等级
        """
        return self._admin_level_data

    def get_data(self) -> Dict[str, ConfigGroup]:
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
