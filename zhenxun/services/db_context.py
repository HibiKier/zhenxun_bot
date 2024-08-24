from nonebot.utils import is_coroutine_callable
from tortoise import Tortoise
from tortoise.connection import connections
from tortoise.models import Model as Model_

from zhenxun.configs.config import BotConfig
from zhenxun.configs.path_config import DATA_PATH

from .log import logger

SCRIPT_METHOD = []
MODELS: list[str] = []
DATABASE_SETTING_FILE = DATA_PATH / "database.json"


class Model(Model_):
    """
    自动添加模块

    Args:
        Model_: Model
    """

    def __init_subclass__(cls, **kwargs):
        MODELS.append(cls.__module__)

        if func := getattr(cls, "_run_script", None):
            SCRIPT_METHOD.append((cls.__module__, func))


async def init():
    if not BotConfig.db_url:
        raise Exception(f"数据库配置为空，请在.env.dev中配置DB_URL...")
    try:
        await Tortoise.init(
            db_url=BotConfig.db_url,
            modules={"models": MODELS},
            timezone="Asia/Shanghai",
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
