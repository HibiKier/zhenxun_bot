from configs.config import Config
import nonebot

Config.add_plugin_config(
    "word_bank",
    "WORD_BANK_LEVEL [LEVEL]",
    5,
    name="词库问答",
    help_="设置增删词库的权限等级",
    default_value=5
)

Config.add_plugin_config(
    "word_bank",
    "WORD_BANK_FUZZY",
    False,
    help_="模糊匹配",
    default_value=False
)
Config.add_plugin_config(
    "word_bank",
    "WORD_BANK_KEY",
    True,
    help_="关键字匹配",
    default_value=True
)
Config.add_plugin_config(
    "word_bank",
    "WORD_BANK_MIX",
    25,
    help_="查看词条时图片内最多显示条数",
    default_value=25
)
nonebot.load_plugins("plugins/word_bank")
