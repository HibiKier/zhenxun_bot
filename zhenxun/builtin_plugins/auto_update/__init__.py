from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Match,
    Option,
    Query,
    on_alconna,
    store_true,
)
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.manager.resource_manager import (
    DownloadResourceException,
    ResourceManager,
)
from zhenxun.utils.message import MessageUtils

from ._data_source import UpdateManage

__plugin_meta__ = PluginMetadata(
    name="自动更新",
    description="就算是真寻也会成长的",
    usage="""
    usage：
        检查更新真寻最新版本，包括了自动更新
        资源文件大小一般在130mb左右，除非必须更新一般仅更新代码文件
        指令：
            检查更新 [main|release] ?[-r]
            -r: 下载资源文件
            示例:
            检查更新 main
            检查更新 main -r
            检查更新 release -r
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)

_matcher = on_alconna(
    Alconna(
        "检查更新",
        Args["ver_type?", ["main", "release"]],
        Option("-r|--resource", action=store_true, help_text="下载资源文件"),
    ),
    priority=1,
    block=True,
    permission=SUPERUSER,
    rule=to_me(),
)


@_matcher.handle()
async def _(
    bot: Bot,
    session: Uninfo,
    ver_type: Match[str],
    resource: Query[bool] = Query("resource", False),
):
    result = ""
    if not ver_type.available:
        result = await UpdateManage.check_version()
        logger.info("查看当前版本...", "检查更新", session=session)
        await MessageUtils.build_message(result).finish()
    try:
        result = await UpdateManage.update(bot, session.user.id, ver_type.result)
    except Exception as e:
        logger.error("版本更新失败...", "检查更新", session=session, e=e)
        await MessageUtils.build_message(f"更新版本失败...e: {e}").finish()
    if resource.result:
        try:
            await ResourceManager.init_resources(True)
        except DownloadResourceException:
            result += "\n资源更新下载失败..."
        except Exception as e:
            logger.error("资源更新下载失败...", "检查更新", session=session, e=e)
            result += "\n资源更新未知错误..."
    if result:
        await MessageUtils.build_message(result).finish()
    await MessageUtils.build_message("更新版本失败...").finish()
