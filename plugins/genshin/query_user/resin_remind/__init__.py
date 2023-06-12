from typing import Tuple

from apscheduler.jobstores.base import JobLookupError
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.params import Command

from services.log import logger
from utils.depends import OneCommand

from .._models import Genshin
from .init_task import add_job, scheduler

__zx_plugin_name__ = "原神树脂提醒"
__plugin_usage__ = """
usage：
    即将满树脂的提醒
    会在 120-140 140-160 160 以及溢出指定部分时提醒，
    共提醒3-4次
    指令：
        开原神树脂提醒
        关原神树脂提醒
""".strip()
__plugin_des__ = "时时刻刻警醒你！"
__plugin_cmd__ = ["开原神树脂提醒", "关原神树脂提醒"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神树脂提醒", "关原神树脂提醒", "开原神树脂提醒"],
}
__plugin_configs__ = {
    "AUTO_CLOSE_QUERY_FAIL_RESIN_REMIND": {
        "value": True,
        "help": "当请求连续三次失败时，关闭用户的树脂提醒",
        "default_value": True,
        "type": bool,
    },
    "CUSTOM_RESIN_OVERFLOW_REMIND": {
        "value": 20,
        "help": "自定义树脂溢出指定数量时的提醒，空值是为关闭",
        "default_value": None,
        "type": int,
    },
}

resin_remind = on_command("开原神树脂提醒", aliases={"关原神树脂提醒"}, priority=5, block=True)


@resin_remind.handle()
async def _(event: MessageEvent, cmd: str = OneCommand()):
    user = await Genshin.get_or_none(user_id=str(event.user_id))
    if not user or not user.uid or not user.cookie:
        await resin_remind.finish("请先绑定uid和cookie！")
    try:
        scheduler.remove_job(f"genshin_resin_remind_{user.uid}_{event.user_id}")
    except JobLookupError:
        pass
    if cmd[0] == "开":
        if user.resin_remind:
            await resin_remind.finish("原神树脂提醒已经是开启状态，请勿重复开启！", at_sender=True)
        user.resin_remind = True
        add_job(event.user_id, user.uid)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 开启原神体力提醒"
        )
        await resin_remind.send("开启原神树脂提醒成功！", at_sender=True)
    else:
        if not user.resin_remind:
            await resin_remind.finish("原神树脂提醒已经是开启状态，请勿重复开启！", at_sender=True)
        user.resin_remind = False
        user.resin_recovery_time = None
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 关闭原神体力提醒"
        )
        await resin_remind.send("已关闭原神树脂提醒..", at_sender=True)
    if user:
        await user.save(update_fields=["resin_remind", "resin_recovery_time"])
