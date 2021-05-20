from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
from util.utils import get_message_text, is_number
from services.log import logger
from util.init_result import at


__plugin_name__ = '联系管理员'
__plugin_usage__ = '滴滴滴- 后接内容 联系管理员'


dialogue = on_command("[滴滴滴]", aliases={"滴滴滴-"}, priority=1, block=True)
reply = on_command("/t",  priority=1, permission=SUPERUSER, block=True)


@dialogue.handle()
async def _(bot: Bot, event: Event, state: T_State):
    uid = event.user_id
    coffee = int(list(bot.config.superusers)[0])
    text = get_message_text(event.json())
    if not text or text in ['帮助']:
        await dialogue.send("请发送[滴滴滴]+您要说的内容~", at_sender=True)
    else:
        if event.get_event_name() == "message.private.friend":
            group_id = ""
        else:
            group_id = event.group_id
        await bot.send_private_msg(user_id=coffee, message=f'Q{uid}@群{group_id}\n{text}')
        await dialogue.send(f'您的话已发送至管理员！\n======\n{text}', at_sender=True)
        logger.info(f"Q{uid}@群{group_id} 联系管理员：{coffee} text:{text}")


@reply.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if get_message_text(event.json()) in ['帮助']:
        await reply.finish(f'/t qq group text')
    msg = get_message_text(event.json()).split(" ")
    user_id = int(msg[0])
    if is_number(msg[1]) and len(msg[1]) > 5:
        group_id = int(msg[1])
        text = msg[2]
    else:
        group_id = ""
        text = msg[1]
    if group_id:
        await bot.send_group_msg(group_id=group_id, message=at(user_id) + "\n管理员回复\n=======\n" + text)
    else:
        if user_id in [qq['user_id'] for qq in await bot.get_friend_list()]:
            await bot.send_private_msg(user_id=user_id, message="管理员回复\n=======\n" + text)
            await reply.finish("发送成功", at_sender=True)
        else:
            await reply.send(f"对象不是{list(bot.config.nickname)[0]}的好友...", at_sender=True)
