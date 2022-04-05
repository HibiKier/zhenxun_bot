from configs.config import Config as gConfig
from .api import *
from .auth import *


gConfig.add_plugin_config(
    "web-ui",
    "username",
    "admin",
    name="web-ui",
    help_="前端管理用户名"
)

gConfig.add_plugin_config(
    "web-ui",
    "password",
    None,
    name="web-ui",
    help_="前端管理密码"
)
