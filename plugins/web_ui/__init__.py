from configs.config import Config as gConfig
from .api import *
from .auth import *
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, IgnoredException
from utils.manager import plugins2settings_manager
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageEvent


gConfig.add_plugin_config("web-ui", "username", "admin", name="web-ui", help_="前端管理用户名")

gConfig.add_plugin_config("web-ui", "password", None, name="web-ui", help_="前端管理密码")


# 使用webui访问api后plugins2settings中的cmd字段将从list变为str
# 暂时找不到原因
# 先使用hook修复
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    flag = False
    for module in plugins2settings_manager.keys():
        if plugins2settings_manager.get_plugin_data(module).cmd and isinstance(
            plugins2settings_manager.get_plugin_data(module).cmd, str
        ):
            plugins2settings_manager[module].cmd = plugins2settings_manager[
                module
            ].cmd.split(",")
            flag = True
    if flag:
        plugins2settings_manager.save()
