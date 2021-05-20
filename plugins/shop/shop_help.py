from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from util.img_utils import CreateImg
from configs.path_config import IMAGE_PATH
from util.init_result import image


__plugin_name__ = '商店'


shop_help = on_command("商店", priority=5, block=True)

goods = [
    '好感双倍加持卡Ⅰ\t\t售价：30金币\n\t\t下次签到双倍好感度的概率 + 10%（谁才是真命天子？）（同类商品将覆盖）',
    '好感双倍加持卡Ⅱ\t\t售价：150金币\n\t\t下次签到双倍好感度的概率 + 20%（平平庸庸~）（同类商品将覆盖）',
    '好感双倍加持卡Ⅲ\t\t售价：250金币\n\t\t下次签到双倍好感度的概率 + 30%（金币才是真命天子！）（同类商品将覆盖）'
]

result = ''
for i in range(len(goods)):
    result += f'{i + 1}.{goods[i]}\n'
shop = CreateImg(1000, 1000, background=IMAGE_PATH + 'other/shop.png', font_size=20)
shop.text((100, 170), '注【通过 数字 或者 商品名称 购买】')
shop.text((20, 230), result)
shop.text((20, 900), '神秘药水\t\t售价：9999999金币\n\t\t鬼知道会有什么效果~')
shop.save(IMAGE_PATH + 'shop.png')


@shop_help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await shop_help.send(image('shop.png'))









