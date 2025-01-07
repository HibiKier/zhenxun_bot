from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="鸡汤",
    description="喏，亲手为你煮的鸡汤",
    usage="""
    不喝点什么感觉有点不舒服
    指令：
        鸡汤
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).to_dict(),
)
