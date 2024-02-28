from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.platform import PlatformManage

__plugin_meta__ = PluginMetadata(
    name="更新群组/好友信息",
    description="更新群组/好友信息",
    usage="""
    更新群组信息
    更新好友信息
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)


_group_matcher = on_alconna(
    Alconna(
        "更新群组信息",
    ),
    permission=SUPERUSER,
    rule=to_me(),
    priority=1,
    block=True,
)

_friend_matcher = on_alconna(
    Alconna(
        "更新好友信息",
    ),
    permission=SUPERUSER,
    rule=to_me(),
    priority=1,
    block=True,
)


@_group_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
):
    try:
        num = await PlatformManage.update_group(bot)
        logger.info(
            f"更新群聊信息完成，共更新了 {num} 个群组的信息!",
            arparma.header_result,
            session=session,
        )
        await Text(f"成功更新了 {num} 个群组的信息").send()
    except Exception as e:
        logger.error(
            "更新群组信息发生错误", arparma.header_result, session=session, e=e
        )
        await Text("其他未知错误...").send()


@_friend_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
):
    try:
        num = await PlatformManage.update_friend(bot, session.platform)
        logger.info(
            f"更新好友信息完成，共更新了 {num} 个好友的信息!",
            arparma.header_result,
            session=session,
        )
        await Text(f"成功更新了 {num} 个好友的信息").send()
    except Exception as e:
        logger.error(
            "更新好友信息发生错误", arparma.header_result, session=session, e=e
        )
        await Text("其他未知错误...").send()
