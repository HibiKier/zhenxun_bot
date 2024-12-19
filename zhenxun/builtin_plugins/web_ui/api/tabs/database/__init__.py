from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import nonebot
from nonebot.drivers import Driver
from tortoise import Tortoise
from tortoise.exceptions import OperationalError

from zhenxun.configs.config import BotConfig
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.task_info import TaskInfo

from ....base_model import BaseResultModel, QueryModel, Result
from ....utils import authentication
from .models.model import Column, SqlModel, SqlText
from .models.sql_log import SqlLog

router = APIRouter(prefix="/database")


driver: Driver = nonebot.get_driver()


SQL_DICT = {}


SELECT_TABLE_MYSQL_SQL = """
SELECT table_name AS name, table_comment AS `desc`
FROM information_schema.tables
WHERE table_schema = DATABASE();
"""

SELECT_TABLE_SQLITE_SQL = """
SELECT name FROM sqlite_master WHERE type='table';
"""

SELECT_TABLE_PSQL_SQL = """
select a.tablename as name,d.description as desc from pg_tables a
    left join pg_class c on relname=tablename
    left join pg_description d on oid=objoid and objsubid=0 where a.schemaname='public'
"""

SELECT_TABLE_COLUMN_PSQL_SQL = """
SELECT column_name, data_type, character_maximum_length as max_length, is_nullable
FROM information_schema.columns
WHERE table_name = '{}';
"""

SELECT_TABLE_COLUMN_MYSQL_SQL = """
SHOW COLUMNS FROM {};
"""

SELECT_TABLE_COLUMN_SQLITE_SQL = """
PRAGMA table_info({});
"""

type2sql = {
    "mysql": SELECT_TABLE_MYSQL_SQL,
    "sqlite": SELECT_TABLE_SQLITE_SQL,
    "postgres": SELECT_TABLE_PSQL_SQL,
}

type2sql_column = {
    "mysql": SELECT_TABLE_COLUMN_MYSQL_SQL,
    "sqlite": SELECT_TABLE_COLUMN_SQLITE_SQL,
    "postgres": SELECT_TABLE_COLUMN_PSQL_SQL,
}


@driver.on_startup
async def _():
    for plugin in nonebot.get_loaded_plugins():
        module = plugin.name
        sql_list = []
        if plugin.metadata and plugin.metadata.extra:
            sql_list = plugin.metadata.extra.get("sql_list")
        if module in SQL_DICT:
            raise ValueError(f"{module} 常用SQL module 重复")
        if sql_list:
            SqlModel(
                name="",
                module=module,
                sql_list=sql_list,
            )
            SQL_DICT[module] = SqlModel
    if SQL_DICT:
        result = await PluginInfo.filter(module__in=SQL_DICT.keys()).values_list(
            "module", "name"
        )
        module2name = {r[0]: r[1] for r in result}
        for s in SQL_DICT:
            module = SQL_DICT[s].module
            SQL_DICT[s].name = module2name.get(module, module)


@router.get(
    "/get_table_list",
    dependencies=[authentication()],
    response_model=Result[list[dict]],
    response_class=JSONResponse,
    description="获取数据库表",
)
async def _() -> Result[list[dict]]:
    db = Tortoise.get_connection("default")
    sql_type = BotConfig.get_sql_type()
    query = await db.execute_query_dict(type2sql[sql_type])
    return Result.ok(query)


@router.get(
    "/get_table_column",
    dependencies=[authentication()],
    response_model=Result[list[Column]],
    response_class=JSONResponse,
    description="获取表字段",
)
async def _(table_name: str) -> Result[list[Column]]:
    db = Tortoise.get_connection("default")
    sql_type = BotConfig.get_sql_type()
    sql = type2sql_column[sql_type]
    query = await db.execute_query_dict(sql.format(table_name))
    result_list = []
    if sql_type == "sqlite":
        result_list.extend(
            Column(
                column_name=result["name"],
                data_type=result["type"],
                max_length=-1,
                is_nullable="YES" if result["notnull"] == 1 else "NO",
            )
            for result in query
        )
    elif sql_type == "mysql":
        result_list.extend(
            Column(
                column_name=result["Field"],
                data_type=result["Type"],
                max_length=-1,
                is_nullable=result["Null"],
            )
            for result in query
        )
    else:
        result_list.extend(Column(**result) for result in query)
    return Result.ok(result_list)


@router.post(
    "/exec_sql",
    dependencies=[authentication()],
    response_model=Result[list[dict]],
    response_class=JSONResponse,
    description="执行sql",
)
async def _(sql: SqlText, request: Request) -> Result[list[dict]]:
    ip = request.client.host if request.client else "unknown"
    try:
        if sql.sql.lower().startswith("select"):
            db = Tortoise.get_connection("default")
            res = await db.execute_query_dict(sql.sql)
            await SqlLog.add(ip or "0.0.0.0", sql.sql, "")
            return Result.ok(res, "执行成功啦!")
        else:
            result = await TaskInfo.raw(sql.sql)
            await SqlLog.add(ip or "0.0.0.0", sql.sql, str(result))
            return Result.ok(info="执行成功啦!")
    except OperationalError as e:
        await SqlLog.add(ip or "0.0.0.0", sql.sql, str(e), False)
        return Result.warning_(f"sql执行错误: {e}")


@router.post(
    "/get_sql_log",
    dependencies=[authentication()],
    response_model=Result[BaseResultModel],
    response_class=JSONResponse,
    description="sql日志列表",
)
async def _(query: QueryModel) -> Result[BaseResultModel]:
    total = await SqlLog.all().count()
    if total % query.size:
        total += 1
    data = (
        await SqlLog.all()
        .order_by("-id")
        .offset((query.index - 1) * query.size)
        .limit(query.size)
    )
    return Result.ok(BaseResultModel(total=total, data=data))


@router.get(
    "/get_common_sql",
    dependencies=[authentication()],
    response_model=Result[dict],
    response_class=JSONResponse,
    description="常用sql",
)
async def _(plugin_name: str | None = None) -> Result[dict]:
    if plugin_name:
        return Result.ok(SQL_DICT.get(plugin_name))
    return Result.ok(str(SQL_DICT))
