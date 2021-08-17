from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from .data_source import change_group_switch, set_plugin_status, get_plugin_status
from services.log import logger
from configs.config import plugins2info_dict, NICKNAME
from utils.utils import get_message_text, is_number
from nonebot.permission import SUPERUSER


__plugin_name__ = "群功能开关"

__plugin_usage__ = """
    示例：
        开启色图
        关闭色图
"""


cmds = []
for cmd_list in plugins2info_dict.values():
    for cmd in cmd_list["cmd"]:
        cmds.append(f"开启{cmd}")
        cmds.append(f"关闭{cmd}")
cmds = set(cmds)


switch_rule = on_command(
    "switch_rule", aliases=cmds, priority=5, block=True
)

plugins_status = on_command('功能状态', permission=SUPERUSER, priority=5, block=True)


@switch_rule.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if isinstance(event, GroupMessageEvent):
        await switch_rule.send(
            change_group_switch(
                state["_prefix"]["raw_command"].strip(), event.group_id
            )
        )
        logger.info(
            f'USER {event.user_id} GROUP {event.group_id} 使用群功能管理命令 {state["_prefix"]["raw_command"]}'
        )
    else:
        if str(event.user_id) in bot.config.superusers:
            block_type = get_message_text(event.json())
            _cmd = state["_prefix"]["raw_command"].strip()
            if is_number(block_type):
                if not int(block_type) in [g["group_id"] for g in await bot.get_group_list(self_id=int(bot.self_id))]:
                    await switch_rule.finish(f'{NICKNAME}未加入群聊：{block_type}')
                change_group_switch(_cmd, int(block_type), True)
                group_name = (await bot.get_group_info(group_id=int(block_type)))['group_name']
                await switch_rule.send(f'已禁用群聊 {group_name}({block_type}) 的 {_cmd[2:]} 功能')
            else:
                if block_type not in ['all', 'private', 'group', 'a', 'p', 'g']:
                    block_type = 'all'
                block_type = 'all' if block_type == 'a' else block_type
                block_type = 'private' if block_type == 'p' else block_type
                block_type = 'group' if block_type == 'g' else block_type
                set_plugin_status(_cmd, block_type)
                if block_type == 'all':
                    await switch_rule.send(f'已{_cmd[:2]}功能：{_cmd[2:]}')
                elif block_type == 'private':
                    await switch_rule.send(f'已在私聊中{_cmd[:2]}功能：{_cmd[2:]}')
                else:
                    await switch_rule.send(f'已在群聊中{_cmd[:2]}功能：{_cmd[2:]}')
            logger.info(
                f'USER {event.user_id} 使用功能管理命令 {state["_prefix"]["raw_command"]} | {block_type}'
            )


@plugins_status.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await plugins_status.send(await get_plugin_status())

