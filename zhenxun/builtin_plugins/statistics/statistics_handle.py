from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    Option,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import Command, PluginExtraData
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from ._data_source import StatisticsManage

__plugin_meta__ = PluginMetadata(
    name="功能调用统计",
    description="功能调用统计可视化",
    usage="""
    usage：
    功能调用统计可视化
    指令：
        功能调用统计
        日功能调用统计
        周功能调用统计
        月功能调用统计
        我的功能调用统计   : 当前群我的统计
        我的功能调用统计 -g: 我的全局统计
        我的日功能调用统计
        我的周功能调用统计
        我的月功能调用统计
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.NORMAL,
        menu_type="数据统计",
        aliases={"功能调用统计"},
        superuser_help="""
        "全局功能调用统计",
        "全局日功能调用统计",
        "全局周功能调用统计",
        "全局月功能调用统计",
        """.strip(),
        commands=[
            Command(command="功能调用统计"),
            Command(command="日功能调用统计"),
            Command(command="周功能调用统计"),
            Command(command="我的功能调用统计"),
            Command(command="我的日功能调用统计"),
            Command(command="我的周功能调用统计"),
            Command(command="我的月功能调用统计"),
        ],
    ).to_dict(),
)


_matcher = on_alconna(
    Alconna(
        "功能调用统计",
        Args["name?", str],
        Option("-g|--global", action=store_true, help_text="全局统计"),
        Option("-my", action=store_true, help_text="我的"),
        Option("-t|--type", Args["search_type", ["day", "week", "month"]]),
    ),
    priority=5,
    block=True,
)

_matcher.shortcut(
    "日功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "day"],
    prefix=True,
)

_matcher.shortcut(
    "周功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "week"],
    prefix=True,
)

_matcher.shortcut(
    "月功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "month"],
    prefix=True,
)

_matcher.shortcut(
    "全局功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-g"],
    prefix=True,
)

_matcher.shortcut(
    "全局日功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "day", "-g"],
    prefix=True,
)

_matcher.shortcut(
    "全局周功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "week", "-g"],
    prefix=True,
)

_matcher.shortcut(
    "全局月功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "month", "-g"],
    prefix=True,
)

_matcher.shortcut(
    "我的功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-my"],
    prefix=True,
)

_matcher.shortcut(
    "我的日功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "day", "-my"],
    prefix=True,
)

_matcher.shortcut(
    "我的周功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "week", "-my"],
    prefix=True,
)

_matcher.shortcut(
    "我的月功能调用统计(?P<name>.*)",
    command="功能调用统计",
    arguments=["{name}", "-t", "month", "-my"],
    prefix=True,
)


@_matcher.handle()
async def _(
    session: EventSession, arparma: Arparma, name: Match[str], search_type: Match[str]
):
    plugin_name = name.result if name.available else None
    st = search_type.result if search_type.available else None
    gid = session.id3 or session.id2
    uid = session.id1 if (arparma.find("my") or not gid) else None
    is_global = arparma.find("global")
    if uid and is_global:
        """个人全局"""
        gid = None
    if result := await StatisticsManage.get_statistics(
        plugin_name, arparma.find("global"), st, uid, gid
    ):
        if isinstance(result, str):
            await MessageUtils.build_message(result).finish(reply_to=True)
        else:
            await MessageUtils.build_message(result).send()
    else:
        await MessageUtils.build_message("获取数据失败...").send()
