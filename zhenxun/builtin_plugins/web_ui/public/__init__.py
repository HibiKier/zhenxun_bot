from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from zhenxun.services.log import logger

from .config import PUBLIC_PATH
from .data_source import update_webui_assets

router = APIRouter()


@router.get("/")
async def index():
    return FileResponse(PUBLIC_PATH / "index.html")


@router.get("/favicon.ico")
async def favicon():
    return FileResponse(PUBLIC_PATH / "favicon.ico")


async def init_public(app: FastAPI):
    try:
        if not PUBLIC_PATH.exists():
            await update_webui_assets()
        app.include_router(router)
        for pathname in ["css", "js", "fonts", "img"]:
            app.mount(
                f"/{pathname}",
                StaticFiles(directory=PUBLIC_PATH / pathname, check_dir=True),
                name=f"public_{pathname}",
            )
    except Exception as e:
        logger.error(f"初始化 web ui assets 失败", "Web UI assets", e=e)
