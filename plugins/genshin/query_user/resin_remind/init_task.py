from utils.utils import get_bot, scheduler
from utils.message_builder import at
from models.group_member_info import GroupInfoUser
from apscheduler.jobstores.base import ConflictingIdError
from nonebot import Driver
from ..models import Genshin
from datetime import datetime, timedelta
from services.log import logger
from nonebot.plugin import require
import time
import nonebot
import pytz


driver: Driver = nonebot.get_driver()


get_memo = require('query_memo').get_memo


class UserManager:

    def __init__(self):
        self._data = []

    def append(self, o: str):
        if o not in self._data:
            self._data.append(o)

    def remove(self, o: str):
        if o in self._data:
            self._data.remove(o)

    def exists(self, o: str):
        return o in self._data


user_manager = UserManager()


@driver.on_startup
async def _():
    """
    启动时分配定时任务
    """
    g_list = await Genshin.get_all_resin_remind_user()
    for u in g_list:
        if u.resin_recovery_time and await Genshin.get_user_resin_recovery_time(
            u.uid
        ) > datetime.now(pytz.timezone("Asia/Shanghai")):
            date = await Genshin.get_user_resin_recovery_time(u.uid)
            scheduler.add_job(
                _remind,
                "date",
                run_date=date.replace(microsecond=0),
                id=f"genshin_resin_remind_{u.uid}_{u.user_qq}",
                args=[u.user_qq, u.uid],
            )
            logger.info(
                f"genshin_resin_remind add_job：USER：{u.user_qq} UID：{u.uid} "
                f"{date} 原神树脂提醒"
            )


def add_job(user_id: int, uid: int):
    date = datetime.now(pytz.timezone("Asia/Shanghai")) + timedelta(seconds=30)
    try:
        scheduler.add_job(
            _remind,
            "date",
            run_date=date.replace(microsecond=0),
            id=f"genshin_resin_remind_{uid}_{user_id}",
            args=[user_id, uid],
        )
    except ConflictingIdError:
        pass


async def _remind(user_id: int, uid: str):
    uid = str(uid)
    if uid[0] in ["1", "2"]:
        server_id = "cn_gf01"
    elif uid[0] == "5":
        server_id = "cn_qd01"
    else:
        return
    data, code = await get_memo(uid, server_id)
    if code == 200:
        current_resin = data["current_resin"]  # 当前树脂
        max_resin = data["max_resin"]  # 最大树脂
        resin_recovery_time = data["resin_recovery_time"]  # 树脂全部回复时间
        if max_resin - current_resin > 5:
            user_manager.remove(uid)
            next_time = datetime.strptime(time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(time.time() + float(resin_recovery_time))
            ), "%Y-%m-%d %H:%M:%S")
            await Genshin.set_user_resin_recovery_time(int(uid), next_time)
            scheduler.add_job(
                _remind,
                "date",
                run_date=next_time,
                id=f"genshin_resin_remind_{uid}_{user_id}",
                args=[user_id, uid],
            )
            logger.info(f"genshin_resin_remind add_job：{next_time.replace(microsecond=0)} 原神树脂提醒")
        else:
            if not user_manager.exists(uid):
                user_manager.append(uid)
                bot = get_bot()
                if bot:
                    if user_id in [x["user_id"] for x in await bot.get_friend_list()]:
                        await bot.send_private_msg(
                            user_id=user_id,
                            message=f"树脂已经 {current_resin} 个啦" f"，马上就要溢出了！快快刷掉刷掉！",
                        )
                    else:
                        group_list = await GroupInfoUser.get_user_all_group(user_id)
                        if group_list:
                            await bot.send_group_msg(
                                group_id=group_list[0],
                                message=at(user_id) + f"树脂已经 {current_resin} 个啦"
                                f"，马上就要溢出了！快快刷掉刷掉！",
                            )
