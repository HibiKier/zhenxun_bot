from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import update_member_info

__plugin_name__ = "更新群组成员列表"

__plugin_usage__ = """
    说明：
        更新群组成员的基本信息
    示例：
        更新群组成员列表
"""

from nonebot.adapters.cqhttp.permission import GROUP

refresh_member_group = on_command(
    "更新群组成员列表", aliases={"更新群组成员信息"}, permission=GROUP, priority=5, block=True
)


@refresh_member_group.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if await update_member_info(event.group_id):
        await refresh_member_group.finish("更新群员信息成功！", at_sender=True)
    else:
        await refresh_member_group.finish("更新群员信息失败！", at_sender=True)
