from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="识图",
    description="以图搜图，看破本源",
    usage="""
    识别图片 [二次元图片]
    指令：
        识图 [图片]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="一些工具",
    ).to_dict(),
)
