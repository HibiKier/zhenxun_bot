from configs.config import Config
import nonebot


Config.add_plugin_config(
    "admin_bot_manage:custom_welcome_message",
    "SET_GROUP_WELCOME_MESSAGE_LEVEL [LEVEL]",
    2,
    name="群管理员操作",
    help_="设置群欢迎消息权限",
    default_value=2,
)

Config.add_plugin_config(
    "admin_bot_manage:switch_rule",
    "CHANGE_GROUP_SWITCH_LEVEL [LEVEL]",
    2,
    help_="开关群功能权限",
    default_value=2,
)

Config.add_plugin_config(
    "admin_bot_manage",
    "ADMIN_DEFAULT_AUTH",
    5,
    help_="默认群管理员权限",
    default_value=5
)

nonebot.load_plugins("basic_plugins/admin_bot_manage")
