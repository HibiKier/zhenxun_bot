from typing import Optional, Union


class DrawCountManager:
    """
    抽卡统计保底
    """

    def __init__(self, game_draw_count_rule: tuple, star2name: tuple):
        """
        初始化保底统计

        例如：DrawCountManager((10, 90, 180), ("4", "5", "5"))

        抽卡保底需要的次数和返回的对应名称，例如星级等

        """
        # 只有保底
        self._data = {}
        self._guarantee_tuple = game_draw_count_rule
        self._star2name = star2name

    def increase(self, key: int, value: int = 1):
        """
        用户抽卡次数加1
        """
        if self._data.get(key) is None:
            self._data[key] = {
                "count": value,
            }
            for x in range(len(self._guarantee_tuple)):
                self._data[key][f"count_{x}"] = 0
        else:
            self._data[key][f"count"] += value
            if self._data[key][f"count"] > self._guarantee_tuple[-1]:
                self._data[key][f"count"] = self._data[key][f"count"] % self._guarantee_tuple[-1]

    def reset(self, key: int):
        """
        清空记录
        """
        del self._data[key]

    def set_count(self, key: int, type_: int, count: int):
        if self._data.get(key):
            self._data[key][f"count_{type_}"] = count

    def check(self, key: int, *args) -> Optional[Union[str, int]]:
        """
        是否保底
        """
        pass

    def get_user_count(self, key: int, type_: Optional[int] = None) -> int:
        """
        获取用户当前抽卡次数
        """
        if self._data.get(key):
            if type_ is None:
                return self._data[key]["count"]
            return self._data[key][f"count_{type_}"]
        return 0

    def record_count(self, key: int, type_: int):
        """
        抽出对应星级后记录当前次数
        """
        if self._data.get(key):
            self._data[key][f"count_{type_}"] = self._data[key]["count"]


class GenshinCountManager(DrawCountManager):

    def increase(self, key: int, value: int = 1):
        """
        用户抽卡次数加1
        """
        if self._data.get(key) is None:
            self._data[key] = {
                "is_up": False,
                "count": value,
            }
            for x in range(len(self._guarantee_tuple)):
                self._data[key][f"count_{x}"] = 0
        else:
            self._data[key][f"count"] += value
            if self._data[key][f"count"] > self._guarantee_tuple[-1]:
                self._data[key][f"count"] = self._data[key][f"count"] % 180

    def set_is_up(self, key: int, value: bool):
        if self._data.get(key):
            self._data[key]["is_up"] = value

    def is_up(self, key: int) -> bool:
        if self._data.get(key):
            return self._data[key]["is_up"]
        return False

    def check(self, key: int, *args) -> Optional[Union[str, int]]:
        """
        是否保底
        """
        # print(self._data)
        if self._data.get(key):
            for i in [1, 0]:
                count = self._data[key]["count"]
                if count - self._data[key][f"count_{i}"] == self._guarantee_tuple[i]:
                    if i in [2, 1]:
                        # print("clean four count")
                        self._data[key][f"count_0"] = self._data[key]['count']
                    self._data[key][f"count_{i}"] = self._data[key]['count']
                    return self._star2name[i]
        return None
