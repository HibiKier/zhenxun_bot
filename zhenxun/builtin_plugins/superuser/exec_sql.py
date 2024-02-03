from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaQuery,
    Args,
    Arparma,
    Match,
    Option,
    Query,
    on_alconna,
    store_true,
)
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession
from tortoise import Tortoise

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.db_context import TestSQL
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

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
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "exec",
        Args["sql?", str],
        Option("-l|--list", action=store_true, help_text="查看数据表"),
    ),
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
    block=True,
)


@_matcher.handle()
async def _(
    sql: Match[str],
    session: EventSession,
    arparma: Arparma,
    query_list: Query[bool] = AlconnaQuery("list.value", False),
):
    db = Tortoise.get_connection("default")
    if query_list.result:
        query = await db.execute_query_dict(
            "select tablename from pg_tables where schemaname = 'public'"
        )
        msg = "数据库中的所有表名：\n"
        for tablename in query:
            msg += str(tablename["tablename"]) + "\n"
        logger.info("查看数据库所有表", arparma.header_result, session=session)
        await Text(msg[:-1]).finish()
    else:
        if not sql.available:
            await Text("必须带有需要执行的 SQL 语句...").finish()
        sql_text = sql.result
        if not sql_text.lower().startswith("select"):
            await TestSQL.raw(sql_text)
            await Text("执行 SQL 语句成功!").finish()
        else:
            res = await db.execute_query_dict(sql_text)
            # TODO: Alconna空格sql无法接收
