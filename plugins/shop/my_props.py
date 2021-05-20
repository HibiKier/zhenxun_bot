from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from models.bag_user import UserBag
from nonebot.adapters.cqhttp.permission import GROUP


__plugin_name__ = '商店基础显示'


my_props = on_command("我的道具", priority=5, block=True, permission=GROUP)


@my_props.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    props = await UserBag.get_props(event.user_id, event.group_id)
    if props:
        pname_list = []
        pnum_list = []
        rst = ''
        props = props[:-1].split(',')
        for p in props:
            if p != '':
                if p in pname_list:
                    pnum_list[pname_list.index(p)] += 1
                else:
                    pname_list.append(p)
                    pnum_list.append(1)
        for i in range(len(pname_list)):
            rst += f'{i+1}.{pname_list[i]}\t×{pnum_list[i]}\n'
        await my_props.send('\n' + rst[:-1], at_sender=True)
        logger.info(f'USER {event.user_id} GROUP {event.group_id} 查看我的道具')
    else:
        await my_props.finish('您的背包里没有任何的道具噢~', at_sender=True)











