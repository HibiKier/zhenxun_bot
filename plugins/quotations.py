from nonebot import on_command
import random
from util.utils import get_lines
from configs.path_config import TXT_PATH
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State


__plugin_name__ = '语录'
__plugin_usage__ = '用法： 二次元语录给你力量'


lines = get_lines(TXT_PATH + "yulu.txt")


quotations = on_command("语录", aliases={'二次元', '二次元语录'}, priority=5, block=True)


@quotations.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ['帮助']:
        await quotations.finish(__plugin_usage__)
    result = random.choice(lines)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'}) 发送语录:"
        + result[:-1])
    await quotations.finish(result[:-1])

