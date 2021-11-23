from nonebot import on_command
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import get_message_text, is_number
from models.bag_user import BagUser
from services.db_context import db
from nonebot.adapters.cqhttp.permission import GROUP
from .models.goods_info import GoodsInfo


__zx_plugin_name__ = "商店 - 购买道具"
__plugin_usage__ = """
usage：
    购买道具
    指令：
        购买 [序号或名称] ?[数量=1]
        示例：购买 好感双倍加持卡Ⅰ
        示例：购买 1 4
""".strip()
__plugin_des__ = "商店 - 购买道具"
__plugin_cmd__ = ["购买 [序号或名称] ?[数量=1]"]
__plugin_type__ = ('商店',)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "购买道具"],
}


buy = on_command("购买", aliases={"购买道具"}, priority=5, block=True, permission=GROUP)


@buy.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if get_message_text(event.json()) in ["神秘药水"]:
        await buy.finish("你们看看就好啦，这是不可能卖给你们的~", at_sender=True)
    goods_lst = await GoodsInfo.get_all_goods()
    goods_name_lst = [x.goods_name for x in goods_lst]
    msg = get_message_text(event.json()).strip().split(" ")
    num = 1
    if len(msg) > 1:
        if is_number(msg[1]):
            num = int(msg[1])
        else:
            await buy.finish("购买的数量要是数字！", at_sender=True)
    # print(msg, num)
    if is_number(msg[0]):
        msg = int(msg[0])
        if msg > len(goods_lst) or msg < 1:
            await buy.finish("请输入正确的商品id！", at_sender=True)
        goods = goods_lst[msg - 1]
    else:
        if msg[0] in goods_name_lst:
            for i in range(len(goods_name_lst)):
                if msg[0] == goods_name_lst[i]:
                    goods = goods_lst[i]
                    break
            else:
                await buy.finish("请输入正确的商品名称！")
        else:
            await buy.finish("请输入正确的商品名称！", at_sender=True)
    async with db.transaction():
        if (
            await BagUser.get_gold(event.user_id, event.group_id)
        ) < goods.goods_price * num:
            await buy.finish("您的金币好像不太够哦", at_sender=True)
        if await BagUser.spend_gold(
            event.user_id, event.group_id, goods.goods_price * num
        ):
            for _ in range(num):
                await BagUser.add_props(event.user_id, event.group_id, goods.goods_name)
            await buy.send(
                f"花费 {goods.goods_price*num} 金币购买 {goods.goods_name} ×{num} 成功！",
                at_sender=True,
            )
            logger.info(
                f"USER {event.user_id} GROUP {event.group_id} "
                f"花费 {goods.goods_price*num} 金币购买 {goods.goods_name} ×{num} 成功！"
            )
        else:
            await buy.send(f"{goods.goods_name} 购买失败！", at_sender=True)
            logger.info(
                f"USER {event.user_id} GROUP {event.group_id} "
                f"花费 {goods.goods_price*num} 金币购买 {goods.goods_name} ×{num} 失败！"
            )
