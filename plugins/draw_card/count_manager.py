from typing import Optional
from pydantic import BaseModel
import time


class BaseUserCount(BaseModel):
    count: int = 1  # 当前抽卡次数
    time_: int = time.time()  # 抽卡时间，当超过一定时间时将重置抽卡次数
    timeout: int = 60  # 超时时间60秒


class DrawCountManager:
    """
    抽卡统计保底
    """

    def __init__(
        self, game_draw_count_rule: tuple, star2name: tuple, max_draw_count: int
    ):
        """
        初始化保底统计

        例如：DrawCountManager((10, 90, 180), ("4", "5", "5"))

        抽卡保底需要的次数和返回的对应名称，例如星级等

        :param game_draw_count_rule：抽卡规则
        :param star2name：星级对应的名称
        :param max_draw_count：最大累计抽卡次数，当下次单次抽卡超过该次数时将会清空数据

        """
        # 只有保底
        self._data = {}
        self._guarantee_tuple = game_draw_count_rule
        self._star2name = star2name
        self._max_draw_count = max_draw_count

    def increase(self, key: int, value: int = 1):
        """
        用户抽卡次数加1
        """
        if self._data.get(key) is None:
            self._data[key] = BaseUserCount()
        else:
            self._data[key].count += 1

    def get_max_guarantee(self):
        """
        获取最大保底抽卡次数
        """
        return self._guarantee_tuple[-1]

    def get_user_count(self, key: int) -> int:
        """
        获取当前抽卡次数
        """
        return self._data[key].count

    def update_time(self, key: int):
        """
        更新抽卡时间
        """
        self._data[key].time_ = time.time()

    def reset(self, key: int):
        """
        清空记录
        """
        del self._data[key]


class GenshinCountManager(DrawCountManager):
    class UserCount(BaseUserCount):
        five_index: int = 0  # 获取五星时的抽卡次数
        four_index: int = 0  # 获取四星时的抽卡次数
        is_up: bool = False  # 下次五星是否必定为up

    def increase(self, key: int, value: int = 1):
        """
        用户抽卡次数加1
        """
        if self._data.get(key) is None:
            self._data[key] = self.UserCount()
        else:
            self._data[key].count += 1

    def set_is_up(self, key: int, value: bool):
        """
        设置下次是否必定up
        """
        self._data[key].is_up = value

    def is_up(self, key: int) -> bool:
        """
        判断该次保底是否必定为up
        """
        return self._data[key].is_up

    def get_user_five_index(self, key: int) -> int:
        """
        获取用户上次获取五星的次数
        """
        return self._data[key].five_index

    def get_user_four_index(self, key: int) -> int:
        """
        获取用户上次获取四星的次数
        """
        return self._data[key].four_index

    def mark_five_index(self, key: int):
        """
        标记用户该次次数为五星
        """
        self._data[key].five_index = self._data[key].count

    def mark_four_index(self, key: int):
        """
        标记用户该次次数为四星
        """
        self._data[key].four_index = self._data[key].count

    def check_timeout(self, key: int):
        """
        检查用户距离上次抽卡是否超时
        """
        if key in self._data.keys() and self._is_timeout(key):
            del self._data[key]

    def check_count(self, key: int, count: int):
        """
        检查用户该次抽卡次数累计是否超过最大限制次数
        """
        if (
            key in self._data.keys()
            and self._data[key].count + count > self._max_draw_count
        ):
            del self._data[key]

    def _is_timeout(self, key: int) -> bool:
        return time.time() - self._data[key].time_ > self._data[key].timeout

    def get_user_guarantee_count(self, key: int) -> int:
        return (
            self.get_max_guarantee()
            - (
                (
                    self._data[key].count % self.get_max_guarantee()
                    if self._data[key].count > 0
                    else 0
                )
                - self._data[key].five_index
            )
        ) % self.get_max_guarantee() or self.get_max_guarantee()

    def check(self, key: int) -> Optional[int]:
        """
        是否保底
        """
        # print(self._data)
        user: GenshinCountManager.UserCount = self._data[key]
        if user.count - user.five_index == 90:
            user.five_index = 90
            return 5
        if user.count - user.four_index == 10:
            user.four_index = user.count
            return 4
        return None

