import platform
from pathlib import Path

from .utils import ConfigsManager

if platform.system() == "Linux":
    import os

    hostip = (
        os.popen("cat /etc/resolv.conf | grep nameserver | awk '{ print $2 }'")
        .read()
        .replace("\n", "")
    )


class BotConfigSetting:

    def __init__(self) -> None:
        self.__nickname: str = ""
        self.__system_proxy: str | None = None

    @property
    def nickname(self) -> str:
        return self.__nickname

    @nickname.setter
    def nickname(self, v: str):
        self.__nickname = v

    @property
    def system_proxy(self) -> str | None:
        return self.__system_proxy

    @system_proxy.setter
    def system_proxy(self, v: str):
        self.__system_proxy = v


# 回复消息名称
NICKNAME: str = ""

# 代理，例如 "http://127.0.0.1:7890"
# 如果是WLS 可以 f"http://{hostip}:7890" 使用寄主机的代理
SYSTEM_PROXY: str | None = None  # 全局代理

# 示例："bind": "postgres://user:password@127.0.0.1:5432/database"
bind: str = ""  # 数据库连接链接
sql_name: str = "postgres"
user: str = ""  # 数据用户名
password: str = ""  # 数据库密码
address: str = ""  # 数据库地址
port: str = ""  # 数据库端口
database: str = ""  # 数据库名称

Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")

BotConfig = BotConfigSetting()
