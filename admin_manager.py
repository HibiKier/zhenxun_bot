from typing import Optional, Dict
from .data_class import StaticData
from utils.utils import FreqLimiter
from services.log import logger
from pathlib import Path


class AdminManager(StaticData):
    """
    管理员命令 管理器
    """

    def __init__(self):
        super().__init__(None)

    def add_admin_command(self, plugin: str, level: int):
        """
        添加一个管理员命令
        :param plugin: 模块名
        :param level: 权限等级
        """
        self._data[plugin] = level

    def remove_admin_command(self, plugin: str):
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
            return level >= self._data[plugin]
        return True

    def get_plugin_level(self, plugin: str) -> int:
        """
        获取插件等级
        :param plugin: 模块名
        """
        if plugin in self._data.keys():
            return self._data[plugin]
        return 0


