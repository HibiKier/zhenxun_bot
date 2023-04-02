from datetime import datetime, timedelta
from typing import Any, Optional

import nonebot
import ujson as json
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from configs.config import Config
from configs.path_config import DATA_PATH

from .models.model import Result, User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

token_file = DATA_PATH / "web_ui" / "token.json"
token_file.parent.mkdir(parents=True, exist_ok=True)
token_data = {"token": []}
if token_file.exists():
    try:
        token_data = json.load(open(token_file, "r", encoding="utf8"))
    except json.JSONDecodeError:
        pass


def get_user(uname: str) -> Optional[User]:
    username = Config.get_config("web-ui", "username")
    password = Config.get_config("web-ui", "password")
    if username and password and uname == username:
        return User(username=username, password=password)


def create_token(user: User, expires_delta: Optional[timedelta] = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    return jwt.encode(
        claims={"sub": user.username, "exp": expire},
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


def authentication():
    # if token not in token_data["token"]:
    def inner(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username, expire = payload.get("sub"), payload.get("exp")
            user = get_user(username)  # type: ignore
            if user is None:
                raise JWTError
        except JWTError:
            raise HTTPException(status_code=400, detail="登录验证失败或已失效, 踢出房间!")

    return Depends(inner)
