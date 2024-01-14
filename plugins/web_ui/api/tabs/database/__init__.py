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

from ....base_model import BaseResultModel, QueryModel, Result
from ....config import QueryDateType
from ....utils import authentication
from .models.model import SqlModel, SqlText
from .models.sql_log import SqlLog

router = APIRouter(prefix="/database")


driver: Driver = nonebot.get_driver()


SQL_DICT = {}


SELECT_TABLE_SQL = """
select a.tablename as name,d.description as desc from pg_tables a
    left join pg_class c on relname=tablename
    left join pg_description d on oid=objoid and objsubid=0 where a.schemaname = 'public'
"""

SELECT_TABLE_COLUMN_SQL = """
SELECT column_name, data_type, character_maximum_length as max_length, is_nullable
FROM information_schema.columns
WHERE table_name = '{}';
"""

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

@router.get("/get_table_list", dependencies=[authentication()], description="获取数据库表")
async def _() -> Result:       
    db = Tortoise.get_connection("default")
    query = await db.execute_query_dict(SELECT_TABLE_SQL)
    return Result.ok(query)

@router.get("/get_table_column", dependencies=[authentication()], description="获取表字段")
async def _(table_name: str) -> Result:       
    db = Tortoise.get_connection("default")
    print(SELECT_TABLE_COLUMN_SQL.format(table_name))
    query = await db.execute_query_dict(SELECT_TABLE_COLUMN_SQL.format(table_name))
    return Result.ok(query)

@router.post("/exec_sql", dependencies=[authentication()], description="执行sql")
async def _(sql: SqlText, request: Request) -> Result:
    ip = request.client.host if request.client else "unknown"
    try:
        if sql.sql.lower().startswith("select"):
            db = Tortoise.get_connection("default")
            res = await db.execute_query_dict(sql.sql)
            await SqlLog.add(ip or "0.0.0.0", sql.sql, "")
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
    total = await SqlLog.all().count()
    if (total % query.size):
        total += 1
    data = await SqlLog.all().order_by("-id").offset((query.index - 1) * query.size).limit(query.size)
    return Result.ok(BaseResultModel(total=total, data=data))


@router.get("/get_common_sql", dependencies=[authentication()], description="常用sql")
async def _(plugin_name: Optional[str] = None) -> Result:
    if plugin_name:
        return Result.ok(SQL_DICT.get(plugin_name))
    return Result.ok(str(SQL_DICT))
