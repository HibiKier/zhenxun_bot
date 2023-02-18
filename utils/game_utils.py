from typing import Optional, Dict, Union

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from pydantic import BaseModel
import time


class GameEntry(BaseModel):
    game_name: str
    module: str
    default_msg: str
    msg_data: Dict[int, Union[str, Message, MessageSegment]]
    timeout: int  # 超时时限
    anti_concurrency: bool  # 是否阻断


class GroupGameStatus(BaseModel):
    game: GameEntry
    status: int
    time: time.time()  # 创建时间


class GameManager:
    def __init__(self):
        self._data = {}
        self._status = {}

    def add_game(
        self,
        game_name: str,
        module: str,
        timeout: int,
        default_msg: Optional[str] = "游戏还未结束！",
        msg_data: Dict[int, Union[str, Message, MessageSegment]] = None,
        anti_concurrency: bool = True,
        **kwargs,
    ):
        """
        参数:
            将游戏添加到游戏管理器
        说明:
            :param game_name: 游戏名称
            :param module: 模块名
            :param timeout: 超时时长
            :param default_msg: 默认回复消息
            :param msg_data: 不同状态回复的消息
            :param anti_concurrency: 是否阻断反并发
        """
        self._data[module] = GameEntry(
            game_name=game_name,
            module=module,
            timeout=timeout,
            default_msg=default_msg,
            msg_data=msg_data or {},
            anti_concurrency=anti_concurrency,
            **kwargs,
        )

    def start(self, group_id: int, module: str):
        """
        说明:
            游戏开始标记
        参数:
            :param group_id: 群号
            :param module: 模块名
        """
        if not self._status.get(group_id):
            self._status[group_id] = []
        if module not in [x.game.module for x in self._status[module]]:
            self._status[group_id].append(
                GroupGameStatus(game=self._data[module], status=0)
            )

    def end(self, group_id: int, module: str):
        """
        说明:
            游戏结束标记
        参数:
            :param group_id: 群号
            :param module: 模块名
        """
        if self._status.get(group_id) and module in [
            x.game.module for x in self._status[group_id]
        ]:
            for x in self._status[group_id]:
                if self._status[group_id][x].game.module == module:
                    self._status[group_id].remove(x)
                    break

    def set_status(self, group_id: int, module: str, status: int):
        """
        说明:
            设置游戏状态，根据状态发送不同的提示消息 msg_data
        参数:
            :param group_id: 群号
            :param module: 模块名
            :param status: 状态码
        """
        if self._status.get(group_id) and module in [
            x.game.module for x in self._status[group_id]
        ]:
            [x.game.module for x in self._status[group_id] if x.game.module == module][
                0
            ].status = status

    def check(self, group_id, module: str) -> Optional[str]:
        """
        说明:
            检查群游戏当前状态并返回提示语句
        参数:
            :param group_id: 群号
            :param module: 模块名
        """
        if module in self._data and self._status.get(group_id):
            for x in self._status[group_id]:
                if x.game.anti_concurrency:
                    return f"{x.game.game_name} 还未结束，请等待 {x.game.game_name} 游戏结束！"
        if self._status.get(group_id) and module in [
            x.game.module for x in self._status[group_id]
        ]:
            group_game_status = [
                x.game.module for x in self._status[group_id] if x.game.module == module
            ][0]
            if time.time() - group_game_status.time > group_game_status.game.timeout:
                # 超时结束
                self.end(group_id, module)
            else:
                return (
                    group_game_status.game.msg_data.get(group_game_status.status)
                    or group_game_status.game.default_msg
                )


game_manager = GameManager()


class Game:
    """
    反并发，游戏重复开始
    """
    def __init__(
        self,
        game_name: str,
        module: str,
        timeout: int = 60,
        default_msg: Optional[str] = None,
        msg_data: Dict[int, Union[str, Message, MessageSegment]] = None,
        anti_concurrency: bool = True,
    ):
        """
        参数:
            将游戏添加到游戏管理器
        说明:
            :param game_name: 游戏名称
            :param module: 模块名
            :param timeout: 超时时长
            :param default_msg: 默认回复消息
            :param msg_data: 不同状态回复的消息
            :param anti_concurrency: 是否阻断反并发
        """
        self.module = module
        game_manager.add_game(
            game_name, module, timeout, default_msg, msg_data, anti_concurrency
        )

    def start(self, group_id: int):
        """
        说明:
            游戏开始标记
        参数:
            :param group_id: 群号
        """
        game_manager.start(group_id, self.module)

    def end(self, group_id: int):
        """
        说明:
            游戏结束标记
        参数:
            :param group_id: 群号
        """
        game_manager.end(group_id, self.module)

    def set_status(self, group_id: int, status: int):
        """
        说明:
            设置游戏状态，根据状态发送不同的提示消息 msg_data
        参数:
            :param group_id: 群号
            :param status: 状态码
        """
        game_manager.set_status(group_id, self.module, status)
