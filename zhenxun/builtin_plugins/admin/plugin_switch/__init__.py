from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
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
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession
from requests import session

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import BlockType, PluginType
from zhenxun.utils.rules import admin_check, ensure_group

from ._data_source import PluginManage, build_plugin, build_task
from .command import _group_status_matcher, _status_matcher

base_config = Config.get("admin_bot_manage")


__plugin_meta__ = PluginMetadata(
    name="功能开关",
    description="对群组内的功能限制，超级用户可以对群组以及全局的功能被动开关限制",
    usage="""
    开启/关闭[功能]
    群被动状态
    开启全部被动
    关闭全部被动
    醒来/休息吧
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPER_AND_ADMIN,
        admin_level=base_config.get("CHANGE_GROUP_SWITCH_LEVEL", 2),
        configs=[
            RegisterConfig(
                key="CHANGE_GROUP_SWITCH_LEVEL",
                value=2,
                help="开关群功能权限",
                default_value=2,
                type=int,
            )
        ],
    ).dict(),
)


# _status_matcher = on_alconna(
#     Alconna(
#         "switch",
#         Option("-t|--task", action=store_true, help_text="被动技能"),
#         Subcommand(
#             "open",
#             Args["name", str],
#             Option(
#                 "-g|--group",
#                 Args["group_id", str],
#             ),
#         ),
#         Subcommand(
#             "close",
#             Args["name", str],
#             Option(
#                 "-t|--type",
#                 Args["block_type", ["all", "a", "private", "p", "group", "g"]],
#             ),
#             Option(
#                 "-g|--group",
#                 Args["group_id", str],
#             ),
#         ),
#     ),
#     rule=admin_check("admin_bot_manage", "CHANGE_GROUP_SWITCH_LEVEL"),
#     priority=5,
#     block=True,
# )

# # TODO: shortcut

# _group_status_matcher = on_alconna(
#     Alconna("group-status", Args["status", ["sleep", "wake"]]),
#     rule=admin_check("admin_bot_manage", "CHANGE_GROUP_SWITCH_LEVEL") & ensure_group,
#     priority=5,
#     block=True,
# )


@_status_matcher.assign("$main")
async def _(bot: Bot, session: EventSession, arparma: Arparma):
    image = None
    if session.id1 in bot.config.superusers:
        image = await build_plugin()
    if image:
        await Image(image.pic2bs4()).send(reply=True)
        logger.info(
            f"查看功能列表",
            arparma.header_result,
            session=session,
        )


@_status_matcher.assign("task")
async def _(bot: Bot, session: EventSession, arparma: Arparma):
    image = None
    if image := await build_task(session.id3 or session.id2):
        await Image(image.pic2bs4()).send(reply=True)
        logger.info(
            f"查看被动列表",
            arparma.header_result,
            session=session,
        )


@_status_matcher.assign("open")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    name: str,
    group: Match[str],
):
    if gid := session.id3 or session.id2:
        result = await PluginManage.block_group_plugin(name, gid)
        await Text(result).send(reply=True)
        logger.info(f"开启功能 {name}", arparma.header_result, session=session)
    elif session.id1 in bot.config.superusers:
        group_id = group.result if group.available else None
        result = await PluginManage.superuser_block(name, None, group_id)
        await Text(result).send(reply=True)
        logger.info(
            f"超级用户开启功能 {name}",
            arparma.header_result,
            session=session,
            target=group_id,
        )


@_status_matcher.assign("close")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    name: str,
    block_type: Match[str],
    group: Match[str],
):
    if gid := session.id3 or session.id2:
        result = await PluginManage.unblock_group_plugin(name, gid)
        await Text(result).send(reply=True)
        logger.info(f"关闭功能 {name}", arparma.header_result, session=session)
    elif session.id1 in bot.config.superusers:
        group_id = group.result if group.available else None
        _type = BlockType.ALL
        if block_type.available:
            if block_type.result in ["p", "private"]:
                _type = BlockType.PRIVATE
            elif block_type.result in ["g", "group"]:
                _type = BlockType.GROUP
        result = await PluginManage.superuser_block(name, _type, group_id)
        await Text(result).send(reply=True)
        logger.info(
            f"超级用户关闭功能 {name}, 禁用类型: {_type}",
            arparma.header_result,
            session=session,
            target=group_id,
        )


@_group_status_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    status: str,
):
    if gid := session.id3 or session.id2:
        if status == "sleep":
            await PluginManage.sleep(gid)
            logger.info("进行休眠", arparma.header_result, session=session)
            await Text("那我先睡觉了...").finish()
        else:
            if PluginManage.is_wake(gid):
                await Text("我还醒着呢！").finish()
            await PluginManage.wake(gid)
            logger.info("醒来", arparma.header_result, session=session)
            await Text("呜..醒来了...").finish()
    return Text("群组id为空...").send()
