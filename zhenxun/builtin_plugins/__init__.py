from nonebot import require

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_alconna")
require("nonebot_plugin_session")
require("nonebot_plugin_saa")

from nonebot_plugin_saa import enable_auto_select_bot

enable_auto_select_bot()
