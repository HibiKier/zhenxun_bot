from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from util.utils import get_message_text, is_number
from models.bag_user import UserBag
from services.db_context import db
from nonebot.adapters.cqhttp.permission import GROUP


__plugin_name__ = '商店购买'
__plugin_usage__ = '格式：购买 名称或序号 数量（选填，默认为1）\n\t示例：购买 好感双倍加持卡Ⅰ\n\t示例：购买 1 4'


buy = on_command("购买", aliases={'购买道具'}, priority=5, block=True, permission=GROUP)

goods = [
    '好感双倍加持卡Ⅰ\t\t售价：30金币\n\t\t今日双倍好感度的概率 + 10%（谁才是真命天子？）（同类道具将覆盖）',
    '好感双倍加持卡Ⅱ\t\t售价：140金币\n\t\t今日双倍好感度的概率 + 20%（平平庸庸~）（同类道具将覆盖）',
    '好感双倍加持卡Ⅲ\t\t售价：250金币\n\t\t今日双倍好感度的概率 + 30%（金币才是真命天子！）（同类道具将覆盖）'
]
glist = []
plist = []
for i in range(len(goods)):
    glist.append(goods[i].split('\t\t')[0])
    plist.append(int(goods[i].split('\t\t')[1].split('：')[1].split('金币')[0]))


@buy.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if get_message_text(event.json()) in ['', '帮助']:
        await buy.finish(__plugin_usage__)
    if get_message_text(event.json()) in ['神秘药水']:
        await buy.finish("你们看看就好啦，这是不可能卖给你们的~", at_sender=True)
    msg = get_message_text(event.json()).strip().split(' ')
    index = -1
    num = 1
    if len(msg) > 1:
        if is_number(msg[1]):
            num = int(msg[1])
    print(msg, num)
    if is_number(msg[0]):
        msg = int(msg[0])
        if msg > len(goods) or msg < 1:
            await buy.finish('请输入正确的商品id！', at_sender=True)
        index = msg - 1
    else:
        if msg[0] in glist:
            for i in range(len(glist)):
                if msg == glist[i]:
                    index = i
                    break
        else:
            await buy.finish('请输入正确的商品名称！', at_sender=True)
    async with db.transaction():
        if index != -1:
            if (await UserBag.get_gold(event.user_id, event.group_id)) < plist[index] * num:
                await buy.finish('您的金币好像不太够哦', at_sender=True)
            if await UserBag.spend_glod(event.user_id, event.group_id, plist[index] * num):
                for _ in range(num):
                    await UserBag.add_props(event.user_id, event.group_id, glist[index])
                await buy.send(f'花费 {plist[index]*num} 金币购买 {glist[index]} ×{num} 成功！', at_sender=True)
                logger.info(f'USER {event.user_id} GROUP {event.group_id} '
                            f'花费 {plist[index]*num} 金币购买 {glist[index]} ×{num} 成功！')
            else:
                await buy.send(f'{glist[index]} 购买失败！', at_sender=True)
                logger.info(f'USER {event.user_id} GROUP {event.group_id} '
                            f'花费 {plist[index]*num} 金币购买 {glist[index]} ×{num} 失败！')










