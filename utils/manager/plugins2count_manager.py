from typing import Optional, Dict
from .data_class import StaticData
from utils.utils import DailyNumberLimiter
from services.log import logger
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class Plugins2countManager(StaticData):
    """
    插件命令 次数 管理器
    """

    def __init__(self, file: Path):
        self.file = file
        super().__init__(None)
        self._daily_limiter: Dict[str, DailyNumberLimiter] = {}
        if file.exists():
            with open(file, "r", encoding="utf8") as f:
                self._data = yaml.load(f)
        if "PluginCountLimit" in self._data.keys():
            self._data = (
                self._data["PluginCountLimit"] if self._data["PluginCountLimit"] else {}
            )

    def add_count_limit(
        self,
        plugin: str,
        *,
        max_count: int = 5,
        status: Optional[bool] = True,
        limit_type: Optional[str] = "user",
        rst: Optional[str] = None,
        data_dict: Optional[dict] = None,
    ):
        """
        添加插件调用 次数 限制
        :param plugin: 插件模块名称
        :param max_count: 最大次数限制
        :param status: 默认开关状态
        :param limit_type: 限制类型 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
        :param rst: 回复的话，为空则不回复
        :param data_dict: 封装好的字典数据
        """
        if data_dict:
            max_count = data_dict.get("max_count")
            status = data_dict.get("status")
            limit_type = data_dict.get("limit_type")
            rst = data_dict.get("rst")
            status = status if status is not None else True
            limit_type = limit_type if limit_type else "user"
            max_count = max_count if max_count is not None else 5
        if limit_type not in ["user", "group"]:
            raise ValueError(f"{plugin} 添加count限制错误，‘limit_type‘ 必须为 'user'/'group'")
        self._data[plugin] = {
            "max_count": max_count,
            "status": status,
            "limit_type": limit_type,
            "rst": rst,
        }

    def get_plugin_count_data(self, plugin: str) -> Optional[dict]:
        """
        获取插件次数数据
        :param plugin: 模块名
        """
        if self.check_plugin_count_status(plugin):
            return self._data[plugin]
        return None

    def get_plugin_data(self, plugin: str) -> Optional[dict]:
        """
        获取单个模块限制数据
        :param plugin: 模块名
        """
        if self._data.get(plugin) is not None:
            return self._data.get(plugin)
        return None

    def check_plugin_count_status(self, plugin: str) -> bool:
        """
        检测插件是否有 次数 限制
        :param plugin: 模块名
        """
        return (
            plugin in self._data.keys()
            and self._data[plugin]["status"]
            and self._data[plugin]["max_count"] > 0
        )

    def check(self, plugin: str, id_: int) -> bool:
        """
        检查 count
        :param plugin: 模块名
        :param id_: 限制 id
        """
        if self._daily_limiter.get(plugin):
            return self._daily_limiter[plugin].check(id_)
        return True

    def increase(self, plugin: str, id_: int, num: int = 1):
        """
        增加次数
        :param plugin: 模块名
        :param id_: cd 限制类型
        :param num: 增加次数
        :return:
        """
        if self._daily_limiter.get(plugin):
            self._daily_limiter[plugin].increase(id_, num)

    def reload_count_limit(self):
        """
        加载 cd 限制器
        :return:
        """
        for plugin in self._data:
            if self.check_plugin_count_status(plugin):
                self._daily_limiter[plugin] = DailyNumberLimiter(
                    self.get_plugin_count_data(plugin)["max_count"]
                )
        logger.info(f"已成功加载 {len(self._daily_limiter)} 个Count限制.")

    def reload(self):
        """
        重载本地数据
        """
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                self._data: dict = yaml.load(f)
                self._data = self._data["PluginCountLimit"]
                self.reload_count_limit()
