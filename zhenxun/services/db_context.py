import ujson as json
from nonebot.utils import is_coroutine_callable
from tortoise import Tortoise
from tortoise.connection import connections
from tortoise.models import Model as Model_

from zhenxun.configs.config import (
    address,
    bind,
    database,
    password,
    port,
    sql_name,
    user,
)
from zhenxun.configs.path_config import DATA_PATH

from .log import logger

SCRIPT_METHOD = []
MODELS: list[str] = []
DATABASE_SETTING_FILE = DATA_PATH / "database.json"


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


async def init():
    if DATABASE_SETTING_FILE.exists():
        with open(DATABASE_SETTING_FILE, "r", encoding="utf-8") as f:
            setting_data = json.load(f)
    else:
        i_bind = bind
        if not i_bind and any([user, password, address, port, database]):
            i_bind = f"{sql_name}://{user}:{password}@{address}:{port}/{database}"
        setting_data = {
            "bind": i_bind,
            "sql_name": sql_name,
            "user": user,
            "password": password,
            "address": address,
            "port": port,
            "database": database,
        }
        with open(DATABASE_SETTING_FILE, "w", encoding="utf-8") as f:
            json.dump(setting_data, f, ensure_ascii=False, indent=4)
    i_bind = setting_data.get("bind")
    _sql_name = setting_data.get("sql_name")
    _user = setting_data.get("user")
    _password = setting_data.get("password")
    _address = setting_data.get("address")
    _port = setting_data.get("port")
    _database = setting_data.get("database")
    if not i_bind and not any([_user, _password, _address, _port, _database]):
        raise ValueError("\n数据库配置未填写...")
    if not i_bind:
        i_bind = f"{_sql_name}://{_user}:{_password}@{_address}:{_port}/{_database}"
    try:
        await Tortoise.init(
            db_url=i_bind, modules={"models": MODELS}, timezone="Asia/Shanghai"
        )
        if SCRIPT_METHOD:
            db = Tortoise.get_connection("default")
            logger.debug(
                f"即将运行SCRIPT_METHOD方法, 合计 <u><y>{len(SCRIPT_METHOD)}</y></u> 个..."
            )
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
                    await db.execute_query_dict(sql)
                    # await TestSQL.raw(sql)
                except Exception as e:
                    logger.debug(f"执行SQL: {sql} 错误...", e=e)
            if sql_list:
                logger.debug("SCRIPT_METHOD方法执行完毕!")
        await Tortoise.generate_schemas()
        logger.info(f"Database loaded successfully!")
    except Exception as e:
        raise Exception(f"数据库连接错误... e:{e}")


async def disconnect():
    await connections.close_all()
