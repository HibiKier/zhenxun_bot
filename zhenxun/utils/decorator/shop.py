from collections.abc import Callable

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.plugin import require
from pydantic import BaseModel

from zhenxun.models.goods_info import GoodsInfo


class Goods(BaseModel):
    before_handle: list[Callable] = []
    after_handle: list[Callable] = []
    price: int
    des: str = ""
    discount: float
    limit_time: int
    daily_limit: int
    icon: str | None = None
    is_passive: bool
    partition: str | None
    func: Callable
    kwargs: dict[str, str] = {}
    send_success_msg: bool
    max_num_limit: int


class ShopRegister(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data: dict[str, Goods] = {}
        self._flag = True

    def before_handle(self, name: str | tuple[str, ...], load_status: bool = True):
        """使用前检查方法

        参数:
            name: 道具名称
            load_status: 加载状态
        """

        def register_before_handle(name_list: tuple[str, ...], func: Callable):
            if load_status:
                for name_ in name_list:
                    if self._data.get(name_):
                        self._data[name_].before_handle.append(func)

        _name = (name,) if isinstance(name, str) else name
        return lambda func: register_before_handle(_name, func)

    def after_handle(self, name: str | tuple[str, ...], load_status: bool = True):
        """使用后执行方法

        参数:
            name: 道具名称
            load_status: 加载状态
        """

        def register_after_handle(name_list: tuple[str, ...], func: Callable):
            if load_status:
                for name_ in name_list:
                    if self._data.get(name_):
                        self._data[name_].after_handle.append(func)

        _name = (name,) if isinstance(name, str) else name
        return lambda func: register_after_handle(_name, func)

    def register(
        self,
        name: tuple[str, ...],
        price: tuple[float, ...],
        des: tuple[str, ...],
        discount: tuple[float, ...],
        limit_time: tuple[int, ...],
        load_status: tuple[bool, ...],
        daily_limit: tuple[int, ...],
        is_passive: tuple[bool, ...],
        partition: tuple[str, ...],
        icon: tuple[str, ...],
        send_success_msg: tuple[bool, ...],
        max_num_limit: tuple[int, ...],
        **kwargs,
    ):
        """注册商品

        参数:
            name: 商品名称
            price: 价格
            des: 简介
            discount: 折扣
            limit_time: 售卖限时时间
            load_status: 是否加载
            daily_limit: 每日限购
            is_passive: 是否被动道具
            partition: 分区名称
            icon: 图标
            send_success_msg: 成功时发送消息
            max_num_limit: 单次最大使用次数
        """

        def add_register_item(func: Callable):
            if name in self._data.keys():
                raise ValueError("该商品已注册，请替换其他名称！")
            for n, p, d, dd, lmt, s, dl, pa, par, i, ssm, mnl in zip(
                name,
                price,
                des,
                discount,
                limit_time,
                load_status,
                daily_limit,
                is_passive,
                partition,
                icon,
                send_success_msg,
                max_num_limit,
            ):
                if s:
                    _temp_kwargs = {}
                    for key, value in kwargs.items():
                        if key.startswith(f"{n}_"):
                            _temp_kwargs[key.split("_", maxsplit=1)[-1]] = value
                        else:
                            _temp_kwargs[key] = value
                    goods = self._data.get(n) or Goods(
                        price=p,
                        des=d,
                        discount=dd,
                        limit_time=lmt,
                        daily_limit=dl,
                        is_passive=pa,
                        partition=par,
                        func=func,
                        send_success_msg=ssm,
                        max_num_limit=mnl,
                    )
                    goods.price = p
                    goods.des = d
                    goods.discount = dd
                    goods.limit_time = lmt
                    goods.daily_limit = dl
                    goods.icon = i
                    goods.is_passive = pa
                    goods.partition = par
                    goods.func = func
                    goods.kwargs = _temp_kwargs
                    goods.send_success_msg = ssm
                    goods.max_num_limit = mnl
                    self._data[n] = goods
            return func

        return lambda func: add_register_item(func)

    async def load_register(self):
        require("shop")
        from zhenxun.builtin_plugins.shop._data_source import ShopManage

        # 统一进行注册
        if self._flag:
            # 只进行一次注册
            self._flag = False
            for name in self._data.keys():
                if goods := self._data.get(name):
                    uuid = await GoodsInfo.add_goods(
                        name,
                        goods.price,
                        goods.des,
                        goods.discount,
                        goods.limit_time,
                        goods.daily_limit,
                        goods.is_passive,
                        goods.partition,
                        goods.icon,
                    )
                    if uuid:
                        await ShopManage.register_use(
                            name,
                            uuid,
                            goods.func,
                            goods.send_success_msg,
                            goods.max_num_limit,
                            goods.before_handle,
                            goods.after_handle,
                            **self._data[name].kwargs,
                        )

    def __call__(
        self,
        name: str | tuple[str, ...],
        price: float | tuple[float, ...],
        des: str | tuple[str, ...],
        discount: float | tuple[float, ...] = 1,
        limit_time: int | tuple[int, ...] = 0,
        load_status: bool | tuple[bool, ...] = True,
        daily_limit: int | tuple[int, ...] = 0,
        is_passive: bool | tuple[bool, ...] = False,
        partition: str | tuple[str, ...] | None = None,
        icon: str | tuple[str, ...] = "",
        send_success_msg: bool | tuple[bool, ...] = True,
        max_num_limit: int | tuple[int, ...] = 1,
        **kwargs,
    ):
        """注册商品

        参数:
            name: 商品名称
            price: 价格
            des: 简介
            discount: 折扣
            limit_time: 售卖限时时间
            load_status: 是否加载
            daily_limit: 每日限购
            is_passive: 是否被动道具
            partition: 分区名称
            icon: 图标
            send_success_msg: 成功时发送消息
            max_num_limit: 单次最大使用次数
        """
        _current_len = -1
        for x in [name, price, des, discount, limit_time, load_status]:
            if isinstance(x, tuple):
                if _current_len == -1:
                    _current_len = len(x)
                if _current_len != len(x):
                    raise ValueError(
                        f"注册商品 {name} 中 name，price，des，discount，limit_time，"
                        "load_status，daily_limit 数量不符！"
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
        _partition = self.__get(partition, _current_len)
        _icon = self.__get(icon, _current_len)
        _send_success_msg = self.__get(send_success_msg, _current_len)
        _max_num_limit = self.__get(max_num_limit, _current_len)
        return self.register(
            _name,
            _price,
            _des,
            _discount,
            _limit_time,
            _load_status,
            _daily_limit,
            _is_passive,
            _partition,
            _icon,
            _send_success_msg,
            _max_num_limit,
            **kwargs,
        )

    def __get(self, value, _current_len):
        return (
            value
            if isinstance(value, tuple)
            else tuple(value for _ in range(_current_len))
        )

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

    def __init__(self, info: str | MessageSegment | Message | None):
        super().__init__(self)
        self._info = info

    def get_info(self):
        return self._info


shop_register = ShopRegister()
