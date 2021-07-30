from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from utils.utils import scheduler, get_bot
from .data_source import get_epic_game
from models.group_remind import GroupRemind
from nonebot.adapters.cqhttp.exception import ActionFailed

__plugin_name__ = "epic免费游戏提醒"

__plugin_usage__ = "用法：发送’epic‘"


epic = on_command("epic", priority=5, block=True)


@epic.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    result, code = await get_epic_game()
    await epic.send(result)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
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
    gl = await bot.get_group_list(self_id=bot.self_id)
    gl = [g["group_id"] for g in gl]
    for g in gl:
        if await GroupRemind.get_status(g, "epic"):
            result, code = await get_epic_game()
            if code == 200:
                try:
                    await bot.send_group_msg(group_id=g, message=result)
                except ActionFailed:
                    logger.error(f"{g}群 epic免费游戏推送错误")
