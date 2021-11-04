from .data_class import StaticData
from typing import Optional
from pathlib import Path


class NonePluginCountManager(StaticData):

    """
    插件加载容忍管理器，当连续 max_count 次插件加载，视为删除插件，清楚数据
    """

    def __init__(self, file: Optional[Path], max_count: int = 5):
        """
        :param file: 存储路径
        :param max_count: 容忍最大次数
        """
        super().__init__(file)
        self._max_count = max_count

    def add_count(self, module: str, count: int = 1):
        """
        添加次数
        :param module: 模块
        :param count: 次数，无特殊情况均为 1
        """
        if module not in self._data.keys():
            self._data[module] = count
        else:
            self._data[module] += count

    def reset(self, module: str):
        """
        重置次数
        :param module: 模块
        """
        if module in self._data.keys():
            self._data[module] = 0

    def check(self, module: str):
        """
        检查容忍次数是否到达最大值
        :param module: 模块
        """
        if module in self._data.keys():
            return self._data.keys() > self._max_count
        return False





