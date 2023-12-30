from os import name
from typing import Optional

import nonebot
from fastapi import APIRouter, Request
from nonebot.drivers import Driver
from tortoise import Tortoise
from tortoise.exceptions import OperationalError

from configs.config import NICKNAME
from services.db_context import TestSQL
from utils.utils import get_matchers

from ....base_model import QueryModel, Result
from ....config import QueryDateType
from ....utils import authentication
from .models.model import SqlModel, SqlText
from .models.sql_log import SqlLog

router = APIRouter()


driver: Driver = nonebot.get_driver()


SQL_DICT = {}


@driver.on_startup
async def _():
    for matcher in get_matchers(True):
        if _plugin := matcher.plugin:
            try:
                _module = _plugin.module
            except AttributeError:
                pass
            else:
                plugin_name = matcher.plugin_name
                if plugin_name in SQL_DICT:
                    raise ValueError(f"{plugin_name} 常用SQL plugin_name 重复")
                SqlModel(
                    name=getattr(_module, "__plugin_name__", None) or plugin_name or "",
                    plugin_name=plugin_name or "",
                    sql_list=getattr(_module, "sql_list", []),
                )
                SQL_DICT[plugin_name] = SqlModel


@router.post("/exec_sql", dependencies=[authentication()], description="执行sql")
async def _(sql: SqlText, request: Request) -> Result:
    ip = request.client.host if request.client else "unknown"
    try:
        if sql.sql.lower().startswith("select"):
            db = Tortoise.get_connection("default")
            res = await db.execute_query_dict(sql.sql)
            return Result.ok(res, "执行成功啦!")
        else:
            result = await TestSQL.raw(sql.sql)
            await SqlLog.add(ip or "0.0.0.0", sql.sql, str(result))
            return Result.ok(info="执行成功啦!")
    except OperationalError as e:
        await SqlLog.add(ip or "0.0.0.0", sql.sql, str(e), False)
        return Result.warning_(f"sql执行错误: {e}")


@router.post("/get_sql_log", dependencies=[authentication()], description="sql日志列表")
async def _(query: QueryModel) -> Result:
    data = await SqlLog.all().offset((query.index - 1) * query.size).limit(query.size)
    return Result.ok(data)


@router.get("/get_sql", dependencies=[authentication()], description="常用sql")
async def _(plugin_name: Optional[str] = None) -> Result:
    if plugin_name:
        return Result.ok(SQL_DICT.get(plugin_name))
    return Result.ok(SQL_DICT)
