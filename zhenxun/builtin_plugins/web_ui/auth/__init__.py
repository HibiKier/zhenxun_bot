from datetime import timedelta
import json

import aiofiles
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import nonebot

from zhenxun.configs.config import Config

from ..base_model import Result
from ..utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_token,
    get_user,
    token_data,
    token_file,
)

app = nonebot.get_app()


router = APIRouter()


@router.post("/login")
async def login_get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = Config.get_config("web-ui", "username")
    password = Config.get_config("web-ui", "password")
    if not username or not password:
        return Result.fail("你滴配置文件里用户名密码配置项为空", 998)
    if username != form_data.username or str(password) != form_data.password:
        return Result.fail("真笨, 账号密码都能记错!", 999)
    user = get_user(form_data.username)
    if not user:
        return Result.fail("用户不存在...", 997)
    access_token = create_token(
        user=user,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    token_data["token"].append(access_token)
    if len(token_data["token"]) > 3:
        token_data["token"] = token_data["token"][1:]
    async with aiofiles.open(token_file, "w", encoding="utf8") as f:
        await f.write(json.dumps(token_data, ensure_ascii=False, indent=4))
    return Result.ok(
        {"access_token": access_token, "token_type": "bearer"}, "欢迎回家, 欧尼酱!"
    )
