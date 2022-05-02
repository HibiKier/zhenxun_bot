#
# from functools import wraps
# from typing import Union, List, Callable
# from nonebot.plugin import require
# from nonebot.adapters.onebot.v11 import Bot
# import asyncio
# import nonebot
#
# driver = nonebot.get_driver()
#
# use = require("use")
# shop = require("shop_handle")
#
# flag = False
#
# name_list = []
#
# func_list = []
#
#
# def shop_register(
#         name: Union[str, List[str]],
#         price: Union[int, List[int]],
#         des: Union[str, List[str]],
#         discount: Union[float, List[float]] = 1,
#         limit_time: Union[int, List[int]] = 0,
#         status: bool = True,
#         **kwargs_
# ):
#     print("---------")
#     print("name：", name)
#     print("price：", price)
#     print("des：", des)
#     print("discount：", discount)
#     print("limit_time：", limit_time)
#     print("status：", status)
#     print("kwargs:", kwargs_)
#     asyncio.run(shop.register_goods(
#         name, 30, price, discount, limit_time
#     ))
#
#     def _register_use(goods_func: Callable):
#         def _wrapper(**kwargs):
#             # print(*args)
#             print(**kwargs)
#             print(1111111111111111)
#             use.register_use(name, goods_func, **kwargs)
#             # func_list.append({"name": name, "func": goods_func, "args": args, "kwargs": kwargs})
#         return _wrapper
#
#     return _register_use
#
#
# @driver.on_bot_connect
# async def do_something(bot: Bot):
#     for func in func_list:
#         if asyncio.iscoroutinefunction(func):
#             await func()
#         else:
#             func()
