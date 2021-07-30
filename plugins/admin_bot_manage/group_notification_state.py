from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import set_group_status, group_current_status
from nonebot.adapters.cqhttp.permission import GROUP
from services.log import logger
from nonebot import on_command


__plugin_name__ = "群通知开关"

__plugin_usage__ = """
    示例：
        开启早晚安
        关闭早晚安
"""


group_status = on_command(
    "oc_reminds",
    aliases={
        "开启早晚安",
        "关闭早晚安",
        "开启进群欢迎",
        "关闭进群欢迎",
        "开启每日开箱重置提醒",
        "关闭每日开箱重置提醒",
        "开启b站转发解析",
        "关闭b站转发解析",
        "开启epic通知",
        "关闭epic通知",
        "开启丢人爬",
        "关闭丢人爬",
        "开启原神黄历提醒",
        "关闭原神黄历提醒",
        "开启全部通知",
        "开启所有通知",
        "关闭全部通知",
        "关闭所有通知",
        "群通知状态",
    },
    permission=GROUP,
    priority=1,
    block=True,
)


@group_status.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if state["_prefix"]["raw_command"] in ["群通知状态"]:
        await group_status.finish(await group_current_status(event.group_id))
    await group_status.send(
        await set_group_status(state["_prefix"]["raw_command"], event.group_id),
        at_sender=True,
    )
    logger.info(
        f'USER {event.user_id} GROUP {event.group_id} 使用群通知管理命令 {state["_prefix"]["raw_command"]}'
    )
