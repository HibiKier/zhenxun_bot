from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Depends
from models.user_shop_gold_log import UserShopGoldLog
from models.bag_user import BagUser
from utils.message_builder import at


def cost_gold(gold: int):
    """
    说明:
        插件方法调用使用金币
    参数:
        :param gold: 金币数量
    """
    async def dependency(matcher: Matcher, event: GroupMessageEvent):
        if (await BagUser.get_gold(event.user_id, event.group_id)) < gold:
            await matcher.finish(at(event.user_id) + f"金币不足..该功能需要{gold}金币..")
        await BagUser.spend_gold(event.user_id, event.group_id, gold)
        await UserShopGoldLog.add_shop_log(event.user_id, event.group_id, 2, matcher.plugin_name, gold, 1)

    return Depends(dependency)


