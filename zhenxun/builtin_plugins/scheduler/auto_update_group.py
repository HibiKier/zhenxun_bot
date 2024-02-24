import nonebot
from nonebot_plugin_apscheduler import scheduler

from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger

# TODO: 其他平台更新


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
                await GroupConsole.update_or_create(
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
                    logger.debug(
                        f"更新好友信息成功", "自动更新好友", session=f["user_id"]
                    )
                else:
                    logger.debug(
                        f"好友信息已存在", "自动更新好友", session=f["user_id"]
                    )
        except Exception as e:
            logger.error(f"自动更新好友信息错误", "自动更新好友", e=e)
    logger.info("自动更新好友信息成功...")
