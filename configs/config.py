from typing import Optional
from pathlib import Path
from .utils import ConfigsManager


# 回复消息名称
NICKNAME: str = "小真寻"

# 数据库（必要）
# 如果填写了bind就不需要再填写后面的字段了#）
# 示例："bind": "postgresql://user:password@127.0.0.1:5432/database"
bind: str = ""  # 数据库连接链接
sql_name: str = "postgresql"
user: str = ""  # 数据用户名
password: str = ""  # 数据库密码
address: str = ""  # 数据库地址
port: str = ""  # 数据库端口
database: str = ""  # 数据库名称

# 代理，例如 "http://127.0.0.1:7890"
SYSTEM_PROXY: Optional[str] = None  # 全局代理


Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")
