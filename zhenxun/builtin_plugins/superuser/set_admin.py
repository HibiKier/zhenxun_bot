from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    At,
    Match,
    Option,
    Subcommand,
    on_alconna,
)
from nonebot_plugin_session import EventSession, SessionLevel

from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.level_user import LevelUser
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="用户权限管理",
    description="设置用户权限",
    usage="""
    权限设置 add [level: 权限等级] [at: at对象或用户id] ?[-g gid: 群组]
    权限设置 delete [at: at对象或用户id]  ?[-g gid: 群组]

    添加权限 5 @user
    权限设置 add 5 422 -g 352352

    删除权限 @user
    删除权限 1234123 -g 123123

    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).to_dict(),
)


_matcher = on_alconna(
    Alconna(
        "权限设置",
        Subcommand(
            "add",
            Args["level", int]["uid", [str, At]],
            help_text="添加权限",
        ),
        Subcommand("delete", Args["uid", [str, At]], help_text="删除权限"),
        Option("-g|--group", Args["gid", str], help_text="指定群组"),
    ),
    permission=SUPERUSER,
    priority=5,
    block=True,
)

_matcher.shortcut(
    "添加权限",
    command="权限设置",
    arguments=["add", "{%0}"],
    prefix=True,
)

_matcher.shortcut(
    "删除权限",
    command="权限设置",
    arguments=["delete", "{%0}"],
    prefix=True,
)


@_matcher.assign("add")
async def _(
    session: EventSession,
    arparma: Arparma,
    level: int,
    gid: Match[str],
    uid: str | At,
):
    group_id = gid.result if gid.available else session.id3 or session.id2
    if group_id:
        if isinstance(uid, At):
            uid = uid.target
        user = await LevelUser.get_or_none(user_id=uid, group_id=group_id)
        old_level = user.user_level if user else 0
        await LevelUser.set_level(uid, group_id, level, 1)
        logger.info(
            f"修改权限: {old_level} -> {level}", arparma.header_result, session=session
        )
        if session.level in [SessionLevel.LEVEL2, SessionLevel.LEVEL3]:
            await MessageUtils.build_message(
                [
                    "成功为 ",
                    At(flag="user", target=uid),
                    f" 设置权限：{old_level} -> {level}",
                ]
            ).finish(reply_to=True)
        await MessageUtils.build_message(
            f"成功为 \n群组：{group_id}\n用户：{uid} \n"
            f"设置权限!\n权限：{old_level} -> {level}"
        ).finish()
    await MessageUtils.build_message("设置权限时群组不能为空...").finish()


@_matcher.assign("delete")
async def _(
    session: EventSession,
    arparma: Arparma,
    gid: Match[str],
    uid: str | At,
):
    group_id = gid.result if gid.available else session.id3 or session.id2
    if group_id:
        if isinstance(uid, At):
            uid = uid.target
        if user := await LevelUser.get_or_none(user_id=uid, group_id=group_id):
            await user.delete()
            if session.level in [SessionLevel.LEVEL2, SessionLevel.LEVEL3]:
                logger.info(
                    f"删除权限: {user.user_level} -> 0",
                    arparma.header_result,
                    session=session,
                )
                await MessageUtils.build_message(
                    ["成功删除 ", At(flag="user", target=uid), " 的权限等级!"]
                ).finish(reply_to=True)
            logger.info(
                f"删除群组用户权限: {user.user_level} -> 0",
                arparma.header_result,
                session=session,
            )
            await MessageUtils.build_message(
                f"成功删除 \n群组：{group_id}\n用户：{uid} \n"
                f"的权限等级!\n权限：{user.user_level} -> 0"
            ).finish()
        await MessageUtils.build_message("对方目前暂无权限喔...").finish()
    await MessageUtils.build_message("设置权限时群组不能为空...").finish()
