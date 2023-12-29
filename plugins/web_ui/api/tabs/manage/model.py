from typing import Dict, List, Literal, Optional, Union

from matplotlib.dates import FR
from nonebot.adapters.onebot.v11 import Bot
from pydantic import BaseModel


class Group(BaseModel):
    """
    群组信息
    """

    group_id: Union[str, int]
    """群组id"""
    group_name: str
    """群组名称"""
    member_count: int
    """成员人数"""
    max_member_count: int
    """群组最大人数"""


class Task(BaseModel):
    """
    被动技能
    """

    name: str
    """被动名称"""
    nameZh: str
    """被动中文名称"""
    status: bool
    """状态"""


class GroupResult(BaseModel):
    """
    群组返回数据
    """

    group: Group
    """Group"""
    level: int
    """群等级"""
    status: bool
    """状态"""
    close_plugins: List[str]
    """关闭的插件"""
    task: List[Task]
    """被动列表"""


class Friend(BaseModel):
    """
    好友数据
    """

    user_id: Union[str, int]
    """用户id"""
    nickname: str = ""
    """昵称"""
    remark: str = ""
    """备注"""


class UpdateGroup(BaseModel):
    """
    更新群组信息
    """

    group_id: str
    """群号"""
    status: bool
    """状态"""
    level: int
    """群权限"""
    task_status: Dict[str, bool]
    """被动状态"""


class FriendRequestResult(BaseModel):
    """
    好友/群组请求管理
    """

    bot_id: Union[str, int]
    """bot_id"""
    oid: str
    """排序"""
    id: int
    """id"""
    flag: str
    """flag"""
    nickname: Optional[str]
    """昵称"""
    level: Optional[int]
    """等级"""
    sex: Optional[str]
    """性别"""
    age: Optional[int]
    """年龄"""
    from_: Optional[str]
    """来自"""
    comment: Optional[str]
    """备注信息"""


class GroupRequestResult(FriendRequestResult):
    """
    群聊邀请请求
    """

    invite_group: Union[int, str]
    """邀请群聊"""
    group_name: Optional[str]
    """群聊名称"""


class HandleRequest(BaseModel):
    """
    操作请求接收数据
    """

    bot_id: str
    """bot_id"""
    id: int
    """id"""
    request_type: Literal["private", "group"]
    """类型"""


class LeaveGroup(BaseModel):
    """
    退出群聊
    """

    bot_id: str
    """bot_id"""
    group_id: str
    """群聊id"""


class DeleteFriend(BaseModel):
    """
    删除好友
    """

    bot_id: str
    """bot_id"""
    user_id: str
    """用户id"""
