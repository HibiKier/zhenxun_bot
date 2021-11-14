from typing import Optional
from pathlib import Path
from .data_class import StaticData
from . import group_manager


class PluginsManager(StaticData):
    """
    插件 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file)
        if not self._data:
            self._data = {}

    def add_plugin_data(
        self,
        module: str,
        plugin_name: str,
        *,
        status: Optional[bool] = True,
        error: Optional[bool] = False,
        block_type: Optional[str] = None,
        author: Optional[str] = None,
        version: Optional[int] = None,
    ):
        """
        添加插件数据
        :param module: 模块名称
        :param plugin_name: 插件名称
        :param status: 插件开关状态
        :param error: 加载状态
        :param block_type: 限制类型
        :param author: 作者
        :param version: 版本
        """
        self._data[module] = {
            "plugin_name": plugin_name,
            "status": status,
            "error": error,
            "block_type": block_type,
            "author": author,
            "version": version,
        }

    def block_plugin(
        self, module: str, group_id: Optional[int] = None, block_type: str = "all"
    ):
        """
        说明：
            锁定插件
        参数：
            :param module: 功能模块名
            :param group_id: 群组，None时为超级用户禁用
            :param block_type: 限制类型
        """
        self._set_plugin_status(module, "block", group_id, block_type)

    def unblock_plugin(self, module: str, group_id: Optional[int] = None):
        """
        说明：
            解锁插件
        参数：
            :param module: 功能模块名
            :param group_id: 群组
        """
        self._set_plugin_status(module, "unblock", group_id)

    def get_plugin_status(
        self, module: str, block_type: str = "all"
    ) -> bool:
        """
        说明：
            获取插件状态
        参数：
            :param module: 功能模块名
            :param block_type: 限制类型
        """
        if module in self._data.keys():
            if self._data[module]["block_type"] == "all" and block_type == "all":
                return False
            else:
                return not self._data[module]["block_type"] == block_type
        return True

    def get_plugin_block_type(self, module: str) -> str:
        """
        说明：
            获取功能限制类型
        参数：
            :param module: 模块名称
        """
        if module in self._data.keys():
            return self._data[module]["block_type"]
        return ""

    def get_plugin_error_status(self, module: str) -> bool:
        """
        插件是否成功加载
        :param module: 模块名称
        """
        if module not in self._data.keys():
            self.init_plugin(module)
        return self._data[module]["error"]

    def _set_plugin_status(
        self,
        module: str,
        status: str,
        group_id: Optional[str],
        block_type: str = "all",
    ):
        """
        说明：
            设置功能开关状态
        参数：
            :param module: 功能模块名
            :param status: 功能状态
            :param group_id: 群组
            :param block_type: 限制类型
        """
        group_id = str(group_id) if group_id else group_id
        if module:
            if group_id:
                if status == "block":
                    group_manager.block_plugin(f"{module}:super", int(group_id))
                else:
                    group_manager.unblock_plugin(f"{module}:super", int(group_id))
            else:
                if module not in self._data.keys():
                    self.init_plugin(module)
                if status == "block":
                    self._data[module]["status"] = False
                    self._data[module]["block_type"] = block_type
                else:
                    if module in self._data.keys():
                        self._data[module]["status"] = True
                        self._data[module]["block_type"] = None
            self.save()

    def init_plugin(self, module: str):
        """
        初始化插件数据
        :param module: 模块名称
        """
        if module not in self._data.keys():
            self._data[module] = {
                "plugin_name": module,
                "status": True,
                "error": False,
                "block_type": None,
                "author": None,
                "version": None,
            }
