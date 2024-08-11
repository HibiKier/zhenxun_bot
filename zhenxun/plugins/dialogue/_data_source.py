from typing import Dict

from nonebot_plugin_alconna import UniMsg
from pydantic import BaseModel


class DialogueData(BaseModel):

    name: str
    """用户名称"""
    user_id: str
    """用户id"""
    group_id: str | None
    """群组id"""
    group_name: str | None
    """群组名称"""
    message: UniMsg
    """UniMsg"""
    platform: str | None
    """平台"""


class DialogueManage:

    _data: Dict[int, DialogueData] = {}
    _index = 0

    @classmethod
    def add(
        cls,
        name: str,
        uid: str,
        gid: str | None,
        group_name: str | None,
        message: UniMsg,
        platform: str | None,
    ):
        cls._data[cls._index] = DialogueData(
            name=name,
            user_id=uid,
            group_id=gid,
            group_name=group_name,
            message=message,
            platform=platform,
        )
        cls._index += 1

    @classmethod
    def remove(cls, index: int):
        if index in cls._data:
            del cls._data[index]

    @classmethod
    def get(cls, k: int):
        return cls._data.get(k)
