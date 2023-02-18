from typing import Dict, List, Optional

from utils.manager.data_class import StaticData

from .models import AdminSetting


class AdminManager(StaticData):
    """
    管理员命令 管理器
    """

    def __init__(self):
        super().__init__(None)
        self._data: Dict[str, AdminSetting] = {}

    def add_admin_plugin_settings(self, plugin: str, cmd: List[str], level: int):
        """
        说明:
            添加一个管理员命令
        参数:
            :param plugin: 模块
            :param cmd: 别名
            :param level: 等级
        """
        self._data[plugin] = AdminSetting(level=level, cmd=cmd)

    def set_admin_level(self, plugin: str, level: int):
        """
        说明:
            设置管理员命令等级
        参数:
            :param plugin: 模块名
            :param level: 权限等级
        """
        if plugin in self._data.keys():
            self._data[plugin].level = level

    def remove_admin_plugin_settings(self, plugin: str):
        """
        说明:
            删除一个管理员命令
        参数:
            :param plugin: 模块名
        """
        if plugin in self._data.keys():
            del self._data[plugin]

    def check(self, plugin: str, level: int) -> bool:
        """
        说明:
            检查是否满足权限
        参数:
            :param plugin: 模块名
            :param level: 权限等级
        """
        if plugin in self._data.keys():
            return level >= self._data[plugin].level
        return True

    def get_plugin_level(self, plugin: str) -> int:
        """
        说明:
            获取插件权限
        参数:
            :param plugin: 模块名
        """
        if plugin in self._data.keys():
            return self._data[plugin].level
        return 0

    def get_plugin_module(self, cmd: str) -> Optional[str]:
        """
        说明:
            根据 cmd 获取功能 modules
        参数:
            :param cmd: 命令
        """
        for key in self._data.keys():
            if data := self._data.get(key):
                if data.cmd and cmd in data.cmd:
                    return key
        return None
