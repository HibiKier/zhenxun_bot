import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from services.db_context import init, disconnect

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config
driver.on_startup(init)
driver.on_shutdown(disconnect)
nonebot.load_builtin_plugins()
nonebot.load_plugins("plugins")
nonebot.load_plugins("plugins/shop")
nonebot.load_plugins("plugins/genshin")
nonebot.load_plugins("plugins/alapi")
nonebot.load_plugins("plugins/pix_gallery")


if __name__ == "__main__":
    nonebot.run()
