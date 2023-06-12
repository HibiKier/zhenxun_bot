from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupIncreaseNoticeEvent,
    GroupMessageEvent,
)

from services.log import logger

from ._data_source import update_member_info

__zx_plugin_name__ = "更新群组成员列表 [Admin]"
__plugin_usage__ = """
usage：
    更新群组成员的基本信息
    指令：
        更新群组成员列表/更新群组成员信息
""".strip()
__plugin_des__ = "更新群组成员列表"
__plugin_cmd__ = ["更新群组成员列表"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": 1,
}


refresh_member_group = on_command(
    "更新群组成员列表", aliases={"更新群组成员信息"}, permission=GROUP, priority=5, block=True
)


@refresh_member_group.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if await update_member_info(bot, event.group_id):
        await refresh_member_group.send("更新群员信息成功！", at_sender=True)
        logger.info("更新群员信息成功！", "更新群组成员列表", event.user_id, event.group_id)
    else:
        await refresh_member_group.send("更新群员信息失败！", at_sender=True)
        logger.info("更新群员信息失败！", "更新群组成员列表", event.user_id, event.group_id)


group_increase_handle = on_notice(priority=1, block=False)


@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    if str(event.user_id) == bot.self_id:
        await update_member_info(bot, event.group_id)
        logger.info("{NICKNAME}加入群聊更新群组信息", "更新群组成员列表", event.user_id, event.group_id)
