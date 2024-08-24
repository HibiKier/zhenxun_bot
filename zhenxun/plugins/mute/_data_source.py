import time

import ujson as json
from pydantic import BaseModel

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import DATA_PATH

base_config = Config.get("mute_setting")


class GroupData(BaseModel):

    count: int
    """次数"""
    time: int
    """检测时长"""
    duration: int
    """禁言时长"""
    message_data: dict = {}
    """消息存储"""


class MuteManage:

    file = DATA_PATH / "group_mute_data.json"

    def __init__(self) -> None:
        self._group_data: dict[str, GroupData] = {}
        if self.file.exists():
            _data = json.load(open(self.file))
            for gid in _data:
                self._group_data[gid] = GroupData(
                    count=_data[gid]["count"],
                    time=_data[gid]["time"],
                    duration=_data[gid]["duration"],
                )

    def get_group_data(self, group_id: str) -> GroupData:
        """获取群组数据

        参数:
            group_id: 群组id

        返回:
            GroupData: GroupData
        """
        if group_id not in self._group_data:
            self._group_data[group_id] = GroupData(
                count=base_config.get("MUTE_DEFAULT_COUNT", 10) or 10,
                time=base_config.get("MUTE_DEFAULT_TIME", 7) or 7,
                duration=base_config.get("MUTE_DEFAULT_DURATION", 10) or 10,
            )
        return self._group_data[group_id]

    def reset(self, user_id: str, group_id: str):
        """重置用户检查次数

        参数:
            user_id: 用户id
            group_id: 群组id
        """
        if group_data := self._group_data.get(group_id):
            if user_id in group_data.message_data:
                group_data.message_data[user_id]["count"] = 0

    def save_data(self):
        """保存数据"""
        data = {}
        for gid in self._group_data:
            data[gid] = {
                "count": self._group_data[gid].count,
                "time": self._group_data[gid].time,
                "duration": self._group_data[gid].duration,
            }
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_message(self, user_id: str, group_id: str, message: str) -> int:
        """添加消息

        参数:
            user_id: 用户id
            group_id: 群组id
            message: 消息内容

        返回:
            int: 禁言时长
        """
        if group_id not in self._group_data:
            self._group_data[group_id] = GroupData(
                count=base_config.get("MUTE_DEFAULT_COUNT"),
                time=base_config.get("MUTE_DEFAULT_TIME"),
                duration=base_config.get("MUTE_DEFAULT_DURATION"),
            )
        group_data = self._group_data[group_id]
        if group_data.duration == 0:
            return 0
        message_data = group_data.message_data
        if not message_data.get(user_id):
            message_data[user_id] = {
                "time": time.time(),
                "count": 1,
                "message": message,
            }
        else:
            if message.find(message_data[user_id]["message"]) != -1:
                message_data[user_id]["count"] += 1
            else:
                message_data[user_id]["time"] = time.time()
                message_data[user_id]["count"] = 1
            message_data[user_id]["message"] = message
            if time.time() - message_data[user_id]["time"] > group_data.time:
                message_data[user_id]["time"] = time.time()
                message_data[user_id]["count"] = 1
            if (
                message_data[user_id]["count"] > group_data.count
                and time.time() - message_data[user_id]["time"] < group_data.time
            ):
                return group_data.duration
        return 0


mute_manage = MuteManage()
