from nonebot.plugin import PluginMetadata

from zhenxun.configs.utils import PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="B站订阅",
    description="非常便利的B站订阅通知",
    usage="""
        usage：
            B站直播，番剧，UP动态开播等提醒
            主播订阅相当于 直播间订阅 + UP订阅
            指令：
                添加订阅 ['主播'/'UP'/'番剧'] [id/链接/番名]
                删除订阅 ['主播'/'UP'/'id'] [id]
                查看订阅
            示例：
                添加订阅主播 2345344 <-(直播房间id)
                添加订阅UP 2355543 <-(个人主页id)
                添加订阅番剧 史莱姆 <-(支持模糊搜索)
                添加订阅番剧 125344 <-(番剧id)
                删除订阅id 2324344 <-(任意id，通过查看订阅获取)
        """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.3-b101fbc",
        superuser_help="""
    登录b站获取cookie防止风控：
            bil_check/检测b站
            bil_login/登录b站
            bil_logout/退出b站 uid
            示例:
                登录b站
                检测b站
                bil_logout 12345<-(退出登录的b站uid，通过检测b站获取)
        """,
    ).to_dict(),
)
