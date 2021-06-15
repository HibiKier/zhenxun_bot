from util.utils import scheduler
from models.bag_user import BagUser
from services.log import logger


# 重置每日金币
@scheduler.scheduled_job(
    'cron',
    # year=None,
    # month=None,
    # day=None,
    # week=None,
    # day_of_week="mon,tue,wed,thu,fri",
    hour=0,
    minute=1,
    # second=None,
    # start_date=None,
    # end_date=None,
    # timezone=None,
)
async def _():
    try:
        user_list = await BagUser.get_user_all()
        for user in user_list:
            await user.update(
                get_today_gold=0,
                spend_today_gold=0,
            ).apply()
    except Exception as e:
        logger.error(f'重置每日金币错误 e:{e}')










