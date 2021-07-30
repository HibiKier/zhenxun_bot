from nonebot import on_command
from utils.utils import get_message_text, get_message_imgs
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import custom_group_welcome
from nonebot.adapters.cqhttp.permission import GROUP
from services.log import logger


__plugin_name__ = "自定义进群欢迎消息"

__plugin_usage__ = """
    自定义进群欢迎消息 [消息] [图片](可省略)
    示例：自定义进群欢迎消息 欢迎新人！[图片]
"""


custom_welcome = on_command(
    "自定义进群欢迎消息",
    aliases={"自定义欢迎消息", "自定义群欢迎消息", "设置群欢迎消息"},
    permission=GROUP,
    priority=5,
    block=True,
)


@custom_welcome.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    if not msg and not imgs:
        await custom_welcome.finish(__plugin_usage__)
    await custom_welcome.send(
        await custom_group_welcome(msg, imgs, event.user_id, event.group_id),
        at_sender=True,
    )
    logger.info(f"USER {event.user_id} GROUP {event.group_id} 自定义群欢迎消息：{msg}")
