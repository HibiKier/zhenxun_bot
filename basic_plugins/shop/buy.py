from nonebot import on_command

from models.user_shop_gold_log import UserShopGoldLog
from services.log import logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import CommandArg
from utils.utils import is_number
from models.bag_user import BagUser
from services.db_context import db
from nonebot.adapters.onebot.v11.permission import GROUP
from models.goods_info import GoodsInfo
import time


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
__plugin_type__ = ("商店",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "购买道具"],
}
__plugin_cd_limit__ = {"cd": 3}


buy = on_command("购买", aliases={"购买道具"}, priority=5, block=True, permission=GROUP)


@buy.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    goods = None
    if arg.extract_plain_text().strip() in ["神秘药水"]:
        await buy.finish("你们看看就好啦，这是不可能卖给你们的~", at_sender=True)
    goods_list = [
        x
        for x in await GoodsInfo.get_all_goods()
        if x.goods_limit_time > time.time() or x.goods_limit_time == 0
    ]
    goods_name_list = [x.goods_name for x in goods_list]
    msg = arg.extract_plain_text().strip().split()
    num = 1
    if len(msg) > 1:
        if is_number(msg[1]) and int(msg[1]) > 0:
            num = int(msg[1])
        else:
            await buy.finish("购买的数量要是数字且大于0！", at_sender=True)
    if is_number(msg[0]):
        msg = int(msg[0])
        if msg > len(goods_name_list) or msg < 1:
            await buy.finish("请输入正确的商品id！", at_sender=True)
        goods = goods_list[msg - 1]
    else:
        if msg[0] in goods_name_list:
            for i in range(len(goods_name_list)):
                if msg[0] == goods_name_list[i]:
                    goods = goods_list[i]
                    break
            else:
                await buy.finish("请输入正确的商品名称！")
        else:
            await buy.finish("请输入正确的商品名称！", at_sender=True)
    async with db.transaction():
        if (
            await BagUser.get_gold(event.user_id, event.group_id)
        ) < goods.goods_price * num * goods.goods_discount:
            await buy.finish("您的金币好像不太够哦", at_sender=True)
        flag, n = await GoodsInfo.check_user_daily_purchase(
            goods, event.user_id, event.group_id, num
        )
        if flag:
            await buy.finish(f"该次购买将超过每日次数限制，目前该道具还可以购买{n}次哦", at_sender=True)
        if await BagUser.buy_property(event.user_id, event.group_id, goods, num):
            await GoodsInfo.add_user_daily_purchase(
                goods, event.user_id, event.group_id, num
            )
            await buy.send(
                f"花费 {goods.goods_price * num * goods.goods_discount} 金币购买 {goods.goods_name} ×{num} 成功！",
                at_sender=True,
            )
            logger.info(
                f"USER {event.user_id} GROUP {event.group_id} "
                f"花费 {goods.goods_price*num} 金币购买 {goods.goods_name} ×{num} 成功！"
            )
            await UserShopGoldLog.add_shop_log(
                event.user_id,
                event.group_id,
                0,
                goods.goods_name,
                num,
                goods.goods_price * num * goods.goods_discount,
            )
        else:
            await buy.send(f"{goods.goods_name} 购买失败！", at_sender=True)
            logger.info(
                f"USER {event.user_id} GROUP {event.group_id} "
                f"花费 {goods.goods_price * num * goods.goods_discount} 金币购买 {goods.goods_name} ×{num} 失败！"
            )
