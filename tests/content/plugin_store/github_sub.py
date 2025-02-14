from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="github订阅",
    description="订阅github用户或仓库",
    usage="""
    usage：
        github新Comment，PR，Issue等提醒
    指令：
        添加github ['用户'/'仓库'] [用户名/{owner/repo}]
        删除github [用户名/{owner/repo}]
        查看github
        示例：添加github订阅 用户 HibiKier
        示例：添加gb订阅 仓库 HibiKier/zhenxun_bot
        示例：添加github 用户 HibiKier
        示例：删除gb订阅 HibiKier
    """.strip(),
    extra=PluginExtraData(
        author="xuanerwa",
        version="0.7",
    ).to_dict(),
)
