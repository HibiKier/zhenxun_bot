from utils.message_builder import image
from utils.utils import scheduler, get_bot
from nonebot import on_message
from services.log import logger
from models.group_info import GroupInfo
from models.friend_user import FriendUser
from nonebot.adapters.onebot.v11.exception import ActionFailed
from configs.config import NICKNAME, Config
from utils.manager import group_manager
from pathlib import Path
import shutil

__zx_plugin_name__ = "定时任务相关 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {'zwa': '早晚安'}


Config.add_plugin_config(
    "_task",
    "DEFAULT_ZWA",
    True,
    help_="被动 早晚安 进群默认开关状态",
    default_value=True,
)

Config.add_plugin_config(
    "_backup",
    "BACKUP_FLAG",
    True,
    help_="是否开启文件备份",
    default_value=True
)

Config.add_plugin_config(
    "_backup",
    "BACKUP_DIR_OR_FILE",
    ['data/black_word', 'data/configs', 'data/statistics', 'data/word_bank', 'data/manager', 'configs'],
    name="文件备份",
    help_="备份的文件夹或文件",
    default_value=[]
)


cx = on_message(priority=9, block=False)


# 早上好
@scheduler.scheduled_job(
    "cron",
    hour=6,
    minute=1,
)
async def _():
    try:
        bot = get_bot()
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        for g in gl:
            result = image("zao.jpg", "zhenxun")
            try:
                await bot.send_group_msg(group_id=g, message="[[_task|zwa]]早上好" + result)
            except ActionFailed:
                logger.warning(f"{g} 群被禁言中，无法发送早安")
    except Exception as e:
        logger.error(f"早晚安错误 e:{e}")


# 睡觉了
@scheduler.scheduled_job(
    "cron",
    hour=23,
    minute=59,
)
async def _():
    try:
        bot = get_bot()
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        for g in gl:
            result = image("sleep.jpg", "zhenxun")
            try:
                await bot.send_group_msg(
                    group_id=g, message=f"[[_task|zwa]]{NICKNAME}要睡觉了，你们也要早点睡呀" + result
                )
            except ActionFailed:
                logger.warning(f"{g} 群被禁言中，无法发送晚安")
    except Exception as e:
        logger.error(f"早晚安错误 e:{e}")


# 自动更新群组信息
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    try:
        bot = get_bot()
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        for g in gl:
            group_info = await bot.get_group_info(group_id=g)
            await GroupInfo.add_group_info(
                group_info["group_id"],
                group_info["group_name"],
                group_info["max_member_count"],
                group_info["member_count"],
            )
            logger.info(f"自动更新群组 {g} 信息成功")
    except Exception as e:
        logger.error(f"自动更新群组信息错误 e:{e}")


# 自动更新好友信息
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=1,
)
async def _():
    try:
        bot = get_bot()
        fl = await bot.get_friend_list()
        for f in fl:
            if await FriendUser.add_friend_info(f["user_id"], f["nickname"]):
                logger.info(f'自动更新好友 {f["user_id"]} 信息成功')
            else:
                logger.warning(f'自动更新好友 {f["user_id"]} 信息失败')
    except Exception as e:
        logger.error(f"自动更新群组信息错误 e:{e}")


# 自动备份
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=25,
)
async def _():
    if Config.get_config("_backup", "BACKUP_FLAG"):
        _backup_path = Path() / 'backup'
        _backup_path.mkdir(exist_ok=True, parents=True)
        for x in Config.get_config("_backup", "BACKUP_DIR_OR_FILE"):
            try:
                path = Path(x)
                _p = _backup_path / x
                if path.exists():
                    if path.is_dir():
                        if _p.exists():
                            shutil.rmtree(_p, ignore_errors=True)
                        shutil.copytree(x, _p)
                    else:
                        if _p.exists():
                            _p.unlink()
                        shutil.copy(x, _p)
                    logger.info(f'已完成自动备份：{x}')
            except Exception as e:
                logger.error(f"自动备份文件 {x} 发生错误 {type(e)}:{e}")


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
