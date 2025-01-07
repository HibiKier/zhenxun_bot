import asyncio
import os
import re

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from nonebot.log import logger

nonebot.init()

from zhenxun.services.db_context import disconnect, init

driver = nonebot.get_driver()

driver.register_adapter(OneBotV11Adapter)


driver.on_startup(init)
driver.on_shutdown(disconnect)


# nonebot.load_builtin_plugins("echo")
nonebot.load_plugins("zhenxun/builtin_plugins")
nonebot.load_plugins("zhenxun/plugins")

all_plugins = [name.replace(":", ".") for name in nonebot.get_available_plugin_names()]
logger.info(f"所有插件：{all_plugins}")
loaded_plugins = tuple(
    re.sub(r"^zhenxun\.(plugins|builtin_plugins)\.", "", plugin.module_name)
    for plugin in nonebot.get_loaded_plugins()
)
logger.info(f"已加载插件：{loaded_plugins}")

for plugin in all_plugins.copy():
    if plugin.startswith(("platform",)):
        logger.info(f"平台插件：{plugin}")
    elif plugin.endswith(loaded_plugins):
        logger.info(f"已加载插件：{plugin}")
    else:
        logger.info(f"未加载插件：{plugin}")
        continue
    all_plugins.remove(plugin)

if all_plugins:
    logger.info(f"出现未加载的插件：{all_plugins}")
    exit(1)
else:
    logger.info("所有插件均已加载")


@driver.on_startup
async def _():
    task = asyncio.create_task(asyncio.sleep(1))
    task.add_done_callback(lambda _: driver._lifespan.on_ready(os._exit(0)))


nonebot.run()
