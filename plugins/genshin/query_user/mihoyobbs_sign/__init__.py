from typing import Tuple

from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import Command

from services.log import logger

# from .init_task import add_job, scheduler, _sign
# from apscheduler.jobstores.base import JobLookupError
from .._models import Genshin
from .mihoyobbs import *

__zx_plugin_name__ = "米游社自动签到"
__plugin_usage__ = """
usage：
    发送'米游社签到'或绑定原神自动签到
    即可手动/自动进行米游社签到
    （若启用了原神自动签到会在签到原神同时完成米游币领取）
    --> 每天白嫖90-110米游币不香吗
    注：需要重新绑定原神cookie！！！
    遇到问题请提issue或@作者
""".strip()
__plugin_des__ = "米游社自动签到任务"
__plugin_cmd__ = ["米游社签到", "米游社我硬签"]
__plugin_type__ = ("原神相关",)
__plugin_version__ = 0.1
__plugin_author__ = "HDU_Nbsp"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["米游社签到"],
}

mihoyobbs_matcher = on_command("米游社签到", aliases={"米游社我硬签"}, priority=5, block=True)


@mihoyobbs_matcher.handle()
async def _(event: MessageEvent, cmd: Tuple[str, ...] = Command()):
    await mihoyobbs_matcher.send("提交米游社签到申请", at_sender=True)
    return_data = await mihoyobbs_sign(event.user_id)
    if return_data:
        await mihoyobbs_matcher.finish(return_data, at_sender=True)
    else:
        await mihoyobbs_matcher.finish("米游社签到失败，请查看控制台输出", at_sender=True)


async def mihoyobbs_sign(user_id):
    user = await Genshin.get_or_none(user_qq=user_id)
    if not user or not user.uid or not user.cookie:
        await mihoyobbs_matcher.finish("请先绑定uid和cookie！", at_sender=True)
    bbs = mihoyobbs.Mihoyobbs(stuid=user.stuid, stoken=user.stoken, cookie=user.cookie)
    await bbs.init()
    return_data = ""
    if (
        bbs.Task_do["bbs_Sign"]
        and bbs.Task_do["bbs_Read_posts"]
        and bbs.Task_do["bbs_Like_posts"]
        and bbs.Task_do["bbs_Share"]
    ):
        return_data += (
            f"今天的米游社签到任务已经全部完成了！\n"
            f"一共获得{mihoyobbs.today_have_get_coins}个米游币\n目前有{mihoyobbs.Have_coins}个米游币"
        )
        logger.info(
            f"今天已经全部完成了！一共获得{mihoyobbs.today_have_get_coins}个米游币，目前有{mihoyobbs.Have_coins}个米游币"
        )
    else:
        i = 0
        # print("开始签到")
        # print(mihoyobbs.today_have_get_coins)
        while mihoyobbs.today_get_coins != 0 and i < 3:
            # if i > 0:
            await bbs.refresh_list()
            await bbs.signing()
            await bbs.read_posts()
            await bbs.like_posts()
            await bbs.share_post()
            await bbs.get_tasks_list()
            i += 1
        return_data += (
            "\n" + f"今天已经获得{mihoyobbs.today_have_get_coins}个米游币\n"
            f"还能获得{mihoyobbs.today_get_coins}个米游币\n目前有{mihoyobbs.Have_coins}个米游币"
        )
        logger.info(
            f"今天已经获得{mihoyobbs.today_have_get_coins}个米游币，"
            f"还能获得{mihoyobbs.today_get_coins}个米游币，目前有{mihoyobbs.Have_coins}个米游币"
        )
    return return_data
