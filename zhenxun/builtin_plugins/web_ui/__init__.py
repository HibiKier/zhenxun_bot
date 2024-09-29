import asyncio
import secrets

import nonebot
from fastapi import FastAPI, APIRouter
from nonebot.plugin import PluginMetadata
from nonebot.log import default_filter, default_format

from zhenxun.utils.enum import PluginType
from zhenxun.services.log import logger, logger_
from zhenxun.configs.config import Config as gConfig
from zhenxun.configs.utils import RegisterConfig, PluginExtraData

from .public import init_public
from .auth import router as auth_router
from .api.logs import router as ws_log_routes
from .api.logs.log_manager import LOG_STORAGE
from .api.tabs.main import router as main_router
from .api.tabs.manage import router as manage_router
from .api.tabs.system import router as system_router
from .api.tabs.main import ws_router as status_routes
from .api.tabs.database import router as database_router
from .api.tabs.dashboard import router as dashboard_router
from .api.tabs.manage.chat import ws_router as chat_routes
from .api.tabs.plugin_manage import router as plugin_router
from .api.tabs.plugin_manage.store import router as store_router

__plugin_meta__ = PluginMetadata(
    name="WebUi",
    description="WebUi API",
    usage="""
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        configs=[
            RegisterConfig(
                module="web-ui",
                key="username",
                value="admin",
                help="前端管理用户名",
                type=str,
                default_value="admin",
            ),
            RegisterConfig(
                module="web-ui",
                key="password",
                value=None,
                help="前端管理密码",
                type=str,
                default_value=None,
            ),
            RegisterConfig(
                module="web-ui",
                key="secret",
                value=secrets.token_urlsafe(32),
                help="JWT密钥",
                type=str,
                default_value=None,
            ),
        ],
    ).dict(),
)

driver = nonebot.get_driver()


gConfig.set_name("web-ui", "web-ui")


BaseApiRouter = APIRouter(prefix="/zhenxun/api")


BaseApiRouter.include_router(auth_router)
BaseApiRouter.include_router(store_router)
BaseApiRouter.include_router(dashboard_router)
BaseApiRouter.include_router(main_router)
BaseApiRouter.include_router(manage_router)
BaseApiRouter.include_router(database_router)
BaseApiRouter.include_router(plugin_router)
BaseApiRouter.include_router(system_router)


WsApiRouter = APIRouter(prefix="/zhenxun/socket")

WsApiRouter.include_router(ws_log_routes)
WsApiRouter.include_router(status_routes)
WsApiRouter.include_router(chat_routes)


@driver.on_startup
async def _():
    try:

        async def log_sink(message: str):
            loop = None
            if not loop:
                try:
                    loop = asyncio.get_running_loop()
                except Exception as e:
                    logger.warning("Web Ui log_sink", e=e)
            if not loop:
                loop = asyncio.new_event_loop()
            loop.create_task(LOG_STORAGE.add(message.rstrip("\n")))  # noqa: RUF006

        logger_.add(
            log_sink, colorize=True, filter=default_filter, format=default_format
        )

        app: FastAPI = nonebot.get_app()
        app.include_router(BaseApiRouter)
        app.include_router(WsApiRouter)
        await init_public(app)
        logger.info("<g>API启动成功</g>", "Web UI")
    except Exception as e:
        logger.error("<g>API启动失败</g>", "Web UI", e=e)
