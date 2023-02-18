from services.log import logger
from utils.utils import scheduler

from .._models import Genshin


@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=1,
)
async def _():
    try:
        await Genshin.all().update(today_query_uid="")
        logger.warning(f"重置原神查询记录成功..")
    except Exception as e:
        logger.error(f"重置原神查询记录失败. {type(e)}:{e}")

