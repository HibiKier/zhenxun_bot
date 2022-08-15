from .data_source import genshin_sign
from ..mihoyobbs_sign import mihoyobbs_sign
from models.group_member_info import GroupInfoUser
from utils.message_builder import at
from services.log import logger
from utils.utils import scheduler, get_bot
from apscheduler.jobstores.base import ConflictingIdError
from .._models import Genshin
from datetime import datetime, timedelta
from nonebot import Driver
import nonebot
import random
import pytz


driver: Driver = nonebot.get_driver()


@driver.on_startup
async def _():
    """
    启动时分配定时任务
    """
    g_list = await Genshin.get_all_auto_sign_user()
    for u in g_list:
        if u.auto_sign_time:
            if date := await Genshin.random_sign_time(u.uid):
                scheduler.add_job(
                    _sign,
                    "date",
                    run_date=date.replace(microsecond=0),
                    id=f"genshin_auto_sign_{u.uid}_{u.user_qq}_0",
                    args=[u.user_qq, u.uid, 0],
                )
                logger.info(
                    f"genshin_sign add_job：USER：{u.user_qq} UID：{u.uid} " f"{date} 原神自动签到"
                )


def add_job(user_id: int, uid: int, date: datetime):
    try:
        scheduler.add_job(
            _sign,
            "date",
            run_date=date.replace(microsecond=0),
            id=f"genshin_auto_sign_{uid}_{user_id}_0",
            args=[user_id, uid, 0],
        )
        logger.debug(f"genshin_sign add_job：{date.replace(microsecond=0)} 原神自动签到")
    except ConflictingIdError:
        pass


async def _sign(user_id: int, uid: int, count: int):
    """
    执行签到任务
    :param user_id: 用户id
    :param uid: uid
    :param count: 执行次数
    """
    try:
        return_data = await mihoyobbs_sign(user_id)
    except Exception as e:
        logger.error(f"mihoyobbs_sign error：{e}")
        return_data = "米游社签到失败，请尝试发送'米游社签到'进行手动签到"
    if count < 3:
        try:
            msg = await genshin_sign(uid)
            next_time = await Genshin.random_sign_time(uid)
            msg += f"\n下一次签到时间为：{next_time.replace(microsecond=0)}"
            logger.info(f"USER：{user_id} UID：{uid} 原神自动签到任务发生成功...")
            try:
                scheduler.add_job(
                    _sign,
                    "date",
                    run_date=next_time.replace(microsecond=0),
                    id=f"genshin_auto_sign_{uid}_{user_id}_0",
                    args=[user_id, uid, 0],
                )
            except ConflictingIdError:
                msg += "\n定时任务设定失败..."
        except Exception as e:
            logger.error(f"USER：{user_id} UID：{uid} 原神自动签到任务发生错误 {type(e)}：{e}")
            msg = None
        if not msg:
            now = datetime.now(pytz.timezone("Asia/Shanghai"))
            if now.hour < 23:
                random_hours = random.randint(1, 23 - now.hour)
                next_time = now + timedelta(hours=random_hours)
                scheduler.add_job(
                    _sign,
                    "date",
                    run_date=next_time.replace(microsecond=0),
                    id=f"genshin_auto_sign_{uid}_{user_id}_{count}",
                    args=[user_id, uid, count + 1],
                )
                msg = (
                    f"{now.replace(microsecond=0)} 原神"
                    f"签到失败，将在 {next_time.replace(microsecond=0)} 时重试！"
                )
            else:
                msg = "今日原神签到失败，请手动签到..."
                logger.debug(f"USER：{user_id} UID：{uid} 原神今日签到失败...")
    else:
        msg = "今日原神自动签到重试次数已达到3次，请手动签到。"
        logger.debug(f"USER：{user_id} UID：{uid} 原神今日签到失败次数打到 3 次...")
    bot = get_bot()
    if bot:
        if user_id in [x["user_id"] for x in await bot.get_friend_list()]:
            await bot.send_private_msg(user_id=user_id, message=return_data)
            await bot.send_private_msg(user_id=user_id, message=msg)
        else:
            if not (group_id := await Genshin.get_bind_group(uid)):
                group_list = await GroupInfoUser.get_user_all_group(user_id)
                if group_list:
                    group_id = group_list[0]
            await bot.send_group_msg(
                group_id=group_id, message=at(user_id) + msg
            )
