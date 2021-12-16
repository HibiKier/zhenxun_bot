from typing import Optional, Any, Union
from pathlib import Path
from ruamel.yaml import YAML
from ruamel import yaml


class ConfigsManager:
    """
    插件配置 与 资源 管理器
    """

    def __init__(self, file: Path):
        self._data: dict = {}
        self._admin_level_data = []
        if file:
            file.parent.mkdir(exist_ok=True, parents=True)
            self.file = file
            if file.exists():
                _yaml = YAML()
                with open(file, "r", encoding="utf8") as f:
                    self._data = _yaml.load(f)

    def add_plugin_config(
        self,
        module: str,
        key: str,
        value: Optional[Any],
        *,
        name: Optional[str] = None,
        help_: Optional[str] = None,
        default_value: Optional[str] = None,
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
        :param _override: 覆盖前值
        """
        if (
            not (module in self._data.keys() and self._data[module].get(key))
            or _override
        ):
            _module = None
            if ":" in module:
                module = module.split(":")
                _module = module[-1]
                module = module[0]
            if "[LEVEL]" in key and _module:
                key = key.replace("[LEVEL]", "").strip()
                self._admin_level_data.append((_module, value))
            if self._data.get(module) is None:
                self._data[module] = {}
            key = key.upper()
            self._data[module][key] = {
                "value": value,
                "name": name.strip() if isinstance(name, str) else name,
                "help": help_.strip() if isinstance(help_, str) else help_,
                "default_value": default_value,
                "level_module": _module,
            }

    def remove_plugin_config(self, module: str):
        """
        为插件删除一个配置
        :param module: 模块名
        """
        if module in self._data.keys():
            del self._data[module]

    def set_config(self, module: str, key: str, value: str):
        """
        设置配置值
        :param module: 模块名
        :param key: 配置名称
        :param value: 值
        """
        if module in self._data.keys():
            if self._data[module].get(key) is not None:
                self._data[module][key]["value"] = value

    def set_help(self, module: str, key: str, help_: str):
        """
        设置配置注释
        :param module: 模块名
        :param key: 配置名称
        :param help_: 注释文本
        """
        if module in self._data.keys():
            if self._data[module].get(key) is not None:
                self._data[module][key]["help"] = help_

    def set_default_value(self, module: str, key: str, value: str):
        """
        设置配置默认值
        :param module: 模块名
        :param key: 配置名称
        :param value: 值
        """
        if module in self._data.keys():
            if self._data[module].get(key) is not None:
                self._data[module][key]["default_value"] = value

    def get_config(self, module: str, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        获取指定配置值
        :param module: 模块名
        :param key: 配置名称
        :param default: 没有key值内容的默认返回值
        """
        key = key.upper()
        if module in self._data.keys():
            for key in [key, f"{key} [LEVEL]"]:
                if self._data[module].get(key) is not None:
                    if self._data[module][key]["value"] is None:
                        return self._data[module][key]["default_value"]
                    return self._data[module][key]["value"]
        if default is not None:
            return default
        return None

    def get_level2module(self, module: str, key: str) -> Optional[str]:
        """
        获取指定key所绑定的module，一般为权限等级
        :param module: 模块名
        :param key: 配置名称
        :return:
        """
        if self._data.get(module) is not None:
            if self._data[module].get(key) is not None:
                return self._data[module][key].get("level_module")

    def get(self, key: str):
        """
        获取插件配置数据
        :param key: 名称
        """
        if key in self._data.keys():
            return self._data[key]

    def save(self, path: Union[str, Path] = None):
        """
        保存数据
        :param path: 路径
        """
        path = path if path else self.file
        with open(path, "w", encoding="utf8") as f:
            yaml.dump(
                self._data, f, indent=2, Dumper=yaml.RoundTripDumper, allow_unicode=True
            )

    def get_admin_level_data(self):
        """
        获取管理插件等级
        """
        return self._admin_level_data

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
