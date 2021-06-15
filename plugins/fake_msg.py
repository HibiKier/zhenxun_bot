from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot import on_command
from util.utils import get_message_imgs, get_message_text
from util.init_result import share
from services.log import logger


__plugin_name = '假消息'

__plugin_usage__ = '用法：\n格式：假消息 [网址] [标题] [内容](可省) [图片](可省)\n' \
            '示例：假消息 www.4399.com 我喜欢萝莉 为什么我喜欢... [图片]'


fake_msg = on_command('假消息', priority=5, block=True)


@fake_msg.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json()).split(' ')
    img = get_message_imgs(event.json())
    if len(msg) > 1:
        if len(msg) == 2:
            url = msg[0]
            title = msg[1]
            content = ''
        else:
            url = msg[0]
            title = msg[1]
            content = msg[2]
        if img:
            img = img[0]
        else:
            img = ''
        if url.find('http://') == -1:
            url = 'http://' + url
        await fake_msg.send(share(url, title, content, img))
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
            f" 构造假消息 url {url}， title {title}， content {content}")
    else:
        await fake_msg.finish('消息格式错误：\n网址 标题 内容（可省略） 图片（可省略）')














