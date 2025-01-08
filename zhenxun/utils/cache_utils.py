from collections.abc import Callable
from functools import wraps
import time
from typing import Any, ClassVar, Generic, TypeVar, cast

from nonebot.utils import is_coroutine_callable
from pydantic import BaseModel

from zhenxun.services.log import logger

__all__ = ["Cache", "CacheData", "CacheRoot"]

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
    name: str
    """缓存名称"""
    func: Callable[..., Any]
    """更新方法"""
    getter: CacheGetter | None = None
    """获取方法"""
    updater: Callable[..., Any] | None = None
    """更新单个方法"""
    data: Any = None
    """缓存数据"""
    expire: int
    """缓存过期时间"""
    reload_time = time.time()
    """更新时间"""
    reload_count: int = 0
    """更新次数"""

    async def get(self, *args, **kwargs) -> Any:
        """获取单个缓存"""
        if not self.getter:
            return self.data
        return await self.getter.get(self.data, *args, **kwargs)

    async def update(self, key: str, value: Any = None, *args, **kwargs):
        """更新单个缓存"""
        if not self.updater:
            return logger.warning(
                f"缓存类型 {self.name} 没有更新方法，无法更新", "CacheRoot"
            )
        if self.data:
            if is_coroutine_callable(self.updater):
                await self.updater(self.data, key, value, *args, **kwargs)
            else:
                self.updater(self.data, key, value, *args, **kwargs)
        else:
            logger.warning(f"缓存类型 {self.name} 为空，无法更新", "CacheRoot")

    async def reload(self, *args, **kwargs):
        """更新缓存"""
        self.data = (
            await self.func(*args, **kwargs)
            if is_coroutine_callable(self.func)
            else self.func(*args, **kwargs)
        )
        self.reload_time = time.time()
        self.reload_count += 1
        logger.debug(f"缓存类型 {self.name} 更新全局缓存", "CacheRoot")

    async def check_expire(self):
        if time.time() - self.reload_time > self.expire or not self.reload_count:
            await self.reload()


class CacheManage:
    """全局缓存管理，减少数据库与网络请求查询次数


    异常:
        ValueError: 数据名称重复
        ValueError: 数据不存在

    """

    _data: ClassVar[dict[str, CacheData]] = {}

    def new(self, name: str, expire: int = 60 * 10):
        def wrapper(func: Callable):
            _name = name.upper()
            if _name in self._data:
                raise ValueError(f"DbCache 缓存数据 {name} 已存在...")
            self._data[_name] = CacheData(name=_name, func=func, expire=expire)

        return wrapper

    def listener(self, name: str):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    if is_coroutine_callable(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    return result
                finally:
                    cache_data = self._data.get(name.upper())
                    if cache_data:
                        await cache_data.reload()
                        logger.debug(
                            f"缓存类型 {name.upper()} 进行监听更新...", "CacheRoot"
                        )

            return wrapper

        return decorator

    def updater(self, name: str):
        def wrapper(func: Callable):
            _name = name.upper()
            if _name not in self._data:
                raise ValueError(f"DbCache 缓存数据 {name} 不存在...")
            self._data[_name].updater = func

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

    async def get_cache_data(self, name: str):
        if cache := await self.get_cache(name):
            return cache.data
        return None

    async def get_cache(self, name: str) -> CacheData | None:
        name = name.upper()
        cache = self._data.get(name)
        if cache:
            await self.check_expire(name)
            return cache
        return None

    async def get(self, name: str, *args, **kwargs):
        cache = await self.get_cache(name.upper())
        if cache:
            return await cache.get(*args, **kwargs) if cache.getter else cache.data
        return None

    async def reload(self, name: str, *args, **kwargs):
        cache = await self.get_cache(name.upper())
        if cache:
            await cache.reload(*args, **kwargs)

    async def update(self, name: str, key: str, value: Any, *args, **kwargs):
        cache = await self.get_cache(name.upper())
        if cache:
            await cache.update(key, value, *args, **kwargs)


CacheRoot = CacheManage()


class Cache(Generic[T]):
    def __init__(self, module: str):
        self.module = module

    async def get(self, *args, **kwargs) -> T | None:
        return await CacheRoot.get(self.module, *args, **kwargs)

    async def update(self, key: str, value: Any = None, *args, **kwargs):
        return await CacheRoot.update(self.module, key, value, *args, **kwargs)

    async def reload(self, key: str | None = None, *args, **kwargs):
        await CacheRoot.reload(self.module, key, *args, **kwargs)
