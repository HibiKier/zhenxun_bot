import nonebot

# from nonebot.adapters.discord import Adapter as DiscordAdapter
from nonebot.adapters.dodo import Adapter as DoDoAdapter
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter

from zhenxun.services.db_context import disconnect, init

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)
driver.register_adapter(KaiheilaAdapter)
driver.register_adapter(DoDoAdapter)
# driver.register_adapter(DiscordAdapter)


driver.on_startup(init)
driver.on_shutdown(disconnect)

nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_plugins("zhenxun/builtin_plugins")


if __name__ == "__main__":
    nonebot.run()
