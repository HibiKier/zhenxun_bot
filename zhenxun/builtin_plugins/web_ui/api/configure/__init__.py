from pathlib import Path
import re
import subprocess
import sys

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import nonebot

from zhenxun.configs.config import BotConfig, Config

from ...base_model import Result
from .data_source import test_db_connection
from .model import Setting

router = APIRouter(prefix="/configure")

driver = nonebot.get_driver()

port = driver.config.port


flag_file = Path() / ".configure_restart"


@router.post(
    "/set_configure",
    response_model=Result,
    response_class=JSONResponse,
    description="设置基础配置",
)
async def _(setting: Setting) -> Result:
    global port
    password = Config.get_config("web-ui", "password")
    if password or BotConfig.db_url:
        return Result.fail("配置已存在，请先删除DB_URL内容和前端密码再进行设置。")
    env_file = Path() / ".env.dev"
    if not env_file.exists():
        return Result.fail("配置文件.env.dev不存在。")
    env_text = env_file.read_text(encoding="utf-8")
    if setting.superusers:
        superusers = ", ".join([f'"{s}"' for s in setting.superusers])
        env_text = re.sub(r"SUPERUSERS=\[.*?\]", f"SUPERUSERS=[{superusers}]", env_text)
    if setting.host:
        env_text = env_text.replace("HOST = 127.0.0.1", f"HOST = {setting.host}")
    if setting.port:
        env_text = env_text.replace("PORT = 8080", f"PORT = {setting.port}")
        port = setting.port
    if setting.db_url:
        if setting.db_url.startswith("sqlite"):
            db_path = Path(setting.db_url.split(":")[-1])
            db_path.parent.mkdir(parents=True, exist_ok=True)
        env_text = env_text.replace('DB_URL = ""', f'DB_URL = "{setting.db_url}"')
    if setting.username:
        Config.set_config("web-ui", "username", setting.username)
    Config.set_config("web-ui", "password", setting.password, True)
    env_file.write_text(env_text, encoding="utf-8")
    flag_file.touch()
    return Result.ok(info="设置成功，请重启真寻以完成配置！")


@router.get(
    "/test_db",
    response_model=Result,
    response_class=JSONResponse,
    description="设置基础配置",
)
async def _(db_url: str) -> Result:
    result = await test_db_connection(db_url)
    if isinstance(result, str):
        return Result.fail(result)
    return Result.ok(info="数据库连接成功!")


@router.post(
    "/restart",
    response_model=Result,
    response_class=JSONResponse,
    description="重启",
)
async def _() -> Result:
    if not flag_file.exists():
        return Result.fail("重启标志文件不存在...")
    flag_file.unlink()
    bat_path = Path() / "win启动.bat"
    subprocess.Popen([bat_path, str(port)], shell=True)  # noqa: ASYNC220

    # 退出当前进程
    sys.exit(0)
