from nonebot.adapters.cqhttp import GroupMessageEvent
from services.log import logger
from nonebot.adapters.cqhttp import Bot
import asyncio


class GoodsUseFuncManager:
    def __init__(self):
        self._data = {}

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
            return self._data[goods_name]["kwargs"]["_max_num_limit"]
        return 1

    async def use(self, **kwargs):
        """
        使用道具
        :param kwargs: kwargs
        """
        goods_name = kwargs.get("goods_name")
        if self.exists(goods_name):
            if asyncio.iscoroutinefunction(self._data[goods_name]["func"]):
                await self._data[goods_name]["func"](
                    **kwargs,
                )
            else:
                self._data[goods_name]["func"](
                    **kwargs,
                )

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


func_manager = GoodsUseFuncManager()


async def effect(bot: Bot, event: GroupMessageEvent, goods_name: str, num: int) -> bool:
    """
    商品生效
    :param bot: Bot
    :param event: GroupMessageEvent
    :param goods_name: 商品名称
    :param num: 使用数量
    :return: 使用是否成功
    """
    # 优先使用注册的商品插件
    try:
        if func_manager.exists(goods_name):
            _kwargs = func_manager.get_kwargs(goods_name)
            await func_manager.use(
                **{
                    **_kwargs,
                    "_bot": bot,
                    "event": event,
                    "group_id": event.group_id,
                    "user_id": event.user_id,
                    "num": num,
                    "goods_name": goods_name,
                }
            )
        return True
    except Exception as e:
        logger.error(f"use 商品生效函数effect 发生错误 {type(e)}：{e}")
    return False


def register_use(goods_name: str, func, **kwargs):
    """
    注册商品使用方法
    :param goods_name: 商品名称
    :param func: 使用函数
    :param kwargs: kwargs
    """
    if func_manager.exists(goods_name):
        raise ValueError("该商品使用函数已被注册！")
    # 发送使用成功信息
    if kwargs.get("send_success_msg") is None:
        kwargs["send_success_msg"] = True
    kwargs["_max_num_limit"] = (
        kwargs.get("_max_num_limit") if kwargs.get("_max_num_limit") else 1
    )
    func_manager.register_use(goods_name, **{"func": func, "kwargs": kwargs})
    logger.info(f"register_use 成功注册商品：{goods_name} 的使用函数")
