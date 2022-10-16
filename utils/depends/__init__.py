from typing import List, Callable, Optional

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Depends
from models.user_shop_gold_log import UserShopGoldLog
from models.bag_user import BagUser
from utils.message_builder import at
from utils.utils import get_message_at, get_message_face, get_message_img, get_message_text


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


async def _match(matcher: Matcher, event: MessageEvent, msg: Optional[str], func: Callable):
    _list = func(event.message)
    if not _list and msg:
        await matcher.finish(msg)
    return _list


def ImageList(msg: Optional[str] = None) -> List[str]:
    """
    说明:
        获取图片列表，含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_img)

    return Depends(dependency)


def AtList(msg: Optional[str] = None) -> List[str]:
    """
    说明:
        获取at列表，含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_at)

    return Depends(dependency)


def FaceList(msg: Optional[str] = None) -> List[str]:
    """
    说明:
        获取face列表，含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_face)

    return Depends(dependency)


def PlaintText(msg: Optional[str] = None) -> str:
    """
    说明:
        获取纯文本且，含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_text)

    return Depends(dependency)
