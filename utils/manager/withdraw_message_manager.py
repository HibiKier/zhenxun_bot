from typing import Tuple, Union, Dict


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
            message_data = (message_data[0]['message_id'], message_data[1])
        self.data.append(message_data)

    def remove(self, message_data: Tuple[int, int]):
        """
        说明：
            删除一个数据
        参数：
            :param message_data: 消息id和时间
        """
        self.data.remove(message_data)

