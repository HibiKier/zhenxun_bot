from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from zhenxun.services.log import logger

from ..config import PUBLIC_PATH
from .data_source import COMMAND_NAME, update_webui_assets

router = APIRouter()


@router.get("/")
async def index():
    return FileResponse(PUBLIC_PATH / "index.html")


@router.get("/favicon.ico")
async def favicon():
    return FileResponse(PUBLIC_PATH / "favicon.ico")


@router.get("/79edfa81f3308a9f.jfif")
async def _():
    return FileResponse(PUBLIC_PATH / "79edfa81f3308a9f.jfif")


async def init_public(app: FastAPI):
    try:
        if not PUBLIC_PATH.exists():
            folders = await update_webui_assets()
        else:
            folders = [x.name for x in PUBLIC_PATH.iterdir() if x.is_dir()]
        app.include_router(router)
        for pathname in folders:
            logger.debug(f"挂载文件夹: {pathname}")
            app.mount(
                f"/{pathname}",
                StaticFiles(directory=PUBLIC_PATH / pathname, check_dir=True),
                name=f"public_{pathname}",
            )
    except Exception as e:
        logger.error("初始化 WebUI资源 失败", COMMAND_NAME, e=e)
