from pathlib import Path

import nonebot

from zhenxun.configs.config import Config

Config.add_plugin_config(
    "alapi",
    "ALAPI_TOKEN",
    None,
    help="在https://admin.alapi.cn/user/login登录后获取token",
)

nonebot.load_plugins(str(Path(__file__).parent.resolve()))
