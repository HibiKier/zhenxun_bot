from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import AlconnaQuery, Arparma, Match, Query
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import BlockType, PluginType

from ._data_source import PluginManage, build_plugin, build_task
from .command import _group_status_matcher, _status_matcher

base_config = Config.get("admin_bot_manage")


__plugin_meta__ = PluginMetadata(
    name="功能开关",
    description="对群组内的功能限制，超级用户可以对群组以及全局的功能被动开关限制",
    usage="""
    普通管理员
        格式:
        开启/关闭[功能名称]         : 开关功能
        开启/关闭群被动[被动名称]    : 群被动开关
        群被动状态                 : 查看被动技能开关状态
        醒来                      : 结束休眠
        休息吧                    : 群组休眠, 不会再响应命令

        示例:
        开启签到              : 开启签到
        关闭签到              : 关闭签到
        开启群被动早晚安       : 关闭被动任务早晚安

    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPER_AND_ADMIN,
        superuser_help="""
        超级管理员额外命令
            格式:
            插件列表
            开启/关闭[功能名称] ?[-t ["private", "p", "group", "g"](关闭类型)] ?[-g 群组Id]

            私聊下:
                示例:
                开启签到                : 全局开启签到
                关闭签到                : 全局关闭签到
                关闭签到 p              : 全局私聊关闭签到
                关闭签到 -g 12345678    : 关闭群组12345678的签到功能(普通管理员无法开启)
        """,
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


@_status_matcher.assign("$main")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    task: Query[bool] = AlconnaQuery("task.value", False),
):
    image = None
    if task.result:
        image = await build_task(session.id3 or session.id2)
    elif session.id1 in bot.config.superusers:
        image = await build_plugin()
    if image:
        await Image(image.pic2bytes()).send(reply=True)
        logger.info(
            f"查看{'功能' if arparma.find('task') else '被动'}列表",
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
    task: Query[bool] = AlconnaQuery("task.value", False),
):
    if gid := session.id3 or session.id2:
        if task.result:
            result = await PluginManage.unblock_group_task(name, gid)
        else:
            result = await PluginManage.block_group_plugin(name, gid)
        await Text(result).send(reply=True)
        logger.info(f"开启功能 {name}", arparma.header_result, session=session)
    elif session.id1 in bot.config.superusers:
        group_id = group.result if group.available else None
        if task.result:
            result = await PluginManage.superuser_task_handle(name, group_id, True)
            await Text(result).send(reply=True)
            logger.info(
                f"超级用户开启被动技能 {name}",
                arparma.header_result,
                session=session,
                target=group_id,
            )
        else:
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
    task: Query[bool] = AlconnaQuery("task.value", False),
):
    if gid := session.id3 or session.id2:
        if task.result:
            result = await PluginManage.block_group_task(name, gid)
        else:
            result = await PluginManage.unblock_group_plugin(name, gid)
        await Text(result).send(reply=True)
        logger.info(f"关闭功能 {name}", arparma.header_result, session=session)
    elif session.id1 in bot.config.superusers:
        group_id = group.result if group.available else None
        if task.result:
            result = await PluginManage.superuser_task_handle(name, group_id, False)
            await Text(result).send(reply=True)
            logger.info(
                f"超级用户关闭被动技能 {name}",
                arparma.header_result,
                session=session,
                target=group_id,
            )
        else:
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
