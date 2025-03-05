from collections.abc import Callable
from functools import wraps
import inspect
import time
from typing import Any, ClassVar, Generic, TypeVar, cast

from nonebot.utils import is_coroutine_callable
from nonebot_plugin_apscheduler import scheduler
from pydantic import BaseModel

from zhenxun.services.log import logger

__all__ = ["Cache", "CacheData", "CacheRoot"]

T = TypeVar("T")


class DbCacheException(Exception):
    def __init__(self, info: str):
        self.info = info

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return self.info


def validate_name(func: Callable):
    """
    装饰器：验证 name 是否存在于 CacheManage._data 中。
    """

    def wrapper(self, name: str, *args, **kwargs):
        _name = name.upper()
        if _name not in CacheManage._data:
            raise DbCacheException(f"DbCache 缓存数据 {name} 不存在...")
        return func(self, _name, *args, **kwargs)

    return wrapper


class CacheGetter(BaseModel, Generic[T]):
    get_func: Callable[..., Any] | None = None
    """获取方法"""

    async def get(self, cache_data: "CacheData", *args, **kwargs) -> T:
        """获取缓存"""
        processed_data = (
            await self.get_func(cache_data, *args, **kwargs)
            if self.get_func and is_coroutine_callable(self.get_func)
            else self.get_func(cache_data, *args, **kwargs)
            if self.get_func
            else cache_data.data
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
    with_refresh: Callable[..., Any] | None = None
    """刷新方法"""
    with_expiration: Callable[..., Any] | None = None
    """缓存时间初始化方法"""
    cleanup_expired: Callable[..., Any] | None = None
    """缓存过期方法"""
    data: Any = None
    """缓存数据"""
    expire: int
    """缓存过期时间"""
    expire_data: dict[str, int | float] = {}
    """缓存过期数据时间记录"""
    reload_time: float = time.time()
    """更新时间"""
    reload_count: int = 0
    """更新次数"""

    async def get(self, *args, **kwargs) -> Any:
        """获取单个缓存"""
        self.call_cleanup_expired()  # 移除过期缓存
        if not self.getter:
            return self.data
        result = await self.getter.get(self, *args, **kwargs)
        await self.call_with_expiration()
        return result

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
            logger.debug(
                f"缓存类型 {self.name} 更新单个缓存 key: {key}，value: {value}",
                "CacheRoot",
            )
            self.expire_data[key] = time.time() + self.expire
        else:
            logger.warning(f"缓存类型 {self.name} 为空，无法更新", "CacheRoot")

    async def refresh(self, *args, **kwargs):
        """刷新缓存，只刷新已缓存的数据"""
        if not self.with_refresh:
            return await self.reload(*args, **kwargs)
        if self.data:
            if is_coroutine_callable(self.with_refresh):
                await self.with_refresh(self.data, *args, **kwargs)
            else:
                self.with_refresh(self.data, *args, **kwargs)
            logger.debug(
                f"缓存类型 {self.name} 刷新全局缓存，共刷新 {len(self.data)} 条数据",
                "CacheRoot",
            )

    async def reload(self, *args, **kwargs):
        """更新全部缓存数据"""
        if self.has_args():
            self.data = (
                await self.func(*args, **kwargs)
                if is_coroutine_callable(self.func)
                else self.func(*args, **kwargs)
            )
        else:
            self.data = (
                await self.func() if is_coroutine_callable(self.func) else self.func()
            )
        await self.call_with_expiration()
        self.reload_time = time.time()
        self.reload_count += 1
        logger.debug(
            f"缓存类型 {self.name} 更新全局缓存，共更新 {len(self.data)} 条数据",
            "CacheRoot",
        )

    def call_cleanup_expired(self):
        """清理过期缓存"""
        if self.cleanup_expired:
            if result := self.cleanup_expired(self):
                logger.debug(
                    f"成功清理 {self.name} {len(result)} 条过期缓存", "CacheRoot"
                )

    async def call_with_expiration(self, is_force: bool = False):
        """缓存时间更新

        参数:
            is_force: 是否强制更新全部数据缓存时间.
        """
        if self.with_expiration:
            if is_force:
                self.expire_data = {}
            expiration_data = (
                await self.with_expiration(self.data, self.expire_data, self.expire)
                if is_coroutine_callable(self.with_expiration)
                else self.with_expiration(self.data, self.expire_data, self.expire)
            )
            self.expire_data = {**self.expire_data, **expiration_data}

    def has_args(self):
        """是否含有参数

        返回:
            bool: 是否含有参数
        """
        sig = inspect.signature(self.func)
        return any(
            param.kind
            in (
                param.POSITIONAL_OR_KEYWORD,
                param.POSITIONAL_ONLY,
                param.VAR_POSITIONAL,
            )
            for param in sig.parameters.values()
        )


class CacheManage:
    """全局缓存管理，减少数据库与网络请求查询次数


    异常:
        DbCacheException: 数据名称重复
        DbCacheException: 数据不存在

    """

    _data: ClassVar[dict[str, CacheData]] = {}

    def start_check(self):
        """启动缓存检查"""
        for cache_data in self._data.values():
            if cache_data.cleanup_expired:
                scheduler.add_job(
                    cache_data.call_cleanup_expired,
                    "interval",
                    seconds=cache_data.expire,
                    args=[],
                    id=f"CacheRoot-{cache_data.name}",
                )

    def new(self, name: str, expire: int = 60 * 10):
        def wrapper(func: Callable):
            _name = name.upper()
            if _name in self._data:
                raise DbCacheException(f"DbCache 缓存数据 {name} 已存在...")
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
                    if cache_data and cache_data.with_refresh:
                        if is_coroutine_callable(cache_data.with_refresh):
                            await cache_data.with_refresh(cache_data.data)
                        else:
                            cache_data.with_refresh(cache_data.data)
                        await cache_data.call_with_expiration(True)
                        logger.debug(
                            f"缓存类型 {name.upper()} 进行监听更新...", "CacheRoot"
                        )

            return wrapper

        return decorator

    @validate_name
    def updater(self, name: str):
        def wrapper(func: Callable):
            self._data[name.upper()].updater = func

        return wrapper

    @validate_name
    def getter(self, name: str, result_model: type | None = None):
        def wrapper(func: Callable):
            self._data[name].getter = CacheGetter[result_model](get_func=func)

        return wrapper

    @validate_name
    def with_refresh(self, name: str):
        def wrapper(func: Callable):
            self._data[name.upper()].with_refresh = func

        return wrapper

    @validate_name
    def with_expiration(self, name: str):
        def wrapper(func: Callable[[Any, int], dict[str, float]]):
            self._data[name.upper()].with_expiration = func

        return wrapper

    @validate_name
    def cleanup_expired(self, name: str):
        def wrapper(func: Callable[[CacheData], None]):
            self._data[name.upper()].cleanup_expired = func

        return wrapper

    async def check_expire(self, name: str, *args, **kwargs):
        name = name.upper()
        if self._data.get(name) and (
            time.time() - self._data[name].reload_time > self._data[name].expire
            or not self._data[name].reload_count
        ):
            await self._data[name].reload(*args, **kwargs)

    async def get_cache_data(self, name: str):
        return cache.data if (cache := await self.get_cache(name)) else None

    async def get_cache(self, name: str, *args, **kwargs) -> CacheData | None:
        name = name.upper()
        if cache := self._data.get(name):
            # await self.check_expire(name, *args, **kwargs)
            return cache
        return None

    async def get(self, name: str, *args, **kwargs):
        cache = await self.get_cache(name.upper(), *args, **kwargs)
        if cache:
            return await cache.get(*args, **kwargs) if cache.getter else cache.data
        return None

    async def reload(self, name: str, *args, **kwargs):
        cache = await self.get_cache(name.upper())
        if cache:
            await cache.refresh(*args, **kwargs)

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
