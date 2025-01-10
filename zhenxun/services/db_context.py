from collections.abc import Iterable
from typing import Any
from typing_extensions import Self

import nonebot
from nonebot.utils import is_coroutine_callable
from tortoise import Tortoise
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.connection import connections
from tortoise.models import Model as TortoiseModel

from zhenxun.configs.config import BotConfig

from .cache import CacheRoot
from .log import logger

SCRIPT_METHOD = []
MODELS: list[str] = []

driver = nonebot.get_driver()

CACHE_FLAG = False


@driver.on_bot_connect
def _():
    global CACHE_FLAG
    CACHE_FLAG = True


class Model(TortoiseModel):
    """
    自动添加模块

    Args:
        Model_: Model
    """

    def __init_subclass__(cls, **kwargs):
        MODELS.append(cls.__module__)

        if func := getattr(cls, "_run_script", None):
            SCRIPT_METHOD.append((cls.__module__, func))

    @classmethod
    def get_cache_type(cls):
        return getattr(cls, "cache_type", None) if CACHE_FLAG else None

    @classmethod
    async def create(
        cls, using_db: BaseDBAsyncClient | None = None, **kwargs: Any
    ) -> Self:
        result = await super().create(using_db=using_db, **kwargs)
        if cache_type := cls.get_cache_type():
            await CacheRoot.reload(cache_type)
        return result

    @classmethod
    async def get_or_create(
        cls,
        defaults: dict | None = None,
        using_db: BaseDBAsyncClient | None = None,
        **kwargs: Any,
    ) -> tuple[Self, bool]:
        result = await super().get_or_create(
            defaults=defaults, using_db=using_db, **kwargs
        )
        if cache_type := cls.get_cache_type():
            await CacheRoot.reload(cache_type)
        return result

    @classmethod
    async def update_or_create(
        cls,
        defaults: dict | None = None,
        using_db: BaseDBAsyncClient | None = None,
        **kwargs: Any,
    ) -> tuple[Self, bool]:
        result = await super().update_or_create(
            defaults=defaults, using_db=using_db, **kwargs
        )
        if cache_type := cls.get_cache_type():
            await CacheRoot.reload(cache_type)
        return result

    @classmethod
    async def bulk_create(  # type: ignore
        cls,
        objects: Iterable[Self],
        batch_size: int | None = None,
        ignore_conflicts: bool = False,
        update_fields: Iterable[str] | None = None,
        on_conflict: Iterable[str] | None = None,
        using_db: BaseDBAsyncClient | None = None,
    ) -> list[Self]:
        result = await super().bulk_create(
            objects=objects,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts,
            update_fields=update_fields,
            on_conflict=on_conflict,
            using_db=using_db,
        )
        if cache_type := cls.get_cache_type():
            await CacheRoot.reload(cache_type)
        return result

    @classmethod
    async def bulk_update(  # type: ignore
        cls,
        objects: Iterable[Self],
        fields: Iterable[str],
        batch_size: int | None = None,
        using_db: BaseDBAsyncClient | None = None,
    ) -> int:
        result = await super().bulk_update(
            objects=objects,
            fields=fields,
            batch_size=batch_size,
            using_db=using_db,
        )
        if cache_type := cls.get_cache_type():
            await CacheRoot.reload(cache_type)
        return result

    async def save(
        self,
        using_db: BaseDBAsyncClient | None = None,
        update_fields: Iterable[str] | None = None,
        force_create: bool = False,
        force_update: bool = False,
    ):
        await super().save(
            using_db=using_db,
            update_fields=update_fields,
            force_create=force_create,
            force_update=force_update,
        )
        if CACHE_FLAG and (cache_type := getattr(self, "cache_type", None)):
            await CacheRoot.reload(cache_type)

    async def delete(self, using_db: BaseDBAsyncClient | None = None):
        await super().delete(using_db=using_db)
        if CACHE_FLAG and (cache_type := getattr(self, "cache_type", None)):
            await CacheRoot.reload(cache_type)


class DbUrlIsNode(Exception):
    """
    数据库链接地址为空
    """

    pass


class DbConnectError(Exception):
    """
    数据库连接错误
    """

    pass


async def init():
    if not BotConfig.db_url:
        raise DbUrlIsNode("数据库配置为空，请在.env.dev中配置DB_URL...")
    try:
        await Tortoise.init(
            db_url=BotConfig.db_url,
            modules={"models": MODELS},
            timezone="Asia/Shanghai",
        )
        if SCRIPT_METHOD:
            db = Tortoise.get_connection("default")
            logger.debug(
                "即将运行SCRIPT_METHOD方法, 合计 "
                f"<u><y>{len(SCRIPT_METHOD)}</y></u> 个..."
            )
            sql_list = []
            for module, func in SCRIPT_METHOD:
                try:
                    sql = await func() if is_coroutine_callable(func) else func()
                    if sql:
                        sql_list += sql
                except Exception as e:
                    logger.debug(f"{module} 执行SCRIPT_METHOD方法出错...", e=e)
            for sql in sql_list:
                logger.debug(f"执行SQL: {sql}")
                try:
                    await db.execute_query_dict(sql)
                    # await TestSQL.raw(sql)
                except Exception as e:
                    logger.debug(f"执行SQL: {sql} 错误...", e=e)
            if sql_list:
                logger.debug("SCRIPT_METHOD方法执行完毕!")
        await Tortoise.generate_schemas()
        logger.info("Database loaded successfully!")
    except Exception as e:
        raise DbConnectError(f"数据库连接错误... e:{e}") from e


async def disconnect():
    await connections.close_all()
