from typing import Optional
from pathlib import Path
from .data_class import StaticData


class GroupManager(StaticData):
    """
    群权限 | 功能 | 聊天时间 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file)
        if not self.data:
            self.data = {"super": {"close_plugins": {}, "white_group_list": []}, "group_manager": {}}

    def block_plugin(
        self, plugin_cmd: str, group_id: Optional[str] = None, block_type: str = "all"
    ):
        """
        说明：
            锁定插件
        参数：
            :param plugin_cmd: 功能模块名
            :param group_id: 群组，None时为超级用户禁用
            :param block_type: 限制类型
        """
        self._set_plugin_status(plugin_cmd, "block", group_id, block_type)

    def unblock_plugin(self, plugin_cmd: str, group_id: Optional[str] = None):
        """
        说明：
            解锁插件
        参数：
            :param plugin_cmd: 功能模块名
            :param group_id: 群组
        """
        self._set_plugin_status(plugin_cmd, "unblock", group_id)

    def set_group_level(self, group_id: str, level: int):
        """
        说明：
            设置群权限
        参数：
            :param group_id: 群组
            :param level: 权限等级
        """
        if not self.data["group_manager"].get(group_id):
            self._init_group(group_id)
        self.data["group_manager"][group_id]["level"] = level
        self.save()

    def get_plugin_status(
        self, plugin_cmd: str, group_id: Optional[str] = None, block_type: str = "all"
    ) -> bool:
        """
        说明：
            获取插件状态
        参数：
            :param plugin_cmd: 功能模块名
            :param group_id: 群组
            :param block_type: 限制类型
        """
        if group_id:
            if not self.data["group_manager"].get(group_id):
                self._init_group(group_id)
                return True
            if plugin_cmd in self.data["group_manager"][group_id]["close_plugins"]:
                return False
            return True
        else:
            if plugin_cmd in self.data["super"]["close_plugins"]:
                if (
                    self.data["super"]["close_plugins"][plugin_cmd] == "all"
                    and block_type == "all"
                ):
                    return False
                else:
                    return (
                        not self.data["super"]["close_plugins"][plugin_cmd]
                        == block_type
                    )
            return True

    def get_plugin_block_type(self, plugin_cmd: str) -> str:
        """
        说明：
            获取功能限制类型
        参数：
            :param plugin_cmd: 模块名称
        """
        if plugin_cmd in self.data["super"]["close_plugins"]:
            return self.data["super"]["close_plugins"][plugin_cmd]
        return ""

    def get_group_level(self, group_id: str) -> int:
        """
        说明：
            获取群等级
        参数：
            :param group_id: 群号
        """
        if not self.data["group_manager"].get(group_id):
            self._init_group(group_id)
        return self.data["group_manager"][group_id]["level"]

    def check_group_is_white(self, group_id: int) -> bool:
        """
        说明：
            检测群聊是否在白名单
        参数：
            :param group_id: 群号
        """
        return group_id in self.data['super']['white_group_list']

    def add_group_white_list(self, group_id: int):
        """
        说明：
            将群聊加入白名单
        参数：
            :param group_id: 群号
        """
        if group_id not in self.data['super']['white_group_list']:
            self.data['super']['white_group_list'].append(group_id)

    def delete_group_white_list(self, group_id: int):
        """
        说明：
            将群聊从白名单中删除
        参数：
            :param group_id: 群号
        """
        if group_id in self.data['super']['white_group_list']:
            self.data['super']['white_group_list'].remove(group_id)

    def _set_plugin_status(
        self,
        plugin_cmd: str,
        status: str,
        group_id: Optional[str],
        block_type: str = "all",
    ):
        """
        说明：
            设置功能开关状态
        参数：
            :param plugin_cmd: 功能模块名
            :param status: 功能状态
            :param group_id: 群组
            :param block_type: 限制类型
        """
        if group_id:
            if not self.data["group_manager"].get(group_id):
                self._init_group(group_id)
            if status == "block":
                if (
                    plugin_cmd
                    not in self.data["group_manager"][group_id]["close_plugins"]
                ):
                    self.data["group_manager"][group_id]["close_plugins"].append(
                        plugin_cmd
                    )
            else:
                if plugin_cmd in self.data["group_manager"][group_id]["close_plugins"]:
                    self.data["group_manager"][group_id]["close_plugins"].remove(
                        plugin_cmd
                    )
        else:
            if status == "block":
                if (
                    plugin_cmd not in self.data["super"]["close_plugins"]
                    or block_type != self.data["super"]["close_plugins"][plugin_cmd]
                ):
                    self.data["super"]["close_plugins"][plugin_cmd] = block_type
            else:
                if plugin_cmd in self.data["super"]["close_plugins"]:
                    del self.data["super"]["close_plugins"][plugin_cmd]
        self.save()

    def _init_group(self, group_id: str):
        """
        说明：
            初始化群数据
        参数：
            :param group_id: 群号
        """
        self.data["group_manager"][group_id] = {"level": 5, "close_plugins": []}
