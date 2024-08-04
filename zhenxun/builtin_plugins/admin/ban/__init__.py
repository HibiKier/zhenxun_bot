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
    name="Ban",
    description="你被逮捕了！丢进小黑屋！封禁用户以及群组，屏蔽消息",
    usage="""
    普通管理员
        格式:
        ban [At用户] -t [时长(分钟)]

        示例:
        ban @用户          : 永久拉黑用户
        ban @用户 -t 100   : 拉黑用户100分钟
        unban @用户        : 从小黑屋中拉出来
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPER_AND_ADMIN,
        superuser_help="""
        超级管理员额外命令
        格式:
        ban [At用户/用户Id] [时长]
        ban列表: 获取所有Ban数据

        群组ban列表: 获取群组Ban数据
        用户ban列表: 获取用户Ban数据

        ban列表 -u [用户Id]: 查找指定用户ban数据
        ban列表 -g [群组Id]: 查找指定群组ban数据
        示例:
            ban列表 -u 123456789    : 查找用户123456789的ban数据
            ban列表 -g 123456789    : 查找群组123456789的ban数据

        私聊下:
            示例:
            ban 123456789          : 永久拉黑用户123456789
            ban 123456789 -t 100   : 拉黑用户123456789 100分钟

            ban -g 999999              : 拉黑群组为999999的群组
            ban -g 999999 -t 100       : 拉黑群组为999999的群组 100分钟

            unban 123456789     : 从小黑屋中拉出来
            unban -g 999999     : 将群组9999999从小黑屋中拉出来
        """,
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


_ban_matcher = on_alconna(
    Alconna(
        "ban",
        Args["user?", [str, At]],
        Option("-g|--group", Args["group_id", str]),
        Option("-t|--time", Args["duration", int]),
    ),
    rule=admin_check("ban", "BAN_LEVEL"),
    priority=5,
    block=True,
)

_unban_matcher = on_alconna(
    Alconna(
        "unban",
        Args["user?", [str, At]],
        Option("-g|--group", Args["group_id", str]),
    ),
    rule=admin_check("ban", "BAN_LEVEL"),
    priority=5,
    block=True,
)

_status_matcher = on_alconna(
    Alconna(
        "ban列表",
        Option("-u", Args["user_id", str], help_text="查找用户"),
        Option("-g", Args["group_id", str], help_text="查找群组"),
        Option("--user", action=store_true, help_text="过滤用户"),
        Option("--group", action=store_true, help_text="过滤群组"),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_status_matcher.shortcut(
    "用户ban列表",
    command="ban列表",
    arguments=["--user"],
    prefix=True,
)

_status_matcher.shortcut(
    "群组ban列表",
    command="ban列表",
    arguments=["--group"],
    prefix=True,
)


@_status_matcher.handle()
async def _(
    arparma: Arparma,
    user_id: Match[str],
    group_id: Match[str],
):
    filter_type = None
    if arparma.find("user"):
        filter_type = "user"
    if arparma.find("group"):
        filter_type = "group"
    _user_id = user_id.result if user_id.available else None
    _group_id = group_id.result if group_id.available else None
    if image := await BanManage.build_ban_image(filter_type, _user_id, _group_id):
        await Image(image.pic2bytes()).finish(reply=True)
    else:
        await Text("数据为空捏...").finish(reply=True)


@_ban_matcher.handle()
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
            if session.id1 not in bot.config.superusers:
                await Text("权限不足捏...").finish(reply=True)
            user_id = user.result
    _duration = duration.result * 60 if duration.available else -1
    if (gid := session.id3 or session.id2) and not group_id.available:
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
                Mention(user_id) if isinstance(user.result, At) else Text(user_id),  # type: ignore
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


@_unban_matcher.handle()
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
            if session.id1 not in bot.config.superusers:
                await Text("权限不足捏...").finish(reply=True)
            user_id = user.result
    if gid := session.id3 or session.id2:
        if group_id.available:
            gid = group_id.result
        if await BanManage.unban(
            user_id, gid, session, session.id1 in bot.config.superusers
        ):
            logger.info(
                f"管理员UnBan",
                arparma.header_result,
                session=session,
                target=f"{gid}:{user_id}",
            )
            await MessageFactory(
                [
                    Text("将 "),
                    Mention(user_id) if isinstance(user.result, At) else Text(user_id),  # type: ignore
                    Text(f" 从黑屋中拉了出来并急救了一下!"),
                ]
            ).finish(reply=True)
        else:
            await Text(f"该用户不在黑名单中捏...").finish(reply=True)
    elif session.id1 in bot.config.superusers:
        _group_id = group_id.result if group_id.available else None
        if await BanManage.unban(user_id, _group_id, session, True):
            logger.info(
                f"超级用户UnBan",
                arparma.header_result,
                session=session,
                target=f"{_group_id}:{user_id}",
            )
            at_msg = user_id if user_id else f"群组:{_group_id}"
            await Text(f"对 {at_msg} 从黑屋中拉了出来并急救了一下!").finish(reply=True)
        else:
            await Text(f"该用户不在黑名单中捏...").finish(reply=True)
