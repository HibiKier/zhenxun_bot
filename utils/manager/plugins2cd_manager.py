from typing import Optional, Dict, Literal, Union, overload
from utils.manager.data_class import StaticData
from utils.utils import FreqLimiter
from services.log import logger
from pathlib import Path
from ruamel import yaml
from .models import PluginCd

_yaml = yaml.YAML(typ="safe")


class Plugins2cdManager(StaticData[PluginCd]):
    """
    插件命令 cd 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file, False)
        self._freq_limiter: Dict[str, FreqLimiter] = {}
        self.__load_file()

    @overload
    def add_cd_limit(self, plugin: str, plugin_cd: PluginCd):
        ...

    @overload
    def add_cd_limit(
        self,
        plugin: str,
        cd: Union[int, PluginCd] = 5,
        status: Optional[bool] = True,
        check_type: Literal["private", "group", "all"] = "all",
        limit_type: Literal["user", "group"] = "user",
        rst: Optional[str] = None,
    ):
        ...

    def add_cd_limit(
        self,
        plugin: str,
        cd: Union[int, PluginCd] = 5,
        status: Optional[bool] = True,
        check_type: Literal["private", "group", "all"] = "all",
        limit_type: Literal["user", "group"] = "user",
        rst: Optional[str] = None,
    ):
        """
        说明:
            添加插件调用 cd 限制
        参数:
            :param plugin: 插件模块名称
            :param cd: cd 时长
            :param status: 默认开关状态
            :param check_type: 检查类型 'private'/'group'/'all'，限制私聊/群聊/全部
            :param limit_type: 限制类型 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
            :param rst: 回复的话，为空则不回复
        """
        if isinstance(cd, PluginCd):
            self._data[plugin] = cd
        else:
            if check_type not in ["all", "group", "private"]:
                raise ValueError(
                    f"{plugin} 添加cd限制错误，‘check_type‘ 必须为 'private'/'group'/'all'"
                )
            if limit_type not in ["user", "group"]:
                raise ValueError(f"{plugin} 添加cd限制错误，‘limit_type‘ 必须为 'user'/'group'")
            self._data[plugin] = PluginCd(cd=cd, status=status, check_type=check_type, limit_type=limit_type, rst=rst)

    def get_plugin_cd_data(self, plugin: str) -> Optional[PluginCd]:
        """
        说明:
            获取插件cd数据
        参数:
            :param plugin: 模块名
        """
        if self.check_plugin_cd_status(plugin):
            return self._data[plugin]
        return None

    def check_plugin_cd_status(self, plugin: str) -> bool:
        """
        说明:
            检测插件是否有 cd
        参数:
            :param plugin: 模块名
        """
        return (
            plugin in self._data.keys()
            and self._data[plugin].cd > 0
            and self._data[plugin].status
        )

    def check(self, plugin: str, id_: int) -> bool:
        """
        说明:
            检查 cd
            参数:
            :param plugin: 模块名
            :param id_: 限制 id
        """
        if self._freq_limiter.get(plugin):
            return self._freq_limiter[plugin].check(id_)
        return False

    def start_cd(self, plugin: str, id_: int, cd: int = 0):
        """
        说明:
            开始cd
        参数:
            :param plugin: 模块名
            :param id_: cd 限制类型
            :param cd: cd 时长
        """
        if self._freq_limiter.get(plugin):
            self._freq_limiter[plugin].start_cd(id_, cd)

    def get_plugin_data(self, plugin: str) -> Optional[PluginCd]:
        """
        说明:
            获取单个模块限制数据
        参数:
            :param plugin: 模块名
        """
        if self._data.get(plugin):
            return self._data.get(plugin)

    def reload_cd_limit(self):
        """
        说明:
            加载 cd 限制器
        """
        for plugin in self._data:
            if self.check_plugin_cd_status(plugin):
                self._freq_limiter[plugin] = FreqLimiter(
                    self.get_plugin_cd_data(plugin).cd
                )
        logger.info(f"已成功加载 {len(self._freq_limiter)} 个Cd限制.")

    def reload(self):
        """
        说明:
            重载本地数据
        """
        self.__load_file()
        self.reload_cd_limit()

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
                    {"PluginCdLimit": self.dict()},
                    f,
                    indent=2,
                    Dumper=yaml.RoundTripDumper,
                    allow_unicode=True,
                )
            _data = yaml.round_trip_load(open(path, encoding="utf8"))
            _data["PluginCdLimit"].yaml_set_start_comment(
                """# 需要cd的功能
# 自定义的功能需要cd也可以在此配置
# key：模块名称
# cd：cd 时长（秒）
# status：此限制的开关状态
# check_type：'private'/'group'/'all'，限制私聊/群聊/全部
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：用户N秒内触发1次，'group'：群N秒内触发1次
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
        self._data: Dict[str, PluginCd] = {}
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                temp = _yaml.load(f)
                if "PluginCdLimit" in temp.keys():
                    for k, v in temp["PluginCdLimit"].items():
                        self._data[k] = PluginCd.parse_obj(v)
