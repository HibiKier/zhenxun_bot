from tortoise import Tortoise

from zhenxun.configs.config import BotConfig

from .models.model import Column

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


class ApiDataSource:
    SQL_DICT = {}  # noqa: RUF012

    @classmethod
    async def get_table_column(cls, table_name: str) -> list[Column]:
        """获取表字段信息

        参数:
            table_name: 表名

        返回:
            list[Column]: 字段数据
        """
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
        return result_list
