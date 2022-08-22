from .data_source import get_sign_reward_list, genshin_sign
from ..mihoyobbs_sign import mihoyobbs_sign
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from nonebot import on_command
from services.log import logger
from .init_task import add_job, scheduler, _sign
from apscheduler.jobstores.base import JobLookupError
from .._models import Genshin
from nonebot.params import Command
from typing import Tuple


__zx_plugin_name__ = "原神自动签到"
__plugin_usage__ = """
usage：
    米游社原神签到，需要uid以及cookie
    且在第二天自动排序签到时间
    # 不听，就要手动签到！（使用命令 “原神我硬签
    指令：
        开/关原神自动签到
        原神我硬签
""".strip()
__plugin_des__ = "原神懒人签到"
__plugin_cmd__ = ["开启/关闭原神自动签到", "原神我硬签", "查看我的cookie"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.2
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["原神签到"],
}


genshin_matcher = on_command(
    "开原神自动签到", aliases={"关原神自动签到", "原神我硬签", "查看我的cookie"}, priority=5, block=True
)


@genshin_matcher.handle()
async def _(event: MessageEvent, cmd: Tuple[str, ...] = Command()):
    cmd = cmd[0]
    uid = await Genshin.get_user_uid(event.user_id)
    if cmd == "查看我的cookie":
        my_cookie = await Genshin.get_user_cookie(uid, True)
        if isinstance(event, GroupMessageEvent):
            await genshin_matcher.finish("请私聊查看您的cookie！")
        await genshin_matcher.finish("您的cookie为" + my_cookie)
    if not uid or not await Genshin.get_user_cookie(uid, True):
        await genshin_matcher.finish("请先绑定uid和cookie！")
    # if "account_id" not in await Genshin.get_user_cookie(uid, True):
    #     await genshin_matcher.finish("请更新cookie！")
    if cmd == "原神我硬签":
        try:
            await genshin_matcher.send("正在进行签到...", at_sender=True)
            msg = await genshin_sign(uid)
            return_data = await mihoyobbs_sign(event.user_id)
            logger.info(
                f"(USER {event.user_id}, "
                f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) UID：{uid} 原神签到"
            )
            logger.info(msg)
            # 硬签，移除定时任务
            try:
                for i in range(3):
                    scheduler.remove_job(f"genshin_auto_sign_{uid}_{event.user_id}_{i}",)
            except JobLookupError:
                pass
            u = await Genshin.get_user_by_uid(uid)
            if u and u.auto_sign:
                await u.clear_sign_time(uid)
                next_date = await Genshin.random_sign_time(uid)
                add_job(event.user_id, uid, next_date)
                msg += f"\n{return_data}\n因开启自动签到\n下一次签到时间为：{next_date.replace(microsecond=0)}"
        except Exception as e:
            msg = "原神签到失败..请尝试检查cookie或报告至管理员！"
            logger.info(
                f"(USER {event.user_id}, "
                f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) UID：{uid} 原神签到发生错误 "
                f"{type(e)}：{e}"
            )
        msg = msg or "请检查cookie是否更新！"
        await genshin_matcher.send(msg, at_sender=True)
    else:
        for i in range(3):
            try:
                scheduler.remove_job(f"genshin_auto_sign_{uid}_{event.user_id}_{i}")
            except JobLookupError:
                pass
        if cmd[0] == "开":
            await Genshin.set_auto_sign(uid, True)
            next_date = await Genshin.random_sign_time(uid)
            add_job(event.user_id, uid, next_date)
            await genshin_matcher.send(
                f"已开启原神自动签到！\n下一次签到时间为：{next_date.replace(microsecond=0)}",
                at_sender=True,
            )
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 开启原神自动签到"
            )
        else:
            await Genshin.set_auto_sign(uid, False)
            await Genshin.clear_sign_time(uid)
            await genshin_matcher.send(f"已关闭原神自动签到！", at_sender=True)
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 关闭原神自动签到"
            )
