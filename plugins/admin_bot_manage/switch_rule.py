from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import change_group_switch
from nonebot.adapters.cqhttp.permission import GROUP
from services.log import logger
from configs.config import plugins2info_dict


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
    "switch_rule", aliases=cmds, permission=GROUP, priority=4, block=True
)


@switch_rule.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await switch_rule.send(
        await change_group_switch(
            state["_prefix"]["raw_command"].strip(), event.group_id
        )
    )
    logger.info(
        f'USER {event.user_id} GROUP {event.group_id} 使用群功能管理命令 {state["_prefix"]["raw_command"]}'
    )
