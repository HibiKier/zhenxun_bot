import copy
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import nonebot
import ujson as json

from configs.config import Config
from utils.manager.data_class import StaticData
from utils.utils import get_matchers, is_number

from .models import BaseData, BaseGroup

Config.add_plugin_config(
    "group_manager", "DEFAULT_GROUP_LEVEL", 5, help_="默认群权限", default_value=5, type=int
)

Config.add_plugin_config(
    "group_manager",
    "DEFAULT_GROUP_BOT_STATUS",
    True,
    help_="默认进群总开关状态",
    default_value=True,
    type=bool,
)


def init_group(func: Callable):
    """
    说明:
        初始化群数据
    参数:
        :param func: func
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        if arg_list := list(filter(lambda x: is_number(x), args[1:])):
            group_id = str(arg_list[0])
            if self is not None and group_id and not self._data.group_manager.get(group_id):
                self._data.group_manager[group_id] = BaseGroup()
                self.save()
        return func(*args, **kwargs)

    return wrapper


def init_task(func: Callable):
    """
    说明:
        初始化群被动
    参数:
        :param func: func
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        group_id = str(args[1])
        task = args[2] if len(args) > 1 else None
        if (
            group_id
            and task
            and self._data.group_manager[group_id].group_task_status.get(task) is None
        ):
            for task in self._data.task:
                if (
                    self._data.group_manager[group_id].group_task_status.get(task)
                    is None
                ):
                    self._data.group_manager[group_id].group_task_status[
                        task
                    ] = Config.get_config("_task", f"DEFAULT_{task}", default=True)
            for task in list(self._data.group_manager[group_id].group_task_status):
                if task not in self._data.task:
                    del self._data.group_manager[group_id].group_task_status[task]
            self.save()
        return func(*args, **kwargs)

    return wrapper


class GroupManager(StaticData[BaseData]):
    """
    群权限 | 功能 | 总开关 | 聊天时间 管理器
    """

    def __init__(self, file: Path):
        super().__init__(file, False)
        self._data: BaseData = (
            BaseData.parse_file(file) if file.exists() else BaseData()
        )

    def get_data(self) -> BaseData:
        return copy.deepcopy(self._data)

    def block_plugin(
        self, module: str, group_id: Union[str, int], is_save: bool = True
    ):
        """
        说明:
            锁定插件
        参数:
            :param module: 功能模块名
            :param group_id: 群组，None时为超级用户禁用
            :param is_save: 是否保存文件
        """
        self._set_plugin_status(module, "block", group_id, is_save)

    def unblock_plugin(
        self, module: str, group_id: Union[str, int], is_save: bool = True
    ):
        """
        说明:
            解锁插件
        参数:
            :param module: 功能模块名
            :param group_id: 群组
            :param is_save: 是否保存文件
        """
        self._set_plugin_status(module, "unblock", group_id, is_save)

    def turn_on_group_bot_status(self, group_id: Union[str, int]):
        """
        说明:
            开启群bot开关
        参数:
            :param group_id: 群号
        """
        self._set_group_bot_status(group_id, True)

    def shutdown_group_bot_status(self, group_id: Union[str, int]):
        """
        说明:
            关闭群bot开关
        参数:
            :param group_id: 群号
        """
        self._set_group_bot_status(group_id, False)

    @init_group
    def check_group_bot_status(self, group_id: Union[str, int]) -> bool:
        """
        说明:
            检查群聊bot总开关状态
        参数:
            :param group_id: 说明
        """
        return self._data.group_manager[str(group_id)].status

    @init_group
    def set_group_level(self, group_id: Union[str, int], level: int):
        """
        说明:
            设置群权限
        参数:
            :param group_id: 群组
            :param level: 权限等级
        """
        self._data.group_manager[str(group_id)].level = level
        self.save()

    @init_group
    def get_plugin_status(self, module: str, group_id: Union[str, int]) -> bool:
        """
        说明:
            获取插件状态
        参数:
            :param module: 功能模块名
            :param group_id: 群组
        """
        return module not in self._data.group_manager[str(group_id)].close_plugins

    def get_plugin_super_status(self, module: str, group_id: Union[str, int]) -> bool:
        """
        说明:
            获取插件是否被超级用户关闭
        参数:
            :param module: 功能模块名
            :param group_id: 群组
        """
        return (
            f"{module}:super"
            not in self._data.group_manager[str(group_id)].close_plugins
        )

    @init_group
    def get_group_level(self, group_id: Union[str, int]) -> int:
        """
        说明:
            获取群等级
        参数:
            :param group_id: 群号
        """
        return self._data.group_manager[str(group_id)].level

    def check_group_is_white(self, group_id: Union[str, int]) -> bool:
        """
        说明:
            检测群聊是否在白名单
        参数:
            :param group_id: 群号
        """
        return str(group_id) in self._data.white_group

    def add_group_white_list(self, group_id: Union[str, int]):
        """
        说明:
            将群聊加入白名单
        参数:
            :param group_id: 群号
        """
        group_id = str(group_id)
        if group_id not in self._data.white_group:
            self._data.white_group.append(group_id)

    def delete_group_white_list(self, group_id: Union[str, int]):
        """
        说明:
            将群聊从白名单中删除
        参数:
            :param group_id: 群号
        """
        group_id = str(group_id)
        if group_id in self._data.white_group:
            self._data.white_group.remove(group_id)

    def get_group_white_list(self) -> List[str]:
        """
        说明:
            获取所有群白名单
        """
        return self._data.white_group

    def load_task(self):
        """
        说明:
            加载被动技能
        """
        for matcher in get_matchers(True):
            _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)  # type: ignore
            try:
                _module = _plugin.module
                plugin_task = _module.__getattribute__("__plugin_task__")
                for key in plugin_task.keys():
                    if key in self._data.task.keys():
                        raise ValueError(f"plugin_task：{key} 已存在！")
                    self._data.task[key] = plugin_task[key]
            except AttributeError:
                pass

    @init_group
    def delete_group(self, group_id: Union[str, int]):
        """
        说明:
            删除群配置
        参数:
            :param group_id: 群号
        """
        group_id = str(group_id)
        if group_id in self._data.white_group:
            self._data.white_group.remove(group_id)
            self.save()

    def open_group_task(self, group_id: Union[str, int], task: str):
        """
        说明:
            开启群被动技能
        参数:
            :param group_id: 群号
            :param task: 被动技能名称
        """
        self._set_group_group_task_status(group_id, task, True)

    def close_global_task(self, task: str):
        """
        说明:
            关闭全局被动技能
        参数:
            :param task: 被动技能名称
        """
        if task not in self._data.close_task:
            self._data.close_task.append(task)

    def open_global_task(self, task: str):
        """
        说明:
            开启全局被动技能
        参数:
            :param task: 被动技能名称
        """
        if task in self._data.close_task:
            self._data.close_task.remove(task)

    def close_group_task(self, group_id: Union[str, int], task: str):
        """
        说明:
            关闭群被动技能
        参数:
            :param group_id: 群号
            :param task: 被动技能名称
        """
        self._set_group_group_task_status(group_id, task, False)

    def check_task_status(self, task: str, group_id: Optional[str] = None) -> bool:
        """
        说明:
            检查该被动状态
        参数:
            :param task: 被动技能名称
            :param group_id: 群号
        """
        if group_id:
            return self.check_group_task_status(
                group_id, task
            ) and self.check_task_super_status(task)
        return self.check_task_super_status(task)

    @init_group
    @init_task
    def check_group_task_status(self, group_id: Union[str, int], task: str) -> bool:
        """
        说明:
            查看群被动技能状态
        参数:
            :param group_id: 群号
            :param task: 被动技能名称
        """
        return self._data.group_manager[str(group_id)].group_task_status.get(
            task, False
        )

    def check_task_super_status(self, task: str) -> bool:
        """
        说明:
            查看群被动技能状态（超级用户设置的状态）
        参数:
            :param task: 被动技能名称
        """
        return task not in self._data.close_task

    def get_task_data(self) -> Dict[str, str]:
        """
        说明:
            获取所有被动任务
        """
        return self._data.task

    @init_group
    @init_task
    def group_group_task_status(self, group_id: Union[str, int]) -> str:
        """
        说明:
            查看群被全部动技能状态
        参数:
            :param group_id: 群号
        """
        x = "[群被动技能]:\n"
        group_id = str(group_id)
        for key in self._data.group_manager[group_id].group_task_status.keys():
            x += f'{self._data.task[key]}：{"√" if self.check_group_task_status(group_id, key) else "×"}\n'
        return x[:-1]

    @init_group
    @init_task
    def _set_group_group_task_status(
        self, group_id: Union[str, int], task: str, status: bool
    ):
        """
        说明:
            管理群被动技能状态
        参数:
            :param group_id: 群号
            :param task: 被动技能
            :param status: 状态
        """
        self._data.group_manager[str(group_id)].group_task_status[task] = status
        self.save()

    @init_group
    def _set_plugin_status(
        self, module: str, status: str, group_id: Union[str, int], is_save: bool
    ):
        """
        说明:
            设置功能开关状态
        参数:
            :param module: 功能模块名
            :param status: 功能状态
            :param group_id: 群组
            :param is_save: 是否保存
        """
        group_id = str(group_id)
        if status == "block":
            if module not in self._data.group_manager[group_id].close_plugins:
                self._data.group_manager[group_id].close_plugins.append(module)
        else:
            if module in self._data.group_manager[group_id].close_plugins:
                self._data.group_manager[group_id].close_plugins.remove(module)
        if is_save:
            self.save()

    @init_group
    def _set_group_bot_status(self, group_id: Union[int, str], status: bool):
        """
        说明:
            设置群聊bot总开关
        参数:
            :param group_id: 群号
            :param status: 开关状态
        """
        self._data.group_manager[str(group_id)].status = status
        self.save()

    def reload(self):
        if self.file.exists():
            t = self._data.task
            self._data = BaseData.parse_file(self.file)
            self._data.task = t

    def save(self, path: Optional[Union[str, Path]] = None):
        """
        说明:
            保存文件
        参数:
            :param path: 路径文件
        """
        path = path or self.file
        if isinstance(path, str):
            path = Path(path)
        if path:
            dict_data = self._data.dict()
            del dict_data["task"]
            with open(path, "w", encoding="utf8") as f:
                json.dump(dict_data, f, ensure_ascii=False, indent=4)

    def get(self, key: str, default: Any = None) -> BaseGroup:
        return self._data.group_manager.get(key, default)

    def __setitem__(self, key, value):
        self._data.group_manager[key] = value

    def __getitem__(self, key) -> BaseGroup:
        return self._data.group_manager[key]
