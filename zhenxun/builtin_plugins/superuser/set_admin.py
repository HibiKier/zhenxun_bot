from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    At,
    Match,
    Subcommand,
    on_alconna,
)
from nonebot_plugin_saa import Mention, MessageFactory, Text
from nonebot_plugin_session import EventSession, SessionLevel

from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.level_user import LevelUser
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

__plugin_meta__ = PluginMetadata(
    name="用户权限管理",
    description="设置用户权限",
    usage="""
    权限设置 add [level: 权限等级] [at: at对象或用户id] [gid: 群组]
    权限设置 delete [at: at对象或用户id]
    
    权限设置 add 5 @user
    权限设置 add 5 422 352352

    权限设置 delete @user
    权限设置 delete 123456
    
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "权限设置",
        Subcommand(
            "add", Args["level", int]["uid", [str, At]]["gid?", str], help_text="添加权限"
        ),
        Subcommand("delete", Args["uid", [str, At]]["gid?", str], help_text="删除权限"),
    ),
    permission=SUPERUSER,
    priority=5,
    block=True,
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
            await MessageFactory(
                [Text("成功为 "), Mention(uid), Text(f" 设置权限：{old_level} -> {level}")]
            ).finish(reply=True)
        await Text(
            f"成功为 \n群组：{group_id}\n用户：{uid} \n设置权限!\n权限：{old_level} -> {level}"
        ).finish()
    await Text(f"设置权限时群组不能为空...").finish()


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
                await MessageFactory(
                    [Text("成功删除 "), Mention(uid), Text(f" 的权限等级!")]
                ).finish(reply=True)
            await Text(
                f"成功删除 \n群组：{group_id}\n用户：{uid} \n的权限等级!\n权限：{user.user_level} -> 0"
            ).finish()
        await Text(f"对方目前暂无权限喔...").finish()
    await Text(f"设置权限时群组不能为空...").finish()
