from pathlib import Path
import re

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import nonebot

from zhenxun.configs.config import BotConfig, Config

from ...base_model import Result
from .model import Setting

router = APIRouter(prefix="/configure")

driver = nonebot.get_driver()


@router.post(
    "/set_configure",
    response_model=Result,
    response_class=JSONResponse,
    description="设置基础配置",
)
async def _(setting: Setting) -> Result:
    password = Config.get_config("web-ui", "password")
    if password or BotConfig.db_url:
        raise HTTPException(
            status_code=400, detail="Configuration can only be set once"
        )
    env_file = Path() / ".env.dev"
    if not env_file.exists():
        raise HTTPException(status_code=400, detail="Configuration file not found")
    env_text = env_file.read_text(encoding="utf-8")
    if setting.superusers:
        superusers = ", ".join([f'"{s}"' for s in setting.superusers])
        env_text = re.sub(r"SUPERUSERS=\[.*?\]", f"SUPERUSERS=[{superusers}]", env_text)
    if setting.host:
        env_text = env_text.replace("HOST = 127.0.0.1", f"HOST = {setting.host}")
    if setting.port:
        env_text = env_text.replace("PORT = 8080", f"PORT = {setting.port}")
    if setting.db_url:
        if setting.db_url.startswith("sqlite"):
            db_path = Path(setting.db_url.split(":")[-1])
            db_path.parent.mkdir(parents=True, exist_ok=True)
        env_text.replace('DB_URL = ""', f"DB_URL = {setting.db_url}")
    if setting.username:
        Config.set_config("web-ui", "username", setting.username)
    Config.set_config("web-ui", "password", setting.password)
    env_file.write_text(env_text, encoding="utf-8")
    return Result.ok(info="基础配置设置完成!")
