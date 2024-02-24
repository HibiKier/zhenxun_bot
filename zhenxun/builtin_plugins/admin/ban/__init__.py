from arclet.alconna import Args
from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Arparma,
    At,
    Match,
    Option,
    Subcommand,
    on_alconna,
    store_true,
)
from nonebot_plugin_saa import Image, Mention, MessageFactory, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.rules import admin_check

from ._data_source import BanManage

base_config = Config.get("ban")

__plugin_meta__ = PluginMetadata(
    name="封禁用户/群组",
    description="你被逮捕了！丢进小黑屋！封禁用户以及群组，屏蔽消息",
    usage="""
    .ban [at] ?[小时] ?[分钟]
    .unban
    示例：.ban @user
    示例：.ban @user 6
    示例：.ban @user 3 10
    示例：.unban @user
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPER_AND_ADMIN,
        admin_level=base_config.get("BAN_LEVEL", 5),
        configs=[
            RegisterConfig(
                key="BAN_LEVEL",
                value=5,
                help="ban/unban所需要的管理员权限等级",
                default_value=5,
                type=int,
            )
        ],
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "ban-console",
        Subcommand(
            "ban",
            Args["user?", [str, At]]["duration?", int],
            Option("-g|--group", Args["group_id", str]),
        ),
        Subcommand(
            "unban",
            Args["user?", [str, At]],
            Option("-g|--group", Args["group_id", str]),
        ),
    ),
    rule=admin_check("ban", "BAN_LEVEL"),
    priority=5,
    block=True,
)

_status_matcher = on_alconna(
    Alconna(
        "ban-status",
        Option("-u|--user", Args["user_id", str]),
        Option("-g|--group", Args["group_id", str]),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)
# TODO: shortcut


@_status_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    user_id: Match[str],
    group_id: Match[str],
):
    _user_id = user_id.result if user_id.available else None
    _group_id = group_id.result if group_id.available else None
    if image := await BanManage.build_ban_image(_user_id, _group_id):
        await Image(image.pic2bs4()).finish(reply=True)
    else:
        await Text("数据为空捏...").finish(reply=True)


@_matcher.assign("ban")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    user: Match[str | At],
    duration: Match[int],
    group_id: Match[str],
):
    user_id = None
    if user.available:
        if isinstance(user.result, At):
            user_id = user.result.target
        else:
            user_id = user.result
    _duration = duration.result * 60 if duration.available else -1
    if gid := session.id3 or session.id2:
        if group_id.available:
            gid = group_id.result
        await BanManage.ban(
            user_id, gid, _duration, session, session.id1 in bot.config.superusers
        )
        logger.info(
            f"管理员Ban",
            arparma.header_result,
            session=session,
            target=f"{gid}:{user_id}",
        )
        await MessageFactory(
            [
                Text("对 "),
                Mention(user_id),  # type: ignore
                Text(f" 狠狠惩戒了一番，一脚踢进了小黑屋!"),
            ]
        ).finish(reply=True)
    elif session.id1 in bot.config.superusers:
        _group_id = group_id.result if group_id.available else None
        await BanManage.ban(user_id, _group_id, _duration, session, True)
        logger.info(
            f"超级用户Ban",
            arparma.header_result,
            session=session,
            target=f"{_group_id}:{user_id}",
        )
        at_msg = user_id if user_id else f"群组:{_group_id}"
        await Text(f"对 {at_msg} 狠狠惩戒了一番，一脚踢进了小黑屋!").finish(reply=True)


@_matcher.assign("unban")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    user: Match[str | At],
    group_id: Match[str],
):
    user_id = None
    if user.available:
        if isinstance(user.result, At):
            user_id = user.result.target
        else:
            user_id = user.result
    if gid := session.id3 or session.id2:
        if group_id.available:
            gid = group_id.result
        await BanManage.unban(
            user_id, gid, session, session.id1 in bot.config.superusers
        )
        logger.info(
            f"管理员UnBan",
            arparma.header_result,
            session=session,
            target=f"{gid}:{user_id}",
        )
        await MessageFactory(
            [
                Text("将 "),
                Mention(user_id),  # type: ignore
                Text(f" 从黑屋中拉了出来并急救了一下!"),
            ]
        ).finish(reply=True)
    elif session.id1 in bot.config.superusers:
        _group_id = group_id.result if group_id.available else None
        await BanManage.unban(user_id, _group_id, session, True)
        logger.info(
            f"超级用户UnBan",
            arparma.header_result,
            session=session,
            target=f"{_group_id}:{user_id}",
        )
        at_msg = user_id if user_id else f"群组:{_group_id}"
        await Text(f"对 {at_msg} 从黑屋中拉了出来并急救了一下!").finish(reply=True)
