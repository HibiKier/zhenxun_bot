import re

import nonebot

# from nonebot.adapters.discord import Adapter as DiscordAdapter
from nonebot.adapters.dodo import Adapter as DoDoAdapter
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter

nonebot.init()


driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)
driver.register_adapter(KaiheilaAdapter)
driver.register_adapter(DoDoAdapter)
# driver.register_adapter(DiscordAdapter)

# nonebot.load_builtin_plugins("echo")
nonebot.load_plugins("zhenxun/builtin_plugins")
nonebot.load_plugins("zhenxun/plugins")

all_plugins = [name.replace(":", ".") for name in nonebot.get_available_plugin_names()]
print("所有插件：", all_plugins)
loaded_plugins = tuple(
    re.sub(r"^zhenxun\.(plugins|builtin_plugins)\.", "", plugin.module_name)
    for plugin in nonebot.get_loaded_plugins()
)
print("已加载插件：", loaded_plugins)

for plugin in all_plugins.copy():
    if plugin.startswith(("platform",)):
        print(f"平台插件：{plugin}")
    elif plugin.endswith(loaded_plugins):
        print(f"已加载插件：{plugin}")
    else:
        print(f"未加载插件：{plugin}")
        continue
    all_plugins.remove(plugin)

if all_plugins:
    print("出现未加载的插件：", all_plugins)
    exit(1)
else:
    print("所有插件均已加载")
