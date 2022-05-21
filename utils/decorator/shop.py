from typing import Callable, Union, Tuple
from nonebot.plugin import require


use = require("use")
shop = require("shop_handle")


class ShopRegister(dict):
    def __init__(self, *args, **kwargs):
        super(ShopRegister, self).__init__(*args, **kwargs)
        self._data = {}
        self._flag = True

    def register(
        self,
        name: Tuple[str, ...],
        price: Tuple[float, ...],
        des: Tuple[str, ...],
        discount: Tuple[float, ...],
        limit_time: Tuple[int, ...],
        load_status: Tuple[bool, ...],
        **kwargs,
    ):
        def add_register_item(func: Callable):
            if name in self._data.keys():
                raise ValueError("该商品已注册，请替换其他名称！")
            for n, p, d, dd, l, s in zip(name, price, des, discount, limit_time, load_status):
                if s:
                    _temp_kwargs = {}
                    for key, value in kwargs.items():
                        if key.startswith(f"{n}_"):
                            _temp_kwargs[key.split("_", maxsplit=1)[-1]] = value
                    self._data[n] = {
                        "price": p,
                        "des": d,
                        "discount": dd,
                        "limit_time": l,
                        "func": func,
                        "kwargs": _temp_kwargs,
                    }
            return func

        return lambda func: add_register_item(func)

    async def load_register(self):
        # 统一进行注册
        if self._flag:
            # 只进行一次注册
            self._flag = False
            for name in self._data.keys():
                await shop.register_goods(
                    name, self._data[name]["price"], self._data[name]["des"], self._data[name]["discount"], self._data[name]["limit_time"]
                )
                use.register_use(
                    name, self._data[name]["func"], **self._data[name]["kwargs"]
                )

    def __call__(
        self,
        name: Union[str, Tuple[str, ...]],
        price: Union[float, Tuple[float, ...]],
        des: Union[str, Tuple[str, ...]],
        discount: Union[float, Tuple[float, ...]] = 1,
        limit_time: Union[int, Tuple[int, ...]] = 0,
        load_status: Union[bool, Tuple[bool, ...]] = True,
        **kwargs,
    ):
        _tuple_list = []
        _current_len = -1
        for x in [name, price, des, discount, limit_time, load_status]:
            if isinstance(x, tuple):
                if _current_len == -1:
                    _current_len = len(x)
                if _current_len != len(x):
                    raise ValueError(f"注册商品 {name} 中 name，price，des，discount，limit_time，load_status 数量不符！")
        _current_len = _current_len if _current_len > -1 else 1
        _name = name if isinstance(name, tuple) else (name,)
        _price = (
            price
            if isinstance(price, tuple)
            else tuple([price for _ in range(_current_len)])
        )
        _discount = (
            discount
            if isinstance(discount, tuple)
            else tuple([discount for _ in range(_current_len)])
        )
        _limit_time = (
            limit_time
            if isinstance(limit_time, tuple)
            else tuple([limit_time for _ in range(_current_len)])
        )
        _des = (
            des if isinstance(des, tuple) else tuple([des for _ in range(_current_len)])
        )
        _load_status = (
            load_status
            if isinstance(load_status, tuple)
            else tuple([load_status for _ in range(_current_len)])
        )
        return self.register(_name, _price, _des, _discount, _limit_time, _load_status, **kwargs)

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


shop_register = ShopRegister()
