import nonebot
from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from ._data_source import UpdateManage

__plugin_meta__ = PluginMetadata(
    name="自动更新",
    description="就算是真寻也会成长的",
    usage="""
    usage：
        检查更新真寻最新版本，包括了自动更新
        指令：
            检查更新真寻
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
        configs=[
            RegisterConfig(
                key="UPDATE_REMIND",
                value=True,
                help="是否检测更新版本",
                default_value=True,
            ),
            RegisterConfig(
                key="UPDATE_REMIND",
                value=True,
                help="是否检测更新版本",
                default_value=True,
            ),
        ],
    ).dict(),
)

_matcher = on_alconna(
    Alconna("检查更新", Args["ver_type?", ["main", "dev", "release"]]),
    priority=1,
    block=True,
    permission=SUPERUSER,
)


@_matcher.handle()
async def _(bot: Bot, session: EventSession, ver_type: Match[str]):
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not ver_type.available:
        result = await UpdateManage.check_version()
        logger.info("查看当前版本...", "检查更新", session=session)
        await MessageUtils.build_message(result).finish()
    try:
        result = await UpdateManage.update(bot, session.id1, ver_type.result)
    except Exception as e:
        logger.error("版本更新失败...", "检查更新", session=session, e=e)
        await MessageUtils.build_message(f"更新版本失败...e: {e}").finish()
    if result:
        await MessageUtils.build_message(result).finish()
    await MessageUtils.build_message("更新版本失败...").finish()


# driver = nonebot.get_driver()


# @driver.on_startup
# async def _():
#     result = await UpdateManage.check_version()
#     print("-----------------------")
#     print("-----------------------")
#     print(result)
#     print("-----------------------")
#     print("-----------------------")
#     result = await UpdateManage.update(None, "", "dev")
#     print("-----------------------")
#     print("-----------------------")
#     print(result)
#     print("-----------------------")
#     print("-----------------------")
