from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    Option,
    Subcommand,
    on_alconna,
    store_true,
)
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

__plugin_meta__ = PluginMetadata(
    name="管理群操作",
    description="管理群操作",
    usage="""
    群权限 | 群白名单 | 退出群 操作
    退群，添加/删除群白名单，添加/删除群认证，当在群组中这五个命令且没有指定群号时，默认指定当前群组
    指令:
        退群 ?[group_id]
        修改群权限 [group_id] [等级]
        修改群权限 [等级]: 该命令仅在群组时生效，默认修改当前群组
        添加群白名单 ?*[group_id]
        删除群白名单 ?*[group_id]
        添加群认证 ?*[group_id]
        删除群认证 ?*[group_id]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "group-manage",
        Subcommand(
            "modify-level", Args["level", int]["group_id?", int], help_text="修改群权限"
        ),
        Subcommand(
            "super-handle",
            Option("--del", action=store_true, help_text="删除"),
            Args["group_id", int],
            help_text="添加/删除群白名单",
        ),
        Subcommand(
            "auth-handle",
            Option("--del", action=store_true, help_text="删除"),
            Args["group_id", int],
            help_text="添加群白名单",
        ),
        Subcommand("del-group", Args["group_id", int], help_text="退出群组"),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

# TODO: shortcut


def CheckGroupId():
    """
    检测群组id
    """

    async def dependency(
        session: EventSession,
        group_id: Match[int],
        state: T_State,
    ):
        gid = session.id3 or session.id2
        if group_id.available:
            gid = group_id.result
        if not gid:
            await Text("群组id不能为空...").finish()
        state["group_id"] = gid

    return Depends(dependency)


@_matcher.assign("modify-level", parameterless=[CheckGroupId()])
async def _(session: EventSession, arparma: Arparma, state: T_State, level: int):
    gid = state["group_id"]
    group, _ = await GroupConsole.get_or_create(group_id=gid)
    old_level = group.level
    group.level = level
    await group.save(update_fields=["level"])
    await Text("群权限修改成功!").send(reply=True)
    logger.info(
        f"修改群权限: {old_level} -> {level}",
        arparma.header_result,
        session=session,
        target=gid,
    )


@_matcher.assign("super-handle", parameterless=[CheckGroupId()])
async def _(session: EventSession, arparma: Arparma, state: T_State):
    gid = state["group_id"]
    group = await GroupConsole.get_or_none(group_id=gid)
    if not group:
        await Text("群组信息不存在, 请更新群组信息...").finish()
    s = "删除" if arparma.find("del") else "添加"
    group.is_super = not arparma.find("del")
    await group.save(update_fields=["is_super"])
    await Text(f"{s}群白名单成功!").send(reply=True)
    logger.info(f"{s}群白名单", arparma.header_result, session=session, target=gid)


@_matcher.assign("auth-handle", parameterless=[CheckGroupId()])
async def _(session: EventSession, arparma: Arparma, state: T_State):
    gid = state["group_id"]
    await GroupConsole.update_or_create(
        group_id=gid, defaults={"group_flag": 0 if arparma.find("del") else 1}
    )
    s = "删除" if arparma.find("del") else "添加"
    await Text(f"{s}群认证成功!").send(reply=True)
    logger.info(f"{s}群白名单", arparma.header_result, session=session, target=gid)


@_matcher.assign("del-group")
async def _(bot: Bot, session: EventSession, arparma: Arparma, group_id: int):
    if isinstance(bot, v11Bot):
        group_list = [g["group_id"] for g in await bot.get_group_list()]
        if group_id not in group_list:
            logger.debug("群组不存在", "退群", session=session, target=group_id)
            await Text(f"{NICKNAME}未在该群组中...").finish()
        try:
            await bot.set_group_leave(group_id=group_id)
            logger.info(
                f"{NICKNAME}退出群组成功", "退群", session=session, target=group_id
            )
            await Text(f"退出群组 {group_id} 成功!").send()
            await GroupConsole.filter(group_id=group_id).delete()
        except Exception as e:
            logger.error(f"退出群组失败", "退群", session=session, target=group_id, e=e)
            await Text(f"退出群组 {group_id} 失败...").send()
    else:
        # TODO: 其他平台的退群操作
        await Text(f"暂未支持退群操作...").send()
