import shutil
from pathlib import Path
from typing import List

import nonebot
from nonebot import get_bots, on_message

from configs.config import NICKNAME, Config
from configs.path_config import IMAGE_PATH
from models.friend_user import FriendUser
from models.group_info import GroupInfo
from services.log import logger
from utils.message_builder import image
from utils.utils import broadcast_group, scheduler

__zx_plugin_name__ = "定时任务相关 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"zwa": "早晚安"}


Config.add_plugin_config(
    "_task", "DEFAULT_ZWA", True, help_="被动 早晚安 进群默认开关状态", default_value=True, type=bool
)

Config.add_plugin_config(
    "_backup", "BACKUP_FLAG", True, help_="是否开启文件备份", default_value=True, type=bool
)

Config.add_plugin_config(
    "_backup",
    "BACKUP_DIR_OR_FILE",
    [
        "data/black_word",
        "data/configs",
        "data/statistics",
        "data/word_bank",
        "data/manager",
        "configs",
    ],
    name="文件备份",
    help_="备份的文件夹或文件",
    default_value=[],
    type=List[str],
)


cx = on_message(priority=9999, block=False, rule=lambda: False)


# 早上好
@scheduler.scheduled_job(
    "cron",
    hour=20,
    minute=44,
)
async def _():
    img = image(IMAGE_PATH / "zhenxun" / "zao.jpg")
    await broadcast_group("[[_task|zwa]]早上好" + img, log_cmd="被动早晚安")
    logger.info("每日早安发送...")


# 睡觉了
@scheduler.scheduled_job(
    "cron",
    hour=23,
    minute=59,
)
async def _():
    img = image(IMAGE_PATH / "zhenxun" / "sleep.jpg")
    await broadcast_group(
        f"[[_task|zwa]]{NICKNAME}要睡觉了，你们也要早点睡呀" + img, log_cmd="被动早晚安"
    )
    logger.info("每日晚安发送...")


# 自动更新群组信息
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    bots = nonebot.get_bots()
    _used_group = []
    for bot in bots.values():
        try:
            group_list = await bot.get_group_list()
            gl = [g["group_id"] for g in group_list if g["group_id"] not in _used_group]
            for g in gl:
                _used_group.append(g)
                group_info = await bot.get_group_info(group_id=g)
                await GroupInfo.update_or_create(
                    group_id=str(group_info["group_id"]),
                    defaults={
                        "group_name": group_info["group_name"],
                        "max_member_count": group_info["max_member_count"],
                        "member_count": group_info["member_count"],
                        "group_flag": 1,
                    },
                )
                logger.debug("自动更新群组信息成功", "自动更新群组", group_id=g)
        except Exception as e:
            logger.error(f"Bot: {bot.self_id} 自动更新群组信息", e=e)
    logger.info("自动更新群组成员信息成功...")


# 自动更新好友信息
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    bots = nonebot.get_bots()
    for key in bots:
        try:
            bot = bots[key]
            fl = await bot.get_friend_list()
            for f in fl:
                if FriendUser.exists(user_id=str(f["user_id"])):
                    await FriendUser.create(
                        user_id=str(f["user_id"]), user_name=f["nickname"]
                    )
                    logger.debug(f"更新好友信息成功", "自动更新好友", f["user_id"])
                else:
                    logger.debug(f"好友信息已存在", "自动更新好友", f["user_id"])
        except Exception as e:
            logger.error(f"自动更新好友信息错误", "自动更新好友", e=e)
    logger.info("自动更新好友信息成功...")


# 自动备份
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=25,
)
async def _():
    if Config.get_config("_backup", "BACKUP_FLAG"):
        _backup_path = Path() / "backup"
        _backup_path.mkdir(exist_ok=True, parents=True)
        if backup_dir_or_file := Config.get_config("_backup", "BACKUP_DIR_OR_FILE"):
            for path_file in backup_dir_or_file:
                try:
                    path = Path(path_file)
                    _p = _backup_path / path_file
                    if path.exists():
                        if path.is_dir():
                            if _p.exists():
                                shutil.rmtree(_p, ignore_errors=True)
                            shutil.copytree(path_file, _p)
                        else:
                            if _p.exists():
                                _p.unlink()
                            shutil.copy(path_file, _p)
                        logger.debug(f"已完成自动备份：{path_file}", "自动备份")
                except Exception as e:
                    logger.error(f"自动备份文件 {path_file} 发生错误", "自动备份", e=e)
    logger.info("自动备份成功...", "自动备份")

    #  一次性任务


# 固定时间触发，仅触发一次：
#
# from datetime import datetime
#
# @nonebot.scheduler.scheduled_job(
#     'date',
#     run_date=datetime(2021, 1, 1, 0, 0),
#     # timezone=None,
# )
# async def _():
#     await bot.send_group_msg(group_id=123456,
#                              message="2021，新年快乐！")

#  定期任务
#  从 start_date 开始到 end_date 结束，根据类似 Cron
#
# 的规则触发任务：
#
# @nonebot.scheduler.scheduled_job(
#     'cron',
#     # year=None,
#     # month=None,
#     # day=None,
#     # week=None,
#     day_of_week="mon,tue,wed,thu,fri",
#     hour=7,
#     # minute=None,
#     # second=None,
#     # start_date=None,
#     # end_date=None,
#     # timezone=None,
# )
# async def _():
#     await bot.send_group_msg(group_id=123456,
#                              message="起床啦！")

#  间隔任务
#
# interval 触发器
#
# 从 start_date 开始，每间隔一段时间触发，到 end_date 结束：
#
# @nonebot.scheduler.scheduled_job(
#     'interval',
#     # weeks=0,
#     # days=0,
#     # hours=0,
#     minutes=5,
#     # seconds=0,
#     # start_date=time.now(),
#     # end_date=None,
# )
# async def _():
#     has_new_item = check_new_item()
#     if has_new_item:
#         await bot.send_group_msg(group_id=123456,
#                                  message="XX有更新啦！")


# 动态的计划任务
# import datetime
#
# from apscheduler.triggers.date import DateTrigger # 一次性触发器
# # from apscheduler.triggers.cron import CronTrigger # 定期触发器
# # from apscheduler.triggers.interval import IntervalTrigger # 间隔触发器
# from nonebot import on_command, scheduler
#
# @on_command('赖床')
# async def _(session: CommandSession):
#     await session.send('我会在5分钟后再喊你')
#
#     # 制作一个“5分钟后”触发器
#     delta = datetime.timedelta(minutes=5)
#     trigger = DateTrigger(
#         run_date=datetime.datetime.now() + delta
#     )
#
#     # 添加任务
#     scheduler.add_job(
#         func=session.send,  # 要添加任务的函数，不要带参数
#         trigger=trigger,  # 触发器
#         args=('不要再赖床啦！',),  # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
#         # kwargs=None,
#         misfire_grace_time=60,  # 允许的误差时间，建议不要省略
#         # jobstore='default',  # 任务储存库，在下一小节中说明
#     )
