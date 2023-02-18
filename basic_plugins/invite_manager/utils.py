import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class PrivateRequest:

    """
    好友请求
    """

    user_id: int
    time: float = time.time()


@dataclass
class GroupRequest:

    """
    群聊请求
    """

    user_id: int
    group_id: int
    time: float = time.time()


class RequestTimeManage:

    """
    过滤五分钟以内的重复请求
    """

    def __init__(self):

        self._group: Dict[str, GroupRequest] = {}
        self._user: Dict[int, PrivateRequest] = {}

    def add_user_request(self, user_id: int) -> bool:
        """
        添加请求时间

        Args:
            user_id (int): 用户id

        Returns:
            bool: 是否满足时间
        """
        if user := self._user.get(user_id):
            if time.time() - user.time < 60 * 5:
                return False
        self._user[user_id] = PrivateRequest(user_id)
        return True

    def add_group_request(self, user_id: int, group_id: int) -> bool:
        """
        添加请求时间

        Args:
            user_id (int): 用户id
            group_id (int): 邀请群聊

        Returns:
            bool: 是否满足时间
        """
        key = f"{user_id}:{group_id}"
        if group := self._group.get(key):
            if time.time() - group.time < 60 * 5:
                return False
        self._group[key] = GroupRequest(user_id=user_id, group_id=group_id)
        return True

    def clear(self):
        """
        清理过期五分钟请求
        """
        now = time.time()
        for user_id in self._user:
            if now - self._user[user_id].time < 60 * 5:
                del self._user[user_id]
        for key in self._group:
            if now - self._group[key].time < 60 * 5:
                del self._group[key]


time_manager = RequestTimeManage()
