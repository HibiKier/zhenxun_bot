from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from utils.manager import plugins2block_manager, StaticData
import time

ignore_rst_module = ["ai", "poke", "dialogue"]

other_limit_plugins = ["poke"]


class StatusMessageManager(StaticData):

    def __init__(self):
        super().__init__(None)

    def add(self, id_: int):
        self._data[id_] = time.time()

    def delete(self, id_: int):
        if self._data.get(id_):
            del self._data[id_]

    def check(self, id_: int, t: int = 30) -> bool:
        if self._data.get(id_):
            if time.time() - self._data[id_] > t:
                del self._data[id_]
                return True
            return False
        return True


status_message_manager = StatusMessageManager()


def set_block_limit_false(event, module):
    """
    设置用户block为false
    :param event: event
    :param module: 插件模块
    """
    if plugins2block_manager.check_plugin_block_status(module):
        plugin_block_data = plugins2block_manager.get_plugin_block_data(module)
        check_type = plugin_block_data["check_type"]
        limit_type = plugin_block_data["limit_type"]
        if not (
            (isinstance(event, GroupMessageEvent) and check_type == "private")
            or (isinstance(event, PrivateMessageEvent) and check_type == "group")
        ):
            block_type_ = event.user_id
            if limit_type == "group" and isinstance(event, GroupMessageEvent):
                block_type_ = event.group_id
            plugins2block_manager.set_false(block_type_, module)

