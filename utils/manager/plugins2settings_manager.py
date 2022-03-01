from typing import List, Optional, Union, Tuple
from .data_class import StaticData
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class Plugins2settingsManager(StaticData):
    """
    插件命令阻塞 管理器
    """

    def __init__(self, file: Path):
        self.file = file
        super().__init__(None)
        if file.exists():
            with open(file, "r", encoding="utf8") as f:
                self._data = yaml.load(f)
        if self._data:
            if "PluginSettings" in self._data.keys():
                self._data = (
                    self._data["PluginSettings"] if self._data["PluginSettings"] else {}
                )
            for x in self._data.keys():
                if self._data[x].get("cost_gold") is None:
                    self._data[x]["cost_gold"] = 0

    def add_plugin_settings(
        self,
        plugin: str,
        cmd: Optional[List[str]] = None,
        default_status: Optional[bool] = True,
        level: Optional[int] = 5,
        limit_superuser: Optional[bool] = False,
        plugin_type: Tuple[Union[str, int]] = ("normal",),
        cost_gold: int = 0,
        **kwargs
    ):
        """
        添加一个插件设置
        :param plugin: 插件模块名称
        :param cmd: 命令 或 命令别名
        :param default_status: 默认开关状态
        :param level: 功能权限等级
        :param limit_superuser: 功能状态是否限制超级用户
        :param plugin_type: 插件类型
        :param cost_gold: 需要消费的金币
        """
        if kwargs:
            level = kwargs.get("level") if kwargs.get("level") is not None else 5
            default_status = (
                kwargs.get("default_status")
                if kwargs.get("default_status") is not None
                else True
            )
            limit_superuser = (
                kwargs.get("limit_superuser")
                if kwargs.get("limit_superuser") is not None
                else False
            )
            cmd = kwargs.get("cmd") if kwargs.get("cmd") is not None else []
            cost_gold = cost_gold if kwargs.get("cost_gold") else 0
        self._data[plugin] = {
            "level": level if level is not None else 5,
            "default_status": default_status if default_status is not None else True,
            "limit_superuser": limit_superuser
            if limit_superuser is not None
            else False,
            "cmd": cmd,
            "plugin_type": list(
                plugin_type if plugin_type is not None else ("normal",)
            ),
            "cost_gold": cost_gold,
        }

    def get_plugin_data(self, module: str) -> dict:
        """
        通过模块名获取数据
        :param module: 模块名称
        """
        if self._data.get(module) is not None:
            return self._data.get(module)
        return {}

    def get_plugin_module(
        self, cmd: str, is_all: bool = False
    ) -> Union[str, List[str]]:
        """
        根据 cmd 获取功能 modules
        :param cmd: 命令
        :param is_all: 获取全部包含cmd的模块
        """
        keys = []
        for key in self._data.keys():
            if cmd in self._data[key]["cmd"]:
                if is_all:
                    keys.append(key)
                else:
                    return key
        return keys

    def reload(self):
        """
        重载本地数据
        """
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                self._data: dict = yaml.load(f)
                self._data = self._data["PluginSettings"]
