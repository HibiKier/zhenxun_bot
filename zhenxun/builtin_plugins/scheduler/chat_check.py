from datetime import datetime, timedelta

import nonebot
import pytz
from nonebot_plugin_apscheduler import scheduler

from zhenxun.models.chat_history import ChatHistory
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger
from zhenxun.utils.platform import PlatformUtils


@scheduler.scheduled_job(
    "cron",
    hour=4,
    minute=40,
)
async def _():
    """检测群组发言时间并禁用全部被动"""
    update_list = []
    if modules := await TaskInfo.annotate().values_list(
            "module", flat=True
    ):
        for bot in nonebot.get_bots().values():
            group_list, _ = await PlatformUtils.get_group_list(bot)
            group_list = [g for g in group_list if g.channel_id == None]

            for group in group_list:
                try:
                    last_message = (
                        await ChatHistory.filter(group_id=group.group_id)
                        .annotate()
                        .order_by("-create_time")
                        .first()
                    )
                    if last_message:
                        now = datetime.now(pytz.timezone("Asia/Shanghai"))
                        if now - timedelta(days=2) > last_message.create_time:
                            _group, _ = await GroupConsole.get_or_create(
                                group_id=group.group_id, channel_id__isnull=True
                            )
                            _group.block_task = ",".join(modules) + ","  # type: ignore
                            update_list.append(_group)
                            logger.info(
                                "群组两日内未发送任何消息，关闭该群全部被动",
                                "Chat检测",
                                target=_group.group_id,
                            )
                except Exception as e:
                    logger.error(
                        "检测群组发言时间失败...", "Chat检测", target=group.group_id
                    )
    if update_list:
        await GroupConsole.bulk_update(update_list, ["block_task"], 10)
