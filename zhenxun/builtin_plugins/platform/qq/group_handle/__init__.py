from nonebot.adapters import Bot
from nonebot_plugin_uninfo import Uninfo
from nonebot import on_notice, on_request
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import (
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
)
from nonebot.adapters.onebot.v12 import (
    GroupMemberDecreaseEvent,
    GroupMemberIncreaseEvent,
)

from zhenxun.utils.enum import PluginType
from zhenxun.utils.rules import notice_rule
from zhenxun.utils.platform import PlatformUtils
from zhenxun.utils.common_utils import CommonUtils
from zhenxun.configs.config import Config, BotConfig
from zhenxun.models.group_console import GroupConsole
from zhenxun.configs.utils import Task, RegisterConfig, PluginExtraData

from .data_source import GroupManager
from ..exception import ForceAddGroupError

__plugin_meta__ = PluginMetadata(
    name="QQ群事件处理",
    description="群事件处理",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        configs=[
            RegisterConfig(
                module="invite_manager",
                key="message",
                value=f"请不要未经同意就拉{BotConfig.self_nickname}入群！告辞！",
                help="强制拉群后进群回复的内容",
            ),
            RegisterConfig(
                module="invite_manager",
                key="flag",
                value=True,
                help="强制拉群后进群退出并回复内容",
                default_value=True,
                type=bool,
            ),
            RegisterConfig(
                module="invite_manager",
                key="welcome_msg_cd",
                value=5,
                help="群欢迎消息cd",
                default_value=5,
                type=int,
            ),
            RegisterConfig(
                module="_task",
                key="DEFAULT_GROUP_WELCOME",
                value=True,
                help="被动 进群欢迎 进群默认开关状态",
                default_value=True,
                type=bool,
            ),
            RegisterConfig(
                module="_task",
                key="DEFAULT_REFUND_GROUP_REMIND",
                value=True,
                help="被动 退群提醒 进群默认开关状态",
                default_value=True,
                type=bool,
            ),
        ],
        tasks=[
            Task(module="group_welcome", name="进群欢迎"),
            Task(module="refund_group_remind", name="退群提醒"),
        ],
    ).dict(),
)


base_config = Config.get("invite_manager")


limit_cd = base_config.get("welcome_msg_cd")


group_increase_handle = on_notice(
    priority=1,
    block=False,
    rule=notice_rule([GroupIncreaseNoticeEvent, GroupMemberIncreaseEvent]),
)
"""群员增加处理"""
group_decrease_handle = on_notice(
    priority=1,
    block=False,
    rule=notice_rule([GroupMemberDecreaseEvent, GroupMemberIncreaseEvent]),
)
"""群员减少处理"""
add_group = on_request(priority=1, block=False)
"""加群同意请求"""


@group_increase_handle.handle()
async def _(
    bot: Bot,
    session: Uninfo,
    event: GroupIncreaseNoticeEvent | GroupMemberIncreaseEvent,
):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    if user_id == bot.self_id:
        """新成员为bot本身"""
        group, _ = await GroupConsole.get_or_create(
            group_id=group_id, channel_id__isnull=True
        )
        try:
            await GroupManager.add_bot(bot, str(event.operator_id), group_id, group)
        except ForceAddGroupError as e:
            await PlatformUtils.send_superuser(bot, e.get_info())
    else:
        await GroupManager.add_user(session, bot, user_id, group_id)


@group_decrease_handle.handle()
async def _(
    bot: Bot,
    session: Uninfo,
    event: GroupDecreaseNoticeEvent | GroupMemberDecreaseEvent,
):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    if event.sub_type == "kick_me":
        """踢出Bot"""
        await GroupManager.kick_bot(bot, user_id, group_id)
    elif event.sub_type in ["leave", "kick"]:
        result = await GroupManager.run_user(
            bot, user_id, group_id, str(event.operator_id), event.sub_type
        )
        if result and not await CommonUtils.task_is_block(
            session, "refund_group_remind"
        ):
            await group_decrease_handle.send(result)
