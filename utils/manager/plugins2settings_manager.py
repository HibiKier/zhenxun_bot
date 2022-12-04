from typing import List, Optional, Union, Tuple, Dict, overload
from utils.manager.data_class import StaticData
from pathlib import Path
from ruamel import yaml
from .models import PluginSetting, PluginType

_yaml = yaml.YAML(typ="safe")


class Plugins2settingsManager(StaticData):
    """
    插件命令阻塞 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file, False)
        self.__load_file()

    @overload
    def add_plugin_settings(self, plugin: str, plugin_settings: PluginSetting):
        ...

    @overload
    def add_plugin_settings(
        self,
        plugin: str,
        cmd: List[str] = None,
        default_status: bool = True,
        level: int = 5,
        limit_superuser: bool = False,
        plugin_type: Tuple[Union[str, int]] = ("normal",),
        cost_gold: int = 0,
    ):
        ...

    def add_plugin_settings(
        self,
        plugin: str,
        cmd: Union[List[str], PluginSetting] = None,
        default_status: bool = True,
        level: int = 5,
        limit_superuser: bool = False,
        plugin_type: Tuple[Union[str, int]] = ("normal",),
        cost_gold: int = 0,
    ):
        """
        说明:
            添加一个插件设置
        参数:
            :param plugin: 插件模块名称
            :param cmd: 命令 或 命令别名
            :param default_status: 默认开关状态
            :param level: 功能权限等级
            :param limit_superuser: 功能状态是否限制超级用户
            :param plugin_type: 插件类型
            :param cost_gold: 需要消费的金币
        """
        if isinstance(cmd, PluginSetting):
            self._data[plugin] = cmd
        else:
            self._data[plugin] = PluginSetting(
                cmd=cmd,
                level=level,
                default_status=default_status,
                limit_superuser=limit_superuser,
                plugin_type=plugin_type,
                cost_gold=cost_gold,
            )

    def get_plugin_data(self, module: str) -> Optional[PluginSetting]:
        """
        说明:
            通过模块名获取数据
        参数:
            :param module: 模块名称
        """
        return self._data.get(module)

    def get_plugin_module(
        self, cmd: str, is_all: bool = False
    ) -> Union[str, List[str]]:
        """
        说明:
            根据 cmd 获取功能 modules
        参数:
            :param cmd: 命令
            :param is_all: 获取全部包含cmd的模块
        """
        keys = []
        for key in self._data.keys():
            if cmd in self._data[key].cmd:
                if is_all:
                    keys.append(key)
                else:
                    return key
        return keys

    def reload(self):
        """
        说明:
            重载本地数据
        """
        self.__load_file()

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
                self_dict = self.dict()
                for key in self_dict.keys():
                    if self_dict[key].get("plugin_type") and isinstance(
                        self_dict[key].get("plugin_type"), PluginType
                    ):
                        self_dict[key]["plugin_type"] = self_dict[key][
                            "plugin_type"
                        ].value
                yaml.dump(
                    {"PluginSettings": self_dict},
                    f,
                    indent=2,
                    Dumper=yaml.RoundTripDumper,
                    allow_unicode=True,
                )
            _data = yaml.round_trip_load(open(path, encoding="utf8"))
            _data["PluginSettings"].yaml_set_start_comment(
                """# 模块与对应命令和对应群权限
# 用于生成帮助图片 和 开关功能
# key：模块名称
# level：需要的群等级
# default_status：加入群时功能的默认开关状态
# limit_superuser: 功能状态是否限制超级用户
# cmd: 关闭[cmd] 都会触发命令 关闭对应功能，cmd列表第一个词为统计的功能名称
# plugin_type: 帮助类别 示例：('原神相关',) 或 ('原神相关', 1)，1代表帮助命令列向排列，否则为横向排列""",
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
        self._data: Dict[str, PluginSetting] = {}
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                if temp := _yaml.load(f):
                    if "PluginSettings" in temp.keys():
                        for k, v in temp["PluginSettings"].items():
                            self._data[k] = PluginSetting.parse_obj(v)
