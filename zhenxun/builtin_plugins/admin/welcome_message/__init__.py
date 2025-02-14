from typing import Annotated

from nonebot import on_command
from nonebot.params import Command
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatcher,
    Args,
    Arparma,
    Field,
    Match,
    Text,
    UniMsg,
    on_alconna,
)
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.rules import admin_check, ensure_group

from .data_source import Manager

base_config = Config.get("admin_bot_manage")

__plugin_meta__ = PluginMetadata(
    name="自定义群欢迎消息",
    description="自定义群欢迎消息",
    usage="""
    设置群欢迎消息，当消息中包含 -at 时会at入群用户
    可以设置多条欢迎消息，包含多条欢迎消息时将随机发送
    指令:
        设置欢迎消息
        查看欢迎消息 ?[id]: 存在id时查看指定欢迎消息内容
        删除欢迎消息 [id]
    示例:
        设置欢迎消息 欢迎新人！[图片]
        设置欢迎消息 欢迎你 -at
        查看欢迎消息
        查看欢迎消息 2
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=base_config.get("SET_GROUP_WELCOME_MESSAGE_LEVEL", 2),
        configs=[
            RegisterConfig(
                module="admin_bot_manage",
                key="SET_GROUP_WELCOME_MESSAGE_LEVEL",
                value=2,
                help="设置群欢迎消息所需要的管理员权限等级",
                default_value=2,
            )
        ],
    ).to_dict(),
)

_matcher = on_command(
    "设置欢迎消息",
    rule=admin_check("admin_bot_manage", "SET_GROUP_WELCOME_MESSAGE_LEVEL")
    & ensure_group,
    priority=5,
    block=True,
)

_show_matcher = on_alconna(
    Alconna("查看欢迎消息", Args["idx?", int]),
    rule=admin_check("admin_bot_manage", "SET_GROUP_WELCOME_MESSAGE_LEVEL")
    & ensure_group,
    priority=5,
    block=True,
)

_del_matcher: type[AlconnaMatcher] = on_alconna(
    Alconna(
        "删除欢迎消息",
        Args[
            "idx",
            int,
            Field(
                missing_tips=lambda: "请在命令后跟随指定id！",
                unmatch_tips=lambda _: "删除指定id必须为数字！",
            ),
        ],
    ),
    skip_for_unmatch=False,
    rule=admin_check("admin_bot_manage", "SET_GROUP_WELCOME_MESSAGE_LEVEL")
    & ensure_group,
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(
    session: Uninfo,
    message: UniMsg,
    command: Annotated[tuple[str, ...], Command()],
):
    path = Manager.get_path(session)
    if not path:
        await MessageUtils.build_message("群组不存在...").finish()
    message[0].text = message[0].text.replace(command[0], "").strip()
    await Manager.save(path, message)
    uni_msg = Text("设置欢迎消息成功: \n") + message
    await uni_msg.send()
    logger.info(f"设置群欢迎消息成功: {message}", command[0], session=session)


@_show_matcher.handle()
async def _(session: Uninfo, arparma: Arparma, idx: Match[int]):
    result = await Manager.get_group_message(
        session, idx.result if idx.available else None
    )
    if not result:
        await MessageUtils.build_message("当前还未设置群组欢迎消息哦...").finish()
    await MessageUtils.build_message(result).send()
    logger.info("查看群组欢迎信息", arparma.header_result, session=session)


@_del_matcher.handle()
async def _(session: Uninfo, arparma: Arparma, idx: int):
    result = await Manager.delete_group_message(session, int(idx))
    if not result:
        await MessageUtils.build_message("未查找到指定id的群组欢迎消息...").finish()
    await MessageUtils.build_message(result).send()
    logger.info(f"删除群组欢迎信息: {result}", arparma.header_result, session=session)
