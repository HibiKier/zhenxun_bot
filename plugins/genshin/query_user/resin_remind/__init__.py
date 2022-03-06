from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from apscheduler.jobstores.base import JobLookupError
from services.log import logger
from .init_task import scheduler, add_job
from .._models import Genshin
from nonebot.params import Command
from typing import Tuple


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
        "default_value": True
    },
    "CUSTOM_RESIN_OVERFLOW_REMIND": {
        "value": 20,
        "help": "自定义树脂溢出指定数量时的提醒，空值是为关闭",
        "default_value": None
    }
}

resin_remind = on_command("开原神树脂提醒", aliases={"关原神树脂提醒"}, priority=5, block=True)


@resin_remind.handle()
async def _(event: MessageEvent, cmd: Tuple[str, ...] = Command()):
    cmd = cmd[0]
    uid = await Genshin.get_user_uid(event.user_id)
    if not uid or not await Genshin.get_user_cookie(uid, True):
        await resin_remind.finish("请先绑定uid和cookie！")
    try:
        scheduler.remove_job(f"genshin_resin_remind_{uid}_{event.user_id}")
    except JobLookupError:
        pass
    if cmd[0] == "开":
        await Genshin.set_resin_remind(uid, True)
        add_job(event.user_id, uid)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 开启原神体力提醒"
        )
        await resin_remind.send("开启原神树脂提醒成功！", at_sender=True)
    else:
        await Genshin.set_resin_remind(uid, False)
        await Genshin.clear_resin_remind_time(uid)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 关闭原神体力提醒"
        )
        await resin_remind.send("已关闭原神树脂提醒..", at_sender=True)

