from nonebot import on_command, on_regex
from nonebot.rule import to_me
from .query_resource import get_resource_map_mes, get_resource_list_mes, up_label_and_point_list
from utils.utils import get_message_text, scheduler
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.typing import T_State
import os
from services.log import logger
import re
try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = '原神资源查询'

__plugin_usage__ = '用法：\n' \
            '\t原神资源查询 [消息]\n' \
            '\t原神资源列表\n' \
            '\t[消息]在哪\n' \
            '\t哪有[消息]\n' \
            '[消息] = 资源名称'

qr = on_command("原神资源查询", priority=5, block=True)
qr_lst = on_command("原神资源列表", priority=5, block=True)
rex_qr = on_regex('.*?(在哪|在哪里|哪有|哪里有).*?', rule=to_me(), priority=5, block=True)


with open(os.path.dirname(__file__) + '/resource_type_id.json', 'r', encoding='utf-8') as f:
    in_list = [n['name'] for n in json.load(f).values()]


@qr.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    resource_name = get_message_text(event.json())
    if resource_name == "" or resource_name not in in_list:
        return

    await qr.send(await get_resource_map_mes(resource_name), at_sender=True)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
        f" 查询原神材料:" + resource_name)


@rex_qr.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg.find('在哪') != -1:
        rs = re.search('(.*)在哪.*?', msg)
        resource_name = rs.group(1) if rs else ''
    else:
        rs = re.search('.*?(哪有|哪里有)(.*)', msg)
        resource_name = rs.group(2) if rs else ''
    if resource_name:
        msg = await get_resource_map_mes(resource_name)
        if msg == '发送 原神资源列表 查看所有资源名称':
            return
        await rex_qr.send(msg, at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP {event.group_id if event.message_type != 'private' else 'private'})"
            f" 查询原神材料:" + resource_name)


@qr_lst.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    # 长条消息经常发送失败，所以只能这样了
    mes_list = []
    txt = get_resource_list_mes()
    txt_list = txt.split("\n")
    if event.message_type == 'group':
        for txt in txt_list:
            data = {
                "type": "node",
                "data": {
                    "name": f"这里是{list(bot.config.nickname)[0]}酱",
                    "uin": f"{bot.self_id}",
                    "content": txt
                }
            }
            mes_list.append(data)
    # await bot.send(ev, get_resource_list_mes(), at_sender=True)
    if event.message_type == 'group':
        await bot.send_group_forward_msg(group_id=event.group_id, messages=mes_list)
    else:
        rst = ''
        for i in range(len(txt_list)):
            rst += txt_list[i] + '\n'
            if i % 5 == 0:
                if rst:
                    await qr_lst.send(rst)
                rst = ''

        # await qr_lst.send(Message(mes_list))


@scheduler.scheduled_job(
    'cron',
    hour=5,
    minute=1,
)
async def _():
    try:
        await up_label_and_point_list()
        logger.info(f'每日更新原神材料信息成功！')
    except Exception as e:
        logger.error(f'每日更新原神材料信息错误：{e}')
