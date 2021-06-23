from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message
from nonebot.permission import SUPERUSER
from util.utils import get_message_text, is_number, get_message_imgs
from util.init_result import image
from services.log import logger
from util.init_result import at


__plugin_name__ = '联系管理员'
__plugin_usage__ = '用法：滴滴滴- [消息]'


dialogue_data = {}


dialogue = on_command("[滴滴滴]", aliases={"滴滴滴-"}, priority=1, block=True)
reply = on_command("/t",  priority=1, permission=SUPERUSER, block=True)


@dialogue.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    uid = event.user_id
    coffee = int(list(bot.config.superusers)[0])
    text = get_message_text(event.json())
    img_msg = ''
    for img in get_message_imgs(event.json()):
        img_msg += image(img)
    if not text or text in ['帮助']:
        await dialogue.send("请发送[滴滴滴]+您要说的内容~", at_sender=True)
    else:
        if event.get_event_name() == "message.private.friend":
            group_id = 0
        else:
            group_id = event.group_id
        await bot.send_private_msg(user_id=coffee, message=Message(f'Q{uid}@群{group_id}\n{text} {img_msg}'))
        await dialogue.send(Message(f'您的话已发送至管理员！\n======\n{text}{img_msg}'), at_sender=True)
        nickname = event.sender.nickname if event.sender.nickname else event.sender.card
        dialogue_data[len(dialogue_data)] = {'nickname': nickname, 'user_id': event.user_id,
                                             'group_id': group_id, 'msg': text}
        # print(dialogue_data)
        logger.info(f"Q{uid}@群{group_id} 联系管理员：{coffee} text:{text}")


@reply.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg in ['帮助']:
        await reply.finish(f'/t [qq] [group] [text] -> 回复指定用户\n'
                           f'/t [qq] [text] -> 私聊用户\n'
                           f'/t -1 [group] -> 在某群发送消息\n'
                           f'/t [id] [text] -> 回复指定id的对话')
    if not msg:
        result = ''
        for key in dialogue_data.keys():
            result += f'{key}：{dialogue_data[key]["nickname"]}({dialogue_data[key]["user_id"]})' \
                      f' @群 {dialogue_data[key]["group_id"]}\n-------\n{dialogue_data[key]["msg"]}\n-------\n'
        await reply.finish(result[:-1])
    msg = msg.split(" ")
    text = ''
    group_id = 0
    user_id = -1
    if is_number(msg[0]):
        if len(msg[0]) < 3:
            msg[0] = int(msg[0])
            if msg[0] >= 0:
                id_ = msg[0]
                user_id = dialogue_data[id_]["user_id"]
                group_id = dialogue_data[id_]["group_id"]
                text = msg[1]
                dialogue_data.pop(id_)
            else:
                user_id = 0
                if is_number(msg[1]):
                    group_id = int(msg[1])
                    text = msg[2]
                else:
                    await reply.finish('群号错误...', at_sender=True)
        else:
            user_id = int(msg[0])
            if is_number(msg[1]) and len(msg[1]) > 5:
                group_id = int(msg[1])
                text = msg[2]
            else:
                group_id = 0
                text = msg[1]
    else:
        await reply.finish('请输入数字..', at_sender=True)
    for img in get_message_imgs(event.json()):
        text += image(img)
    if group_id:
        if user_id:
            await bot.send_group_msg(group_id=group_id, message=at(user_id) + "\n管理员回复\n=======\n" + text)
            await reply.finish("发送成功", at_sender=True)
        else:
            await bot.send_group_msg(group_id=group_id, message=text)
            await reply.finish("发送成功", at_sender=True)
    else:
        if user_id in [qq['user_id'] for qq in await bot.get_friend_list()]:
            await bot.send_private_msg(user_id=user_id, message="管理员回复\n=======\n" + text)
            await reply.finish("发送成功", at_sender=True)
        else:
            await reply.send(f"对象不是{list(bot.config.nickname)[0]}的好友...", at_sender=True)
