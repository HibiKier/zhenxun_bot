from typing import Optional, Dict, Literal, Union, overload
from utils.manager.data_class import StaticData
from services.log import logger
from utils.utils import UserBlockLimiter
from pathlib import Path
from ruamel import yaml
from .models import PluginBlock

_yaml = yaml.YAML(typ="safe")


class Plugins2blockManager(StaticData):
    """
    插件命令阻塞 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file, False)
        self._block_limiter: Dict[str, UserBlockLimiter] = {}
        self.__load_file()

    @overload
    def add_block_limit(self, plugin: str, plugin_block: PluginBlock):
        ...

    @overload
    def add_block_limit(
        self,
        plugin: str,
        status: bool = True,
        check_type: Literal["private", "group", "all"] = "all",
        limit_type: Literal["user", "group"] = "user",
        rst: Optional[str] = None,
    ):
        ...

    def add_block_limit(
        self,
        plugin: str,
        status: Union[bool, PluginBlock] = True,
        check_type: Literal["private", "group", "all"] = "all",
        limit_type: Literal["user", "group"] = "user",
        rst: Optional[str] = None,
    ):
        """
        说明:
            添加插件调用 block 限制
        参数:
            :param plugin: 插件模块名称
            :param status: 默认开关状态
            :param check_type: 检查类型 'private'/'group'/'all'，限制私聊/群聊/全部
            :param limit_type: 限制类型 监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
            :param rst: 回复的话，为空则不回复
        """
        if isinstance(status, PluginBlock):
            self._data[plugin] = status
        else:
            if check_type not in ["all", "group", "private"]:
                raise ValueError(
                    f"{plugin} 添加block限制错误，‘check_type‘ 必须为 'private'/'group'/'all'"
                )
            if limit_type not in ["user", "group"]:
                raise ValueError(f"{plugin} 添加block限制错误，‘limit_type‘ 必须为 'user'/'group'")
            self._data[plugin] = PluginBlock(
                status=status, check_type=check_type, limit_type=limit_type, rst=rst
            )

    def get_plugin_block_data(self, plugin: str) -> Optional[PluginBlock]:
        """
        说明:
            获取插件block数据
        参数:
            :param plugin: 模块名
        """
        if self.check_plugin_block_status(plugin):
            return self._data[plugin]
        return None

    def check_plugin_block_status(self, plugin: str) -> bool:
        """
        说明:
            检测插件是否有 block
        参数:
            :param plugin: 模块名
        """
        return plugin in self._data.keys() and self._data[plugin].status

    def check(self, id_: int, plugin: str) -> bool:
        """
        说明:
            检查 block
        参数:
            :param id_: 限制 id
            :param plugin: 模块名
        """
        if self._block_limiter.get(plugin):
            return self._block_limiter[plugin].check(id_)
        return False

    def set_true(self, id_: int, plugin: str):
        """
        说明:
            对插件 block
        参数:
            :param id_: 限制 id
            :param plugin: 模块名
        """
        if self._block_limiter.get(plugin):
            self._block_limiter[plugin].set_true(id_)

    def set_false(self, id_: int, plugin: str):
        """
        说明:
            对插件 unblock
        参数:
            :param plugin: 模块名
            :param id_: 限制 id
        """
        if self._block_limiter.get(plugin):
            self._block_limiter[plugin].set_false(id_)

    def reload_block_limit(self):
        """
        说明:
            加载 block 限制器
        """
        for plugin in self._data:
            if self.check_plugin_block_status(plugin):
                self._block_limiter[plugin] = UserBlockLimiter()
        logger.info(f"已成功加载 {len(self._block_limiter)} 个Block限制.")

    def reload(self):
        """
        说明:
            重载本地数据
        """
        self.__load_file()
        self.reload_block_limit()

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
                    {"PluginBlockLimit": self.dict()},
                    f,
                    indent=2,
                    Dumper=yaml.RoundTripDumper,
                    allow_unicode=True,
                )
            _data = yaml.round_trip_load(open(path, encoding="utf8"))
            _data["PluginBlockLimit"].yaml_set_start_comment(
                """# 用户调用阻塞
# 即 当用户调用此功能还未结束时
# 用发送消息阻止用户重复调用此命令直到该命令结束
# key：模块名称
# status：此限制的开关状态
# check_type：'private'/'group'/'all'，限制私聊/群聊/全部
# limit_type：监听对象，以user_id或group_id作为键来限制，'user'：用户id，'group'：群id
#                                     示例：'user'：阻塞用户，'group'：阻塞群聊
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
        self._data: Dict[str, PluginBlock] = {}
        if self.file.exists():
            with open(self.file, "r", encoding="utf8") as f:
                temp = yaml.round_trip_load(f)
                if "PluginBlockLimit" in temp.keys():
                    for k, v in temp["PluginBlockLimit"].items():
                        self._data[k] = PluginBlock.parse_obj(v)
