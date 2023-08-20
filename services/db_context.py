from typing import List

from nonebot.utils import is_coroutine_callable
from tortoise import Tortoise, fields
from tortoise.connection import connections
from tortoise.models import Model as Model_
from tortoise.queryset import RawSQLQuery

from configs.config import address, bind, database, password, port, sql_name, user
from utils.text_utils import prompt2cn

from .log import logger

MODELS: List[str] = []

SCRIPT_METHOD = []


class Model(Model_):
    """
    自动添加模块

    Args:
        Model_ (_type_): _description_
    """

    def __init_subclass__(cls, **kwargs):
        MODELS.append(cls.__module__)

        if func := getattr(cls, "_run_script", None):
            SCRIPT_METHOD.append((cls.__module__, func))


class TestSQL(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""

    class Meta:
        table = "test_sql"
        table_description = "执行SQL命令，不记录任何数据"


async def init():
    if not bind and not any([user, password, address, port, database]):
        raise ValueError("\n" + prompt2cn("数据库配置未填写", 28))
    i_bind = bind
    if not i_bind:
        i_bind = f"{sql_name}://{user}:{password}@{address}:{port}/{database}"
    try:
        await Tortoise.init(
            db_url=i_bind, modules={"models": MODELS}, timezone="Asia/Shanghai"
        )
        await Tortoise.generate_schemas()
        logger.info(f"Database loaded successfully!")
    except Exception as e:
        raise Exception(f"数据库连接错误.... {type(e)}: {e}")
    if SCRIPT_METHOD:
        logger.debug(f"即将运行SCRIPT_METHOD方法, 合计 <u><y>{len(SCRIPT_METHOD)}</y></u> 个...")
        sql_list = []
        for module, func in SCRIPT_METHOD:
            try:
                if is_coroutine_callable(func):
                    sql = await func()
                else:
                    sql = func()
                if sql:
                    sql_list += sql

            except Exception as e:
                logger.debug(f"{module} 执行SCRIPT_METHOD方法出错...", e=e)
        for sql in sql_list:
            logger.debug(f"执行SQL: {sql}")
            try:
                await TestSQL.raw(sql)
            except Exception as e:
                logger.debug(f"执行SQL: {sql} 错误...", e=e)


async def disconnect():
    await connections.close_all()
