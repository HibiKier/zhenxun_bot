from collections.abc import Callable
import time
from typing import Any, ClassVar, Generic, TypeVar, cast

from nonebot.utils import is_coroutine_callable
from pydantic import BaseModel

__all__ = ["Cache", "CacheData"]

T = TypeVar("T")


class CacheGetter(BaseModel, Generic[T]):
    get_func: Callable[..., Any] | None = None
    """获取方法"""

    async def get(self, data: Any, *args, **kwargs) -> T:
        """获取缓存"""
        processed_data = (
            await self.get_func(data, *args, **kwargs)
            if self.get_func and is_coroutine_callable(self.get_func)
            else self.get_func(data, *args, **kwargs)
            if self.get_func
            else data
        )
        return cast(T, processed_data)


class CacheData(BaseModel):
    func: Callable[..., Any]
    """更新方法"""
    getter: CacheGetter | None = None
    """获取方法"""
    data: Any = None
    """缓存数据"""
    expire: int
    """缓存过期时间"""
    reload_time = time.time()
    """更新时间"""
    reload_count: int = 0
    """更新次数"""

    async def reload(self):
        """更新缓存"""
        self.data = (
            await self.func() if is_coroutine_callable(self.func) else self.func()
        )
        self.reload_time = time.time()
        self.reload_count += 1

    async def check_expire(self):
        if time.time() - self.reload_time > self.expire or not self.reload_count:
            await self.reload()


class CacheManage:
    _data: ClassVar[dict[str, CacheData]] = {}

    def listener(self, name: str, expire: int = 60 * 10):
        def wrapper(func: Callable):
            _name = name.upper()
            if _name in self._data:
                raise ValueError(f"DbCache 缓存数据 {name} 已存在...")
            self._data[_name] = CacheData(func=func, expire=expire)

        return wrapper

    def getter(self, name: str, result_model: type | None = None):
        def wrapper(func: Callable):
            _name = name.upper()
            if _name not in self._data:
                raise ValueError(f"DbCache 缓存数据 {name} 不存在...")
            self._data[_name].getter = CacheGetter[result_model](get_func=func)

        return wrapper

    async def check_expire(self, name: str):
        name = name.upper()
        if self._data.get(name):
            if (
                time.time() - self._data[name].reload_time > self._data[name].expire
                or not self._data[name].reload_count
            ):
                await self._data[name].reload()

    async def get_cache_data(self, name: str) -> CacheData | None:
        if cache := await self.get_cache(name):
            return cache
        return None

    async def get_cache(self, name: str):
        name = name.upper()
        cache = self._data.get(name)
        if cache:
            await self.check_expire(name)
            return cache
        return None

    async def get(self, name: str, *args, **kwargs) -> T | None:
        cache = self._data.get(name.upper())
        if cache:
            return (
                await cache.getter.get(*args, **kwargs) if cache.getter else cache.data
            )
        return None

    async def reload(self, name: str):
        cache = self._data.get(name.upper())
        if cache:
            await cache.reload()


Cache = CacheManage()
