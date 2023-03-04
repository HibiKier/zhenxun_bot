import random
from datetime import datetime, timedelta

import nonebot
import pytz
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from nonebot import Driver
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.plugin import require

from configs.config import Config
from models.group_member_info import GroupInfoUser
from services.log import logger
from utils.message_builder import at
from utils.utils import get_bot, scheduler

from .._models import Genshin

driver: Driver = nonebot.get_driver()


require("query_memo")

from ..query_memo import get_memo

global_map = {}


class UserManager:
    def __init__(self, max_error_count: int = 3):
        self._data = []
        self._overflow_data = []
        self._error_count = {}
        self.max_error_count = max_error_count

    def append(self, o: str):
        if o not in self._data:
            self._data.append(o)

    def remove(self, o: str):
        if o in self._data:
            self._data.remove(o)

    def exists(self, o: str):
        return o in self._data

    def add_error_count(self, uid: str):
        if uid in self._error_count.keys():
            self._error_count[uid] += 1
        else:
            self._error_count[uid] = 1

    def check(self, uid: str) -> bool:
        if uid in self._error_count.keys():
            return self._error_count[uid] == self.max_error_count
        return False

    def remove_error_count(self, uid):
        if uid in self._error_count.keys():
            del self._error_count[uid]

    def add_overflow(self, uid: str):
        if uid not in self._overflow_data:
            self._overflow_data.append(uid)

    def remove_overflow(self, uid: str):
        if uid in self._overflow_data:
            self._overflow_data.remove(uid)

    def is_overflow(self, uid: str) -> bool:
        return uid in self._overflow_data


user_manager = UserManager()


@driver.on_startup
async def _():
    """
    启动时分配定时任务
    """
    g_list = await Genshin.filter(resin_remind=True).all()
    update_list = []
    date = datetime.now(pytz.timezone("Asia/Shanghai")) + timedelta(seconds=30)
    for u in g_list:
        if u.resin_remind:
            if u.resin_recovery_time:
                if u.resin_recovery_time and u.resin_recovery_time > datetime.now(
                    pytz.timezone("Asia/Shanghai")
                ):
                    # date = await Genshin.get_user_resin_recovery_time(u.uid)  # 不能要,因为可能在这期间用户使用了树脂
                    add_job(u.user_qq, u.uid)
                    # scheduler.add_job(
                    #     _remind,
                    #     "date",
                    #     run_date=date.replace(microsecond=0),
                    #     id=f"genshin_resin_remind_{u.uid}_{u.user_qq}",
                    #     args=[u.user_qq, u.uid],
                    # )
                    logger.info(
                        f"genshin_resin_remind add_job：USER：{u.user_qq} UID：{u.uid}启动原神树脂提醒 "
                    )
                else:
                    u.resin_recovery_time = None  # type: ignore
                    update_list.append(u)
                    add_job(u.user_qq, u.uid)
                    logger.info(
                        f"genshin_resin_remind add_job CHECK：USER：{u.user_qq} UID：{u.uid}启动原神树脂提醒 "
                    )
            else:
                add_job(u.user_qq, u.uid)
                logger.info(
                    f"genshin_resin_remind add_job CHECK：USER：{u.user_qq} UID：{u.uid}启动原神树脂提醒 "
                )
    if update_list:
        await Genshin.bulk_update(update_list, ["resin_recovery_time"])


def add_job(user_id: int, uid: int):
    # 移除
    try:
        scheduler.remove_job(f"genshin_resin_remind_{uid}_{user_id}")
    except JobLookupError:
        pass
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
    user = await Genshin.get_or_none(user_qq=user_id, uid=int(uid))
    uid = str(uid)
    if uid[0] in ["1", "2"]:
        server_id = "cn_gf01"
    elif uid[0] == "5":
        server_id = "cn_qd01"
    else:
        return
    data, code = await get_memo(uid, server_id)
    now = datetime.now(pytz.timezone("Asia/Shanghai"))
    next_time = None
    if code == 200:
        current_resin = int(data["current_resin"])  # 当前树脂
        max_resin = int(data["max_resin"])  # 最大树脂
        msg = f"你的已经存了 {current_resin} 个树脂了！不要忘记刷掉！"
        # resin_recovery_time = data["resin_recovery_time"]  # 树脂全部回复时间
        if current_resin < max_resin:
            user_manager.remove(uid)
            user_manager.remove_overflow(uid)
        if current_resin < max_resin - 40:
            next_time = now + timedelta(minutes=(max_resin - 40 - current_resin) * 8)
        elif max_resin - 40 <= current_resin < max_resin - 20:
            next_time = now + timedelta(minutes=(max_resin - 20 - current_resin) * 8)
        elif max_resin - 20 <= current_resin < max_resin:
            next_time = now + timedelta(minutes=(max_resin - current_resin) * 8)
        elif current_resin == max_resin:
            custom_overflow_resin = Config.get_config(
                "resin_remind", "CUSTOM_RESIN_OVERFLOW_REMIND"
            )
            if user_manager.is_overflow(uid) and custom_overflow_resin:
                next_time = now + timedelta(minutes=custom_overflow_resin * 8)
                user_manager.add_overflow(uid)
                user_manager.remove(uid)
                msg = f"你的树脂都溢出 {custom_overflow_resin} 个了！浪费可耻！"
            else:
                next_time = now + timedelta(minutes=40 * 8 + random.randint(5, 50))

        if not user_manager.exists(uid) and current_resin >= max_resin - 40:
            if current_resin == max_resin:
                user_manager.append(uid)
            bot = get_bot()
            if bot:
                if user_id in [x["user_id"] for x in await bot.get_friend_list()]:
                    await bot.send_private_msg(
                        user_id=user_id,
                        message=msg,
                    )
                else:
                    if user:
                        group_id = user.bind_group
                        if not group_id:
                            if group_list := await GroupInfoUser.get_user_all_group(
                                user_id
                            ):
                                group_id = group_list[0]
                        try:
                            await bot.send_group_msg(
                                group_id=group_id, message=at(user_id) + msg
                            )
                        except ActionFailed as e:
                            logger.error(f"树脂提醒推送发生错误 {type(e)}：{e}")

    if not next_time:
        if user_manager.check(uid) and Config.get_config(
            "resin_remind", "AUTO_CLOSE_QUERY_FAIL_RESIN_REMIND"
        ):
            if user:
                user.resin_remind = False
                user.resin_recovery_time = None
                await user.save(update_fields=["resin_recovery_time", "resin_remind"])
        next_time = now + timedelta(minutes=(20 + random.randint(5, 20)) * 8)
        user_manager.add_error_count(uid)
    else:
        user_manager.remove_error_count(uid)
    if user:
        user.resin_recovery_time = next_time
        await user.save(update_fields=["resin_recovery_time", "resin_remind"])
    scheduler.add_job(
        _remind,
        "date",
        run_date=next_time,
        id=f"genshin_resin_remind_{uid}_{user_id}",
        args=[user_id, uid],
    )
    logger.info(
        f"genshin_resin_remind add_job：USER：{user_id} UID：{uid} " f"{next_time} 原神树脂提醒"
    )
