from typing import Optional, Dict
from .data_class import StaticData
from services.log import logger
from utils.utils import UserBlockLimiter
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class Plugins2blockManager(StaticData):
    """
    插件命令阻塞 管理器
    """

    def __init__(self, file: Path):
        self.file = file
        super().__init__(None)
        self._block_limiter: Dict[str, UserBlockLimiter] = {}
        if file.exists():
            with open(file, "r", encoding="utf8") as f:
                self._data = yaml.load(f)
        if "PluginBlockLimit" in self._data.keys():
            self._data = (
                self._data["PluginBlockLimit"] if self._data["PluginBlockLimit"] else {}
            )

    def add_block_limit(
        self,
        plugin: str,
        status: Optional[bool] = True,
        check_type: Optional[str] = "all",
        limit_type: Optional[str] = "user",
        rst: Optional[str] = None,
        data_dict: Optional[dict] = None,
    ):
        """
        添加插件调用 block 限制
        :param plugin: 插件模块名称
        :param status: 默认开关状态
        :param check_type: 检查类型 'private'/'group'/'all'，限制私聊/群聊/全部
        :param limit_type: 限制类型 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
        :param rst: 回复的话，为空则不回复
        :param data_dict: 封装好的字典数据
        """
        if data_dict:
            status = data_dict.get("status")
            check_type = data_dict.get("check_type")
            limit_type = data_dict.get("limit_type")
            rst = data_dict.get("rst")
            status = status if status is not None else True
            check_type = check_type if check_type else "all"
            limit_type = limit_type if limit_type else "user"
        if check_type not in ["all", "group", "private"]:
            raise ValueError(
                f"{plugin} 添加block限制错误，‘check_type‘ 必须为 'private'/'group'/'all'"
            )
        if limit_type not in ["user", "group"]:
            raise ValueError(f"{plugin} 添加block限制错误，‘limit_type‘ 必须为 'user'/'group'")
        self._data[plugin] = {
            "status": status,
            "check_type": check_type,
            "limit_type": limit_type,
            "rst": rst,
        }

    def get_plugin_block_data(self, plugin: str) -> Optional[dict]:
        """
        获取插件block数据
        :param plugin: 模块名
        """
        if self.check_plugin_block_status(plugin):
            return self._data[plugin]
        return None

    def check_plugin_block_status(self, plugin: str) -> bool:
        """
        检测插件是否有 block
        :param plugin: 模块名
        """
        return plugin in self._data.keys() and self._data[plugin]["status"]

    def check(self, id_: int, plugin: str) -> bool:
        """
        检查 block
        :param plugin: 模块名
        :param id_: 限制 id
        """
        if self._block_limiter.get(plugin):
            return self._block_limiter[plugin].check(id_)
        return False

    def set_true(self, id_: int, plugin: str):
        """
        对插件 block
        :param plugin: 模块名
        :param id_: 限制 id
        """
        if self._block_limiter.get(plugin):
            self._block_limiter[plugin].set_true(id_)

    def set_false(self, id_: int, plugin: str):
        """
        对插件 unblock
        :param plugin: 模块名
        :param id_: 限制 id
        """
        if self._block_limiter.get(plugin):
            self._block_limiter[plugin].set_false(id_)

    def reload_block_limit(self):
        """
        加载 block 限制器
        :return:
        """
        for plugin in self._data:
            if self.check_plugin_block_status(plugin):
                self._block_limiter[plugin] = UserBlockLimiter()
        logger.info(f"已成功加载 {len(self._block_limiter)} 个Block限制.")

    def reload(self):
        """
        重载本地数据
        """
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                self._data: dict = yaml.load(f)
                self._data = self._data["PluginBlockLimit"]
                self.reload_block_limit()
