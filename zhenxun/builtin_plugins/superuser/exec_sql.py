from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession
from tortoise import Tortoise

from zhenxun.configs.config import BotConfig
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.ban_console import BanConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.image_utils import ImageTemplate
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="数据库操作",
    description="执行sql语句与查看表",
    usage="""
    查看所有表
    exec [sql语句]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).to_dict(),
)

_matcher = on_command(
    "exec",
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_table_matcher = on_command(
    "查看所有表",
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

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
    left join pg_description d on oid=objoid and objsubid=0
    where a.schemaname = 'public'
"""


type2sql = {
    "mysql": SELECT_TABLE_MYSQL_SQL,
    "sqlite": SELECT_TABLE_SQLITE_SQL,
    "postgres": SELECT_TABLE_PSQL_SQL,
}


@_matcher.handle()
async def _(session: EventSession, message: UniMsg):
    sql_text = message.extract_plain_text().strip()
    if sql_text.startswith("exec"):
        sql_text = sql_text[4:].strip()
    if not sql_text:
        await MessageUtils.build_message("需要执行的的SQL语句!").finish()
    logger.info(f"执行SQL语句: {sql_text}", "exec", session=session)
    try:
        if not sql_text.lower().startswith("select"):
            await BanConsole.raw(sql_text)
        else:
            db = Tortoise.get_connection("default")
            res = await db.execute_query_dict(sql_text)
            _column = []
            for r in res:
                if len(r) > len(_column):
                    _column = r.keys()
            data_list = []
            for r in res:
                data = [r.get(c) for c in _column]
                data_list.append(data)
            if not data_list:
                return await MessageUtils.build_message("查询结果为空!").send()
            table = await ImageTemplate.table_page(
                "EXEC", f"总共有 {len(data_list)} 条数据捏", list(_column), data_list
            )
            return await MessageUtils.build_message(table).send()
    except Exception as e:
        logger.error("执行 SQL 语句失败...", session=session, e=e)
        await MessageUtils.build_message(f"执行 SQL 语句失败... {type(e)}").finish()
    await MessageUtils.build_message("执行 SQL 语句成功!").finish()


@_table_matcher.handle()
async def _(session: EventSession):
    try:
        db = Tortoise.get_connection("default")
        sql_type = BotConfig.get_sql_type()
        select_sql = type2sql[sql_type]
        query = await db.execute_query_dict(select_sql)
        column_name = ["表名", "简介"]
        data_list = []
        for table in query:
            data_list.append([table["name"], table.get("desc")])
        logger.info("查看数据库所有表", "查看所有表", session=session)
        table = await ImageTemplate.table_page(
            "数据库表", f"总共有 {len(data_list)} 张表捏", column_name, data_list
        )
        await MessageUtils.build_message(table).send()
    except Exception as e:
        logger.error("获取表数据失败...", session=session, e=e)
        await MessageUtils.build_message(f"获取表数据失败... {type(e)}").send()
