from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from util.utils import is_number, get_message_text
from models.bag_user import UserBag
from nonebot.adapters.cqhttp.permission import GROUP
from services.db_context import db
from .data_source import effect


__plugin_name__ = '使用道具'
__plugin_usage__ = '输入 “使用道具 xxx（序号 或 道具名称）“ 即可使用道具\n【注】序号以我的道具序号为准，更推荐使用道具名称使用道具（怕出错）'


use_props = on_command("使用道具", priority=5, block=True, permission=GROUP)


@use_props.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg in ['', '帮助']:
        await use_props.finish(__plugin_usage__)
    props = await UserBag.get_props(event.user_id, event.group_id)
    if props:
        async with db.transaction():
            pname_list = []
            props = props[:-1].split(',')
            for p in props:
                if p != '':
                    if p not in pname_list:
                        pname_list.append(p)
            if is_number(msg):
                if 0 < int(msg) <= len(pname_list):
                    name = pname_list[int(msg) - 1]
                else:
                    await use_props.finish('仔细看看自己的道具仓库有没有这个道具？', at_sender=True)
            else:
                if msg not in pname_list:
                    await use_props.finish('道具名称错误！', at_sender=True)
                name = msg
            if await UserBag.del_props(event.user_id, event.group_id, name) and\
                    await effect(event.user_id, event.group_id, name):
                await use_props.send(f'使用道具 {name} 成功！', at_sender=True)
                logger.info(f'USER {event.user_id} GROUP {event.group_id} 使用道具 {name} 成功')
            else:
                await use_props.send(f'使用道具 {name} 失败！', at_sender=True)
                logger.info(f'USER {event.user_id} GROUP {event.group_id} 使用道具 {name} 失败')
    else:
        await use_props.send('您的背包里没有任何的道具噢~', at_sender=True)











