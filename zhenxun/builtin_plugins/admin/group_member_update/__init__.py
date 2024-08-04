from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.rules import admin_check, ensure_group

from ._data_source import MemberUpdateManage

__plugin_meta__ = PluginMetadata(
    name="更新群组成员列表",
    description="更新群组成员列表",
    usage="""
    更新群组成员的基本信息
    指令：
        更新群组成员信息
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPER_AND_ADMIN,
        admin_level=1,
    ).dict(),
)


_matcher = on_alconna(
    Alconna("更新群组成员信息"),
    rule=admin_check(1) & ensure_group,
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma):
    if gid := session.id3 or session.id2:
        logger.info("更新群组成员信息", arparma.header_result, session=session)
        await MemberUpdateManage.update(bot, gid)
        await Text("已经成功更新了群组成员信息!").finish(reply=True)
    await Text("群组id为空...").send()


_notice = on_notice(priority=1, block=False)


@_notice.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    # TODO: 其他适配器的加群自动更新群组成员信息
    if str(event.user_id) == bot.self_id:
        await MemberUpdateManage.update(bot, str(event.group_id))
        logger.info(
            f"{NICKNAME}加入群聊更新群组信息",
            "更新群组成员列表",
            session=event.user_id,
            group_id=event.group_id,
        )
