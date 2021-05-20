from nonebot import on_command
from util.utils import get_message_text
from services.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
from .data_source import translate_msg


__plugin_name__ = '翻译'


translate = on_command("translate", aliases={'英翻', '翻英',
                                             '日翻', '翻日',
                                             '韩翻', '翻韩'
                                             }, priority=5, block=True)


@translate.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg:
        state['msg'] = msg


@translate.got('msg', prompt='你要翻译的消息是啥？')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = state['msg']
    if len(msg) > 150:
        await translate.finish('翻译过长！请不要超过150字', at_sender=True)
    await translate.send(await translate_msg(state["_prefix"]["raw_command"], msg))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if event.message_type != 'private' else 'private'}) 使用翻译：{msg}")




