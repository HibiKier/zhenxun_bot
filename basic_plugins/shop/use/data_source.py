import asyncio
from services.log import logger

_use_func_data = {}


async def effect(user_id: int, group_id: int, goods_name: str) -> bool:
    """
    商品生效
    :param user_id: 用户id
    :param group_id: 群号
    :param goods_name: 商品名称
    :return: 使用是否成功
    """
    # 优先使用注册的商品插件
    try:
        if _use_func_data.get(goods_name):
            _kwargs = _use_func_data[goods_name]["kwargs"]
            _kwargs["goods_name"] = goods_name
            _kwargs["user_id"] = user_id
            _kwargs["group_id"] = group_id
            if asyncio.iscoroutinefunction(_use_func_data[goods_name]["func"]):
                await _use_func_data[goods_name]["func"](
                    **_kwargs,
                )
            else:
                _use_func_data[goods_name]["func"](
                    **_kwargs,
                )
        return True
    except Exception as e:
        logger.error(f"use 商品生效函数effect 发生错误 {type(e)}：{e}")
    return False


def registered_use(goods_name: str, func, **kwargs):
    """
    注册商品使用方法
    :param goods_name: 商品名称
    :param func: 使用函数
    :param kwargs: kwargs
    """
    if goods_name in _use_func_data.keys():
        raise ValueError("该商品使用函数已被注册！")
    _use_func_data[goods_name] = {"func": func, "kwargs": kwargs}
