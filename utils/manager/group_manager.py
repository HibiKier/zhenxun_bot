from configs.config import DEFAULT_GROUP_LEVEL
from typing import Optional, List, Union, Dict
from pathlib import Path
from .data_class import StaticData
from utils.utils import get_matchers, get_bot
import nonebot


class GroupManager(StaticData):
    """
    群权限 | 功能 | 聊天时间 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file)
        if not self._data:
            self._data = {
                "super": {"close_plugins": {}, "white_group_list": []},
                "group_manager": {},
            }
        self._task = {}

    def block_plugin(
        self, plugin_cmd: str, group_id: Optional[int] = None, block_type: str = "all"
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

    def unblock_plugin(self, plugin_cmd: str, group_id: Optional[int] = None):
        """
        说明：
            解锁插件
        参数：
            :param plugin_cmd: 功能模块名
            :param group_id: 群组
        """
        self._set_plugin_status(plugin_cmd, "unblock", group_id)

    def set_group_level(self, group_id: int, level: int):
        """
        说明：
            设置群权限
        参数：
            :param group_id: 群组
            :param level: 权限等级
        """
        group_id = str(group_id)
        if not self._data["group_manager"].get(group_id):
            self._init_group(group_id)
        self._data["group_manager"][group_id]["level"] = level
        self.save()

    def get_plugin_status(
        self, plugin_cmd: str, group_id: Optional[int] = None, block_type: str = "all"
    ) -> bool:
        """
        说明：
            获取插件状态
        参数：
            :param plugin_cmd: 功能模块名
            :param group_id: 群组
            :param block_type: 限制类型
        """
        group_id = str(group_id) if group_id else group_id
        if group_id:
            if not self._data["group_manager"].get(group_id):
                self._init_group(group_id)
                return True
            if plugin_cmd in self._data["group_manager"][group_id]["close_plugins"]:
                return False
            return True
        else:
            if plugin_cmd in self._data["super"]["close_plugins"]:
                if (
                    self._data["super"]["close_plugins"][plugin_cmd] == "all"
                    and block_type == "all"
                ):
                    return False
                else:
                    return (
                        not self._data["super"]["close_plugins"][plugin_cmd]
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
        if plugin_cmd in self._data["super"]["close_plugins"]:
            return self._data["super"]["close_plugins"][plugin_cmd]
        return ""

    def get_group_level(self, group_id: int) -> int:
        """
        说明：
            获取群等级
        参数：
            :param group_id: 群号
        """
        group_id = str(group_id)
        if not self._data["group_manager"].get(group_id):
            self._init_group(group_id)
        return self._data["group_manager"][group_id]["level"]

    def check_group_is_white(self, group_id: int) -> bool:
        """
        说明：
            检测群聊是否在白名单
        参数：
            :param group_id: 群号
        """
        return group_id in self._data["super"]["white_group_list"]

    def add_group_white_list(self, group_id: int):
        """
        说明：
            将群聊加入白名单
        参数：
            :param group_id: 群号
        """
        if group_id not in self._data["super"]["white_group_list"]:
            self._data["super"]["white_group_list"].append(group_id)

    def delete_group_white_list(self, group_id: int):
        """
        说明：
            将群聊从白名单中删除
        参数：
            :param group_id: 群号
        """
        if group_id in self._data["super"]["white_group_list"]:
            self._data["super"]["white_group_list"].remove(group_id)

    def get_group_white_list(self) -> List[str]:
        """
        说明：
            获取所有群白名单
        """
        return self._data["super"]["white_group_list"]

    async def open_group_task(self, group_id: int, task: str):
        """
        开启群被动技能
        :param group_id: 群号
        :param task: 被动技能名称
        """
        await self._set_group_task_status(group_id, task, True)

    async def close_group_task(self, group_id: int, task: str):
        """
        关闭群被动技能
        :param group_id: 群号
        :param task: 被动技能名称
        """
        await self._set_group_task_status(group_id, task, False)

    async def check_group_task_status(self, group_id: int, task: str) -> bool:
        """
        查看群被动技能状态
        :param group_id: 群号
        :param task: 被动技能名称
        """
        group_id = str(group_id)
        if (
            not self._data["group_manager"][group_id].get("group_task_status")
            or self._data["group_manager"][group_id]["group_task_status"].get(task)
            is None
        ):
            await self.init_group_task(group_id)
        return self._data["group_manager"][group_id]["group_task_status"][task]

    def get_task_data(self) -> Dict[str, str]:
        return self._task

    async def group_task_status(self, group_id: int) -> str:
        """
        查看群被全部动技能状态
        :param group_id: 群号
        """
        x = '[群被动技能]:\n'
        group_id = str(group_id)
        if not self._data["group_manager"][group_id].get("group_task_status"):
            await self.init_group_task(group_id)
        for key in self._data["group_manager"][group_id]["group_task_status"].keys():
            x += f'{self._task[key]}：{"√" if await self.check_group_task_status(int(group_id), key) else "×"}\n'
        return x[:-1]

    async def _set_group_task_status(self, group_id: int, task: str, status: bool):
        """
        管理群被动技能状态
        :param group_id: 群号
        :param task: 被动技能
        :param status: 状态
        """
        group_id = str(group_id)
        if not self._data["group_manager"].get(group_id):
            self._init_group(group_id)
        if (
            not self._data["group_manager"][group_id].get("group_task_status")
            or self._data["group_manager"][group_id]["group_task_status"].get(task)
            is None
        ):
            await self.init_group_task(group_id)
        self._data["group_manager"][group_id]["group_task_status"][task] = status
        self.save()

    async def init_group_task(self, group_id: Optional[Union[int, str]] = None):
        """
        初始化群聊 被动技能 状态
        """
        if not self._task:
            for matcher in get_matchers():
                _plugin = nonebot.plugin.get_plugin(matcher.module)
                _module = _plugin.module
                try:
                    plugin_task = _module.__getattribute__("__plugin_task__")
                    for key in plugin_task.keys():
                        self._task[key] = plugin_task[key]
                except AttributeError:
                    pass
        bot = get_bot()
        if bot or group_id:
            if group_id:
                _group_list = [group_id]
            else:
                _group_list = [x["group_id"] for x in await bot.get_group_list()]
            for group_id in _group_list:
                group_id = str(group_id)
                if not self._data["group_manager"].get(group_id):
                    self._init_group(group_id)
                if not self._data["group_manager"][group_id].get("group_task_status"):
                    self._data["group_manager"][group_id]['group_task_status'] = {}
                for task in self._task:
                    if (
                        self._data["group_manager"][group_id][
                            "group_task_status"
                        ].get(task)
                        is None
                    ):
                        self._data["group_manager"][group_id]["group_task_status"][
                            task
                        ] = True
                for task in self._data["group_manager"][group_id]["group_task_status"]:
                    if task not in self._task:
                        del self._data["group_manager"][group_id]["group_task_status"][
                            task
                        ]
        self.save()

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
        group_id = str(group_id) if group_id else group_id
        if plugin_cmd:
            if group_id:
                if not self._data["group_manager"].get(group_id):
                    self._init_group(group_id)
                if status == "block":
                    if (
                        plugin_cmd
                        not in self._data["group_manager"][group_id]["close_plugins"]
                    ):
                        self._data["group_manager"][group_id]["close_plugins"].append(
                            plugin_cmd
                        )
                else:
                    if plugin_cmd in self._data["group_manager"][group_id]["close_plugins"]:
                        self._data["group_manager"][group_id]["close_plugins"].remove(
                            plugin_cmd
                        )
            else:
                if status == "block":
                    if (
                        plugin_cmd not in self._data["super"]["close_plugins"]
                        or block_type != self._data["super"]["close_plugins"][plugin_cmd]
                    ):
                        self._data["super"]["close_plugins"][plugin_cmd] = block_type
                else:
                    if plugin_cmd in self._data["super"]["close_plugins"]:
                        del self._data["super"]["close_plugins"][plugin_cmd]
            self.save()

    def _init_group(self, group_id: str):
        """
        说明：
            初始化群数据
        参数：
            :param group_id: 群号
        """
        if not self._data["group_manager"].get(group_id):
            self._data["group_manager"][group_id] = {
                "level": DEFAULT_GROUP_LEVEL,
                "close_plugins": [],
                "group_task_status": {},
            }
