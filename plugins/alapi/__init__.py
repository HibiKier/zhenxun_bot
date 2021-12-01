from configs.config import Config
import nonebot


Config.add_plugin_config(
    "alapi",
    "ALAPI_TOKEN",
    None,
    help_="在https://admin.alapi.cn/user/login登录后获取token"
)


nonebot.load_plugins("plugins/alapi")

