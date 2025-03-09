from collections.abc import Callable
from typing import ClassVar

import nonebot
from nonebot.utils import is_coroutine_callable

from zhenxun.services.log import logger
from zhenxun.utils.enum import HookPriorityType
from zhenxun.utils.exception import HookPriorityException

driver = nonebot.get_driver()


class HookPriorityManager:
    _data: ClassVar[dict[HookPriorityType, dict[int, list[Callable]]]] = {}

    @classmethod
    def add(cls, hook_type: HookPriorityType, func: Callable, priority: int = 5):
        if hook_type not in cls._data:
            cls._data[hook_type] = {}
        if priority not in cls._data[hook_type]:
            cls._data[hook_type][priority] = []
        cls._data[hook_type][priority].append(func)

    @classmethod
    def on_startup(cls, priority: int = 5):
        def wrapper(func):
            cls.add(HookPriorityType.STARTUP, func, priority)
            return func

        return wrapper

    @classmethod
    def on_shutdown(cls, priority: int = 5):
        def wrapper(func):
            cls.add(HookPriorityType.SHUTDOWN, func, priority)
            return func

        return wrapper


@driver.on_startup
async def _():
    priority_data = HookPriorityManager._data.get(HookPriorityType.STARTUP)
    if not priority_data:
        return
    priority_list = sorted(priority_data.keys())
    priority = 0
    try:
        for priority in priority_list:
            for func in priority_data[priority]:
                if is_coroutine_callable(func):
                    await func()
                else:
                    func()
    except HookPriorityException as e:
        logger.error(f"打断优先级 [{priority}] on_startup 方法. {type(e)}: {e}")
