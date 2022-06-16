import json
from datetime import datetime, timedelta
from configs.path_config import DATA_PATH
from typing import Optional
from starlette import status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from configs.config import Config
from jose import JWTError, jwt
import nonebot

from ..config import Result

app = nonebot.get_app()


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="webui/login")


token_file = DATA_PATH / "web_ui" / "token.json"
token_file.parent.mkdir(parents=True, exist_ok=True)
token_data = {"token": []}
if token_file.exists():
    token_data = json.load(open(token_file, 'r', encoding='utf8'))


class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# USER_LIST = [
#     User(username="admin", password="123")
# ]


def get_user(uname: str) -> Optional[User]:
    username = Config.get_config("web-ui", "username")
    password = Config.get_config("web-ui", "password")
    if username and password and uname == username:
        return User(username=username, password=password)


form_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_token(user: User, expires_delta: Optional[timedelta] = None):
    expire = datetime.utcnow() + expires_delta or timedelta(minutes=15)
    return jwt.encode(
        claims={"sub": user.username, "exp": expire},
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


@app.post("/webui/login")
async def login_get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: User = get_user(form_data.username)
    if not user or user.password != form_data.password:
        raise form_exception
    access_token = create_token(user=user, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    token_data["token"].append(access_token)
    if len(token_data["token"]) > 3:
        token_data["token"] = token_data["token"][1:]
    with open(token_file, 'w', encoding="utf8") as f:
        json.dump(token_data, f, ensure_ascii=False, indent=4)
    return {"access_token": access_token, "token_type": "bearer"}


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@app.post("/webui/auth")
def token_to_user(token: str = Depends(oauth2_scheme)):
    if token not in token_data["token"]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username, expire = payload.get("sub"), payload.get("exp")
            user = get_user(username)
            if user is None:
                raise JWTError
        except JWTError:
            return Result(code=401)
    return Result(code=200, data="ok")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
