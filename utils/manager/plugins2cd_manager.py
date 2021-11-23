from typing import Optional, Dict
from .data_class import StaticData
from utils.utils import FreqLimiter
from services.log import logger
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class Plugins2cdManager(StaticData):
    """
    插件命令 cd 管理器
    """

    def __init__(self, file: Path):
        self.file = file
        super().__init__(None)
        self._freq_limiter: Dict[str, FreqLimiter] = {}
        if file.exists():
            with open(file, "r", encoding="utf8") as f:
                self._data = yaml.load(f)
        if "PluginCdLimit" in self._data.keys():
            self._data = (
                self._data["PluginCdLimit"] if self._data["PluginCdLimit"] else {}
            )

    def add_cd_limit(
        self,
        plugin: str,
        *,
        cd: Optional[int] = 5,
        status: Optional[bool] = True,
        check_type: Optional[str] = "all",
        limit_type: Optional[str] = "user",
        rst: Optional[str] = None,
        data_dict: Optional[dict] = None,
    ):
        """
        添加插件调用 cd 限制
        :param plugin: 插件模块名称
        :param cd: cd 时长
        :param status: 默认开关状态
        :param check_type: 检查类型 'private'/'group'/'all'，限制私聊/群聊/全部
        :param limit_type: 限制类型 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
        :param rst: 回复的话，为空则不回复
        :param data_dict: 封装好的字典数据
        """
        if data_dict:
            cd = data_dict.get("cd")
            status = data_dict.get("status")
            check_type = data_dict.get("check_type")
            limit_type = data_dict.get("limit_type")
            rst = data_dict.get("rst")
            cd = cd if cd is not None else 5
            status = status if status is not None else True
            check_type = check_type if check_type else "all"
            limit_type = limit_type if limit_type else "user"
        if check_type not in ["all", "group", "private"]:
            raise ValueError(
                f"{plugin} 添加cd限制错误，‘check_type‘ 必须为 'private'/'group'/'all'"
            )
        if limit_type not in ["user", "group"]:
            raise ValueError(f"{plugin} 添加cd限制错误，‘limit_type‘ 必须为 'user'/'group'")
        self._data[plugin] = {
            "cd": cd,
            "status": status,
            "check_type": check_type,
            "limit_type": limit_type,
            "rst": rst,
        }

    def get_plugin_cd_data(self, plugin: str) -> Optional[dict]:
        """
        获取插件cd数据
        :param plugin: 模块名
        """
        if self.check_plugin_cd_status(plugin):
            return self._data[plugin]
        return None

    def check_plugin_cd_status(self, plugin: str) -> bool:
        """
        检测插件是否有 cd
        :param plugin: 模块名
        """
        return (
            plugin in self._data.keys()
            and self._data[plugin]["cd"] > 0
            and self._data[plugin]["status"]
        )

    def check(self, plugin: str, id_: int) -> bool:
        """
        检查 cd
        :param plugin: 模块名
        :param id_: 限制 id
        """
        if self._freq_limiter.get(plugin):
            return self._freq_limiter[plugin].check(id_)
        return False

    def start_cd(self, plugin: str, id_: int, cd: int = 0):
        """
        开始cd
        :param plugin: 模块名
        :param id_: cd 限制类型
        :param cd: cd 时长
        :return:
        """
        if self._freq_limiter.get(plugin):
            self._freq_limiter[plugin].start_cd(id_, cd)

    def get_plugin_data(self, plugin: str) -> dict:
        """
        获取单个模块限制数据
        :param plugin: 模块名
        """
        if self._data.get(plugin) is not None:
            return self._data.get(plugin)
        return {}

    def reload_cd_limit(self):
        """
        加载 cd 限制器
        :return:
        """
        for plugin in self._data:
            if self.check_plugin_cd_status(plugin):
                self._freq_limiter[plugin] = FreqLimiter(
                    self.get_plugin_cd_data(plugin)["cd"]
                )
        logger.info(f"已成功加载 {len(self._freq_limiter)} 个Cd限制.")

    def reload(self):
        """
        重载本地数据
        """
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                self._data: dict = yaml.load(f)
                self._data = self._data["PluginCdLimit"]
                self.reload_cd_limit()
