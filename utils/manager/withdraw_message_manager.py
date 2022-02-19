from typing import Tuple, Union, Dict
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent


class WithdrawMessageManager:
    def __init__(self):
        self.data = []

    def append(self, message_data: Tuple[Union[int, Dict[str, int]], int]):
        """
        说明：
            添加一个撤回消息id和时间
        参数：
            :param message_data: 撤回消息id和时间
        """
        if isinstance(message_data[0], dict):
            message_data = (message_data[0]["message_id"], message_data[1])
        self.data.append(message_data)

    def remove(self, message_data: Tuple[int, int]):
        """
        说明：
            删除一个数据
        参数：
            :param message_data: 消息id和时间
        """
        self.data.remove(message_data)

    def withdraw_message(
        self, event: MessageEvent, id_: Union[int, Dict[str, int]], conditions: Tuple[int, int]
    ):
        """
        便捷判断消息撤回
        :param event: event
        :param id_: 消息id 或 send 返回的字典
        :param conditions: 判断条件
        """
        if conditions[0]:
            if (
                (conditions[1] == 0 and isinstance(event, PrivateMessageEvent))
                or (conditions[1] == 1 and isinstance(event, GroupMessageEvent))
                or conditions[1] == 2
            ):
                self.append((id_, conditions[0]))
