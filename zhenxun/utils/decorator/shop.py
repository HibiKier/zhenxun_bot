from typing import Callable, Union, Tuple, Optional
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.plugin import require


class ShopRegister(dict):
    def __init__(self, *args, **kwargs):
        super(ShopRegister, self).__init__(*args, **kwargs)
        self._data = {}
        self._flag = True

    def before_handle(self, name: Union[str, Tuple[str, ...]], load_status: bool = True):
        """
        说明:
            使用前检查方法
        参数:
            :param name: 道具名称
            :param load_status: 加载状态
        """
        def register_before_handle(name_list: Tuple[str, ...], func: Callable):
            if load_status:
                for name_ in name_list:
                    if not self._data[name_]:
                        self._data[name_] = {}
                    if not self._data[name_].get('before_handle'):
                        self._data[name_]['before_handle'] = []
                    self._data[name]['before_handle'].append(func)
        _name = (name,) if isinstance(name, str) else name
        return lambda func: register_before_handle(_name, func)

    def after_handle(self, name: Union[str, Tuple[str, ...]], load_status: bool = True):
        """
        说明:
            使用后执行方法
        参数:
            :param name: 道具名称
            :param load_status: 加载状态
        """
        def register_after_handle(name_list: Tuple[str, ...], func: Callable):
            if load_status:
                for name_ in name_list:
                    if not self._data[name_]:
                        self._data[name_] = {}
                    if not self._data[name_].get('after_handle'):
                        self._data[name_]['after_handle'] = []
                    self._data[name_]['after_handle'].append(func)
        _name = (name,) if isinstance(name, str) else name
        return lambda func: register_after_handle(_name, func)

    def register(
        self,
        name: Tuple[str, ...],
        price: Tuple[float, ...],
        des: Tuple[str, ...],
        discount: Tuple[float, ...],
        limit_time: Tuple[int, ...],
        load_status: Tuple[bool, ...],
        daily_limit: Tuple[int, ...],
        is_passive: Tuple[bool, ...],
        icon: Tuple[str, ...],
        **kwargs,
    ):
        def add_register_item(func: Callable):
            if name in self._data.keys():
                raise ValueError("该商品已注册，请替换其他名称！")
            for n, p, d, dd, l, s, dl, pa, i in zip(
                name, price, des, discount, limit_time, load_status, daily_limit, is_passive, icon
            ):
                if s:
                    _temp_kwargs = {}
                    for key, value in kwargs.items():
                        if key.startswith(f"{n}_"):
                            _temp_kwargs[key.split("_", maxsplit=1)[-1]] = value
                        else:
                            _temp_kwargs[key] = value
                    temp = self._data.get(n, {})
                    temp.update({
                        "price": p,
                        "des": d,
                        "discount": dd,
                        "limit_time": l,
                        "daily_limit": dl,
                        "icon": i,
                        "is_passive": pa,
                        "func": func,
                        "kwargs": _temp_kwargs,
                    })
                    self._data[n] = temp
            return func

        return lambda func: add_register_item(func)

    async def load_register(self):
        require("use")
        require("shop_handle")
        from basic_plugins.shop.use.data_source import register_use, func_manager
        from basic_plugins.shop.shop_handle.data_source import register_goods
        # 统一进行注册
        if self._flag:
            # 只进行一次注册
            self._flag = False
            for name in self._data.keys():
                await register_goods(
                    name,
                    self._data[name]["price"],
                    self._data[name]["des"],
                    self._data[name]["discount"],
                    self._data[name]["limit_time"],
                    self._data[name]["daily_limit"],
                    self._data[name]["is_passive"],
                    self._data[name]["icon"],
                )
                register_use(
                    name, self._data[name]["func"], **self._data[name]["kwargs"]
                )
                func_manager.register_use_before_handle(name, self._data[name].get('before_handle', []))
                func_manager.register_use_after_handle(name, self._data[name].get('after_handle', []))

    def __call__(
        self,
        name: Union[str, Tuple[str, ...]],                  # 名称
        price: Union[float, Tuple[float, ...]],             # 价格
        des: Union[str, Tuple[str, ...]],                   # 简介
        discount: Union[float, Tuple[float, ...]] = 1,      # 折扣
        limit_time: Union[int, Tuple[int, ...]] = 0,        # 限时
        load_status: Union[bool, Tuple[bool, ...]] = True,  # 加载状态
        daily_limit: Union[int, Tuple[int, ...]] = 0,       # 每日限购
        is_passive: Union[bool, Tuple[bool, ...]] = False,  # 被动道具（无法被'使用道具'命令消耗）
        icon: Union[str, Tuple[str, ...]] = False,          # 图标
        **kwargs,
    ):
        _tuple_list = []
        _current_len = -1
        for x in [name, price, des, discount, limit_time, load_status]:
            if isinstance(x, tuple):
                if _current_len == -1:
                    _current_len = len(x)
                if _current_len != len(x):
                    raise ValueError(
                        f"注册商品 {name} 中 name，price，des，discount，limit_time，load_status，daily_limit 数量不符！"
                    )
        _current_len = _current_len if _current_len > -1 else 1
        _name = self.__get(name, _current_len)
        _price = self.__get(price, _current_len)
        _discount = self.__get(discount, _current_len)
        _limit_time = self.__get(limit_time, _current_len)
        _des = self.__get(des, _current_len)
        _load_status = self.__get(load_status, _current_len)
        _daily_limit = self.__get(daily_limit, _current_len)
        _is_passive = self.__get(is_passive, _current_len)
        _icon = self.__get(icon, _current_len)
        return self.register(
            _name,
            _price,
            _des,
            _discount,
            _limit_time,
            _load_status,
            _daily_limit,
            _is_passive,
            _icon,
            **kwargs,
        )

    def __get(self, value, _current_len):
        return value if isinstance(value, tuple) else tuple([value for _ in range(_current_len)])

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __str__(self):
        return str(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()


class NotMeetUseConditionsException(Exception):

    """
    不满足条件异常类
    """

    def __init__(self, info: Optional[Union[str, MessageSegment, Message]]):
        super().__init__(self)
        self._info = info

    def get_info(self):
        return self._info


shop_register = ShopRegister()
