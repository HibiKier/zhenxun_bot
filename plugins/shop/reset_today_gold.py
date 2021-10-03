from utils.utils import scheduler
from models.bag_user import BagUser
from services.log import logger


__zx_plugin_name__ = "每日金币重置 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


# 重置每日金币
@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    try:
        user_list = await BagUser.get_all_users()
        for user in user_list:
            await user.update(
                get_today_gold=0,
                spend_today_gold=0,
            ).apply()
    except Exception as e:
        logger.error(f"重置每日金币错误 e:{e}")
