from nonebot import on_regex
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import scheduler, get_bot
from .data_source import get_epic_free
from utils.manager import group_manager
from configs.config import Config

__zx_plugin_name__ = "epic免费游戏"
__plugin_usage__ = """
usage：
    可以不玩，不能没有，每日白嫖
    指令：
        epic
""".strip()
__plugin_des__ = "可以不玩，不能没有，每日白嫖"
__plugin_cmd__ = ["epic"]
__plugin_version__ = 0.1
__plugin_author__ = "AkashiCoin"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["epic"],
}
__plugin_task__ = {"epic_free_game": "epic免费游戏"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_EPIC_FREE_GAME",
    True,
    help_="被动 epic免费游戏 进群默认开关状态",
    default_value=True,
)

epic = on_regex("^epic$", priority=5, block=True)


@epic.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    Type_Event = "Private"
    if isinstance(event, GroupMessageEvent):
        Type_Event = "Group"
    msg_list, code = await get_epic_free(bot, Type_Event)
    if code == 404:
        await epic.send(msg_list)
    elif isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=msg_list)
    else:
        for msg in msg_list:
            await bot.send_private_msg(user_id=event.user_id, message=msg)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 获取epic免费游戏"
    )


# epic免费游戏
@scheduler.scheduled_job(
    "cron",
    hour=12,
    minute=1,
)
async def _():
    bot = get_bot()
    gl = await bot.get_group_list()
    gl = [g["group_id"] for g in gl]
    msg_list, code = await get_epic_free(bot, "Group")
    for g in gl:
        if await group_manager.check_group_task_status(g, "epic_free_game"):
            try:
                if msg_list and code == 200:
                    await bot.send_group_forward_msg(group_id=g, messages=msg_list)
                else:
                    await bot.send_group_msg(group_id=g)
            except Exception as e:
                logger.error(f"GROUP {g} epic免费游戏推送错误 {type(e)}: {e}")
