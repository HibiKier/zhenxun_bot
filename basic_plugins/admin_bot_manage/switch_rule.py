from typing import Any, Tuple

from nonebot import on_command, on_message, on_regex
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import CommandArg, RegexGroup
from nonebot.permission import SUPERUSER

from configs.config import NICKNAME, Config
from services.log import logger
from utils.message_builder import image
from utils.utils import get_message_text, is_number

from ._data_source import (
    change_global_task_status,
    change_group_switch,
    get_plugin_status,
    group_current_status,
    set_group_bot_status,
    set_plugin_status,
)
from .rule import switch_rule

__zx_plugin_name__ = "群功能开关 [Admin]"

__plugin_usage__ = """
usage：
    群内功能与被动技能开关
    指令：
        开启/关闭[功能]
        群被动状态
        开启全部被动
        关闭全部被动
        醒来/休息吧
        示例：开启/关闭色图
""".strip()
__plugin_superuser_usage__ = """
usage:
    （私聊）功能总开关与指定群禁用
    指令：
        功能状态
        开启/关闭[功能] [group]
        开启/关闭[功能] ['private'/'group']
        开启被动/关闭被动[被动名称]     # 全局被动控制
""".strip()
__plugin_des__ = "群内功能开关"
__plugin_cmd__ = [
    "开启/关闭[功能]",
    "群被动状态",
    "开启全部被动",
    "关闭全部被动",
    "醒来/休息吧",
    "功能状态 [_superuser]",
    "开启/关闭[功能] [group] [_superuser]",
    "开启/关闭[功能] ['private'/'group'] [_superuser]",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": Config.get_config("admin_bot_manage", "CHANGE_GROUP_SWITCH_LEVEL"),
    "cmd": ["开启功能", "关闭功能", "开关"],
}

switch_rule_matcher = on_message(rule=switch_rule, priority=4, block=True)

plugins_status = on_command("功能状态", permission=SUPERUSER, priority=5, block=True)

group_task_status = on_command("群被动状态", permission=GROUP, priority=5, block=True)

group_status = on_regex("^(休息吧|醒来)$", permission=GROUP, priority=5, block=True)


@switch_rule_matcher.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
):
    msg = get_message_text(event.message).strip()
    msg_split = msg.split()
    _cmd = msg_split[0]
    if isinstance(event, GroupMessageEvent):
        await switch_rule_matcher.send(await change_group_switch(_cmd, event.group_id))
        logger.info(f"使用群功能管理命令 {_cmd}", "功能管理", event.user_id, event.group_id)
    else:
        if str(event.user_id) in bot.config.superusers:
            block_type = " ".join(msg_split[1:])
            block_type = block_type if block_type else "a"
            if ("关闭被动" in _cmd or "开启被动" in _cmd) and isinstance(
                event, PrivateMessageEvent
            ):
                await switch_rule_matcher.send(change_global_task_status(_cmd))
            elif is_number(block_type):
                if not int(block_type) in [
                    g["group_id"] for g in await bot.get_group_list()
                ]:
                    await switch_rule_matcher.finish(f"{NICKNAME}未加入群聊：{block_type}")
                await change_group_switch(_cmd, int(block_type), True)
                group_name = (await bot.get_group_info(group_id=int(block_type)))[
                    "group_name"
                ]
                await switch_rule_matcher.send(
                    f"已{_cmd[:2]}群聊 {group_name}({block_type}) 的 {_cmd[2:]} 功能"
                )
            elif block_type in ["all", "private", "group", "a", "p", "g"]:
                block_type = "all" if block_type == "a" else block_type
                block_type = "private" if block_type == "p" else block_type
                block_type = "group" if block_type == "g" else block_type
                set_plugin_status(_cmd, block_type)  # type: ignore
                if block_type == "all":
                    await switch_rule_matcher.send(f"已{_cmd[:2]}功能：{_cmd[2:]}")
                elif block_type == "private":
                    await switch_rule_matcher.send(f"已在私聊中{_cmd[:2]}功能：{_cmd[2:]}")
                else:
                    await switch_rule_matcher.send(f"已在群聊中{_cmd[:2]}功能：{_cmd[2:]}")
            else:
                await switch_rule_matcher.finish("格式错误：关闭[功能] [group]/[p/g]")
            logger.info(f"使用功能管理命令 {_cmd} | {block_type}", f"{_cmd}", event.user_id)


@plugins_status.handle()
async def _():
    await plugins_status.send(await get_plugin_status())


@group_task_status.handle()
async def _(event: GroupMessageEvent):
    await group_task_status.send(image(b64=await group_current_status(str(event.group_id))))


@group_status.handle()
async def _(event: GroupMessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    cmd = reg_group[0]
    if cmd == "休息吧":
        msg = set_group_bot_status(str(event.group_id), False)
    else:
        msg = set_group_bot_status(str(event.group_id), True)
    await group_status.send(msg)
    logger.info(f"使用总开关命令: {cmd}", cmd, event.user_id, event.group_id)
