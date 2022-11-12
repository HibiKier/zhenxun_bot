from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot
from pydantic import create_model
from utils.models import ShopParam
from typing import Optional, Union, Callable, List, Tuple, Dict, Any
from types import MappingProxyType
import inspect
import asyncio


class GoodsUseFuncManager:
    def __init__(self):
        self._data = {}

    def register_use_before_handle(self, goods_name: str, fun_list: List[Callable]):
        """
        说明:
            注册商品使用前函数
        参数:
            :param goods_name: 商品名称
            :param fun_list: 函数列表
        """
        if fun_list:
            self._data[goods_name]["before_handle"] = fun_list
            logger.info(f"register_use_before_handle 成功注册商品：{goods_name} 的{len(fun_list)}个使用前函数")

    def register_use_after_handle(self, goods_name: str, fun_list: List[Callable]):
        """
        说明:
            注册商品使用后函数
        参数:
            :param goods_name: 商品名称
            :param fun_list: 函数列表
        """
        if fun_list:
            self._data[goods_name]["after_handle"] = fun_list
            logger.info(f"register_use_after_handle 成功注册商品：{goods_name} 的{len(fun_list)}个使用后函数")

    def register_use(self, goods_name: str, **kwargs):
        """
        注册商品使用方法
        :param goods_name: 商品名称
        :param kwargs: kwargs
        """
        self._data[goods_name] = kwargs

    def exists(self, goods_name: str) -> bool:
        """
        判断商品使用方法是否被注册
        :param goods_name: 商品名称
        """
        return bool(self._data.get(goods_name))

    def get_max_num_limit(self, goods_name: str) -> int:
        """
        获取单次商品使用数量
        :param goods_name: 商品名称
        """
        if self.exists(goods_name):
            return self._data[goods_name]["kwargs"]["max_num_limit"]
        return 1

    def _parse_args(self, args_: MappingProxyType, param: ShopParam, **kwargs):
        param_list_ = []
        _bot = param.bot
        param.bot = None
        param_json = param.dict()
        param_json["bot"] = _bot
        for par in args_.keys():
            if par in ["shop_param"]:
                param_list_.append(param)
            elif par not in ["args", "kwargs"]:
                param_list_.append(param_json.get(par))
                if kwargs.get(par) is not None:
                    del kwargs[par]
        return param_list_

    async def use(
        self, param: ShopParam, **kwargs
    ) -> Optional[Union[str, MessageSegment]]:
        """
        使用道具
        :param param: BaseModel
        :param kwargs: kwargs
        """
        goods_name = param.goods_name
        if self.exists(goods_name):
            # 使用方法
            args = inspect.signature(self._data[goods_name]["func"]).parameters
            if args and list(args.keys())[0] != "kwargs":
                if asyncio.iscoroutinefunction(self._data[goods_name]["func"]):
                    return await self._data[goods_name]["func"](
                        *self._parse_args(args, param, **kwargs)
                    )
                else:
                    return self._data[goods_name]["func"](
                        *self._parse_args(args, param, **kwargs)
                    )
            else:
                if asyncio.iscoroutinefunction(self._data[goods_name]["func"]):
                    return await self._data[goods_name]["func"](
                        **kwargs,
                    )
                else:
                    return self._data[goods_name]["func"](
                        **kwargs,
                    )

    async def run_handle(self, goods_name: str, type_: str, param: ShopParam, **kwargs):
        if self._data[goods_name].get(type_):
            for func in self._data[goods_name].get(type_):
                args = inspect.signature(func).parameters
                if args and list(args.keys())[0] != "kwargs":
                    if asyncio.iscoroutinefunction(func):
                        await func(*self._parse_args(args, param, **kwargs))
                    else:
                        func(*self._parse_args(args, param, **kwargs))
                else:
                    if asyncio.iscoroutinefunction(func):
                        await func(**kwargs)
                    else:
                        func(**kwargs)

    def check_send_success_message(self, goods_name: str) -> bool:
        """
        检查是否发送使用成功信息
        :param goods_name: 商品名称
        """
        if self.exists(goods_name):
            return bool(self._data[goods_name]["kwargs"]["send_success_msg"])
        return False

    def get_kwargs(self, goods_name: str) -> dict:
        """
        获取商品使用方法的kwargs
        :param goods_name: 商品名称
        """
        if self.exists(goods_name):
            return self._data[goods_name]["kwargs"]
        return {}

    def init_model(self, goods_name: str, bot: Bot, event: GroupMessageEvent, num: int, text: str):
        return self._data[goods_name]["model"](
            **{
                "goods_name": goods_name,
                "bot": bot,
                "event": event,
                "user_id": event.user_id,
                "group_id": event.group_id,
                "num": num,
                "message": event.message,
                "text": text
            }
        )


func_manager = GoodsUseFuncManager()


def build_params(
    bot: Bot, event: GroupMessageEvent, goods_name: str, num: int, text: str
) -> Tuple[ShopParam, Dict[str, Any]]:
    """
    说明:
        构造参数
    参数:
        :param bot: bot
        :param event: event
        :param goods_name: 商品名称
        :param num: 数量
        :param text: 其他信息
    :return:
    """
    _kwargs = func_manager.get_kwargs(goods_name)
    return (
        func_manager.init_model(goods_name, bot, event, num, text),
        {
            **_kwargs,
            "_bot": bot,
            "event": event,
            "group_id": event.group_id,
            "user_id": event.user_id,
            "num": num,
            "text": text,
            "message": event.message,
            "goods_name": goods_name,
        },
    )


async def effect(
    bot: Bot, event: GroupMessageEvent, goods_name: str, num: int, text: str, message: Message
) -> Optional[Union[str, MessageSegment]]:
    """
    商品生效
    :param bot: Bot
    :param event: GroupMessageEvent
    :param goods_name: 商品名称
    :param num: 使用数量
    :param text: 其他信息
    :param message: Message
    :return: 使用是否成功
    """
    # 优先使用注册的商品插件
    # try:
    if func_manager.exists(goods_name):
        _kwargs = func_manager.get_kwargs(goods_name)
        model, kwargs = build_params(bot, event, goods_name, num, text)
        return await func_manager.use(model, **kwargs)
    # except Exception as e:
    #     logger.error(f"use 商品生效函数effect 发生错误 {type(e)}：{e}")
    return None


def register_use(goods_name: str, func: Callable, **kwargs):
    """
    注册商品使用方法
    :param goods_name: 商品名称
    :param func: 使用函数
    :param kwargs: kwargs
    """
    if func_manager.exists(goods_name):
        raise ValueError("该商品使用函数已被注册！")
    # 发送使用成功信息
    kwargs["send_success_msg"] = kwargs.get("send_success_msg", True)
    kwargs["max_num_limit"] = kwargs.get("max_num_limit", 1)
    func_manager.register_use(
        goods_name,
        **{
            "func": func,
            "model": create_model(f"{goods_name}_model", __base__=ShopParam, **kwargs),
            "kwargs": kwargs,
        },
    )
    logger.info(f"register_use 成功注册商品：{goods_name} 的使用函数")
