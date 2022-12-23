from typing import Optional, Dict, Literal, Union, overload
from utils.manager.data_class import StaticData
from utils.utils import DailyNumberLimiter
from services.log import logger
from pathlib import Path
from ruamel import yaml
from .models import PluginCount

_yaml = yaml.YAML(typ="safe")


class Plugins2countManager(StaticData[PluginCount]):
    """
    插件命令 次数 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file, False)
        self._daily_limiter: Dict[str, DailyNumberLimiter] = {}
        self.__load_file()

    @overload
    def add_count_limit(self, plugin: str, plugin_count: PluginCount):
        ...

    @overload
    def add_count_limit(
        self,
        plugin: str,
        max_count: int = 5,
        status: Optional[bool] = True,
        limit_type: Literal["user", "group"] = "user",
        rst: Optional[str] = None,
    ):
        ...

    def add_count_limit(
        self,
        plugin: str,
        max_count: Union[int, PluginCount] = 5,
        status: Optional[bool] = True,
        limit_type: Literal["user", "group"] = "user",
        rst: Optional[str] = None,
    ):
        """
        说明:
            添加插件调用 次数 限制
        参数:
            :param plugin: 插件模块名称
            :param max_count: 最大次数限制
            :param status: 默认开关状态
            :param limit_type: 限制类型 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
            :param rst: 回复的话，为空则不回复
        """
        if isinstance(max_count, PluginCount):
            self._data[plugin] = max_count
        else:
            if limit_type not in ["user", "group"]:
                raise ValueError(f"{plugin} 添加count限制错误，‘limit_type‘ 必须为 'user'/'group'")
            self._data[plugin] = PluginCount(max_count=max_count, status=status, limit_type=limit_type, rst=rst)

    def get_plugin_count_data(self, plugin: str) -> Optional[PluginCount]:
        """
        说明:
            获取插件次数数据
        参数:
            :param plugin: 模块名
        """
        if self.check_plugin_count_status(plugin):
            return self._data[plugin]
        return None

    def get_plugin_data(self, plugin: str) -> Optional[PluginCount]:
        """
        说明:
            获取单个模块限制数据
        参数:
            :param plugin: 模块名
        """
        if self._data.get(plugin) is not None:
            return self._data.get(plugin)

    def check_plugin_count_status(self, plugin: str) -> bool:
        """
        说明:
            检测插件是否有 次数 限制
        参数:
            :param plugin: 模块名
        """
        return (
            plugin in self._data.keys()
            and self._data[plugin].status
            and self._data[plugin].max_count > 0
        )

    def check(self, plugin: str, id_: int) -> bool:
        """
        说明:
            检查 count
        参数:
            :param plugin: 模块名
            :param id_: 限制 id
        """
        if self._daily_limiter.get(plugin):
            return self._daily_limiter[plugin].check(id_)
        return True

    def increase(self, plugin: str, id_: int, num: int = 1):
        """
        说明:
            增加次数
        参数:
            :param plugin: 模块名
            :param id_: cd 限制类型
            :param num: 增加次数
        """
        if self._daily_limiter.get(plugin):
            self._daily_limiter[plugin].increase(id_, num)

    def reload_count_limit(self):
        """
        说明:
            加载 cd 限制器
        """
        for plugin in self._data:
            if self.check_plugin_count_status(plugin):
                self._daily_limiter[plugin] = DailyNumberLimiter(
                    self.get_plugin_count_data(plugin).max_count
                )
        logger.info(f"已成功加载 {len(self._daily_limiter)} 个Count限制.")

    def reload(self):
        """
        重载本地数据
        """
        self.__load_file()
        self.reload_count_limit()

    def save(self, path: Union[str, Path] = None):
        """
        说明:
            保存文件
        参数:
            :param path: 文件路径
        """
        path = path or self.file
        if isinstance(path, str):
            path = Path(path)
        if path:
            with open(path, "w", encoding="utf8") as f:
                yaml.dump(
                    {"PluginCountLimit": self.dict()},
                    f,
                    indent=2,
                    Dumper=yaml.RoundTripDumper,
                    allow_unicode=True,
                )
            _data = yaml.round_trip_load(open(path, encoding="utf8"))
            _data["PluginCountLimit"].yaml_set_start_comment(
                """# 命令每日次数限制
# 即 用户/群聊 每日可调用命令的次数 [数据内存存储，重启将会重置]
# 每日调用直到 00:00 刷新
# key：模块名称
# max_count: 每日调用上限
# status：此限制的开关状态
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：用户上限，'group'：群聊上限
# rst：回复的话，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
# rst 为 "" 或 None 时则不回复
# rst示例："[uname]你冲的太快了，[nickname]先生，请稍后再冲[at]"
# rst回复："老色批你冲的太快了，欧尼酱先生，请稍后再冲@老色批"
#      用户昵称↑     昵称系统的昵称↑          艾特用户↑""",
                indent=2,
            )
            with open(path, "w", encoding="utf8") as wf:
                yaml.round_trip_dump(
                    _data, wf, Dumper=yaml.RoundTripDumper, allow_unicode=True
                )

    def __load_file(self):
        """
        说明:
            读取配置文件
        """
        self._data: Dict[str, PluginCount] = {}
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                temp = _yaml.load(f)
                if "PluginCountLimit" in temp.keys():
                    for k, v in temp["PluginCountLimit"].items():
                        self._data[k] = PluginCount.parse_obj(v)
