from configs.config import Config


Config.add_plugin_config(
    "hook",
    "CHECK_NOTICE_INFO_CD",
    300,
    name="基础hook配置",
    help_="群检测，个人权限检测等各种检测提示信息cd",
    default_value=300
)

Config.add_plugin_config(
    "hook",
    "MALICIOUS_BAN_TIME",
    30,
    help_="恶意命令触发检测触发后ban的时长（分钟）",
    default_value=30
)

Config.add_plugin_config(
    "hook",
    "MALICIOUS_CHECK_TIME",
    5,
    help_="恶意命令触发检测规定时间内（秒）",
    default_value=5
)

Config.add_plugin_config(
    "hook",
    "MALICIOUS_BAN_COUNT",
    6,
    help_="恶意命令触发检测最大触发次数",
    default_value=6
)

