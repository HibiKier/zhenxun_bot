from .data_class import StaticData
from typing import List, Optional


class AdminManager(StaticData):
    """
    管理员命令 管理器
    """

    def __init__(self):
        super().__init__(None)

    def add_admin_plugin_settings(self, plugin: str, cmd: List[str], level: int):
        """
        添加一个管理员命令
        :param plugin: 模块
        :param cmd: 别名
        :param level: 等级
        """
        self._data[plugin] = {
            "level": level,
            "cmd": cmd,
        }

    def set_admin_level(self, plugin: str, level: int):
        """
        设置管理员命令等级
        :param plugin: 模块名
        :param level: 权限等级
        """
        self._data[plugin]["level"] = level

    def remove_admin_plugin_settings(self, plugin: str):
        """
        删除一个管理员命令
        :param plugin: 模块名
        """
        if plugin in self._data.keys():
            del self._data[plugin]

    def check(self, plugin: str, level: int) -> bool:
        """
        检查是否满足权限
        :param plugin: 模块名
        :param level: 权限等级
        """
        if plugin in self._data.keys():
            return level >= self._data[plugin]["level"]
        return True

    def get_plugin_level(self, plugin: str) -> int:
        """
        获取插件等级
        :param plugin: 模块名
        """
        if plugin in self._data.keys():
            return self._data[plugin]["level"]
        return 0

    def get_plugin_module(self, cmd: str) -> Optional[str]:
        """
        根据 cmd 获取功能 modules
        :param cmd: 命令
        """
        for key in self._data.keys():
            if self._data[key].get("cmd") and cmd in self._data[key]["cmd"]:
                return key
        return None
