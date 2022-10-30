from typing import List, Callable, Optional, Union

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Depends
from models.user_shop_gold_log import UserShopGoldLog
from models.bag_user import BagUser
from utils.message_builder import at
from utils.utils import get_message_at, get_message_face, get_message_img, get_message_text
from configs.config import Config


def CostGold(gold: int):
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


def GetConfig(module: Optional[str] = None, config: str = "", default_value: Optional[str] = None, prompt: Optional[str] = None):
    """
    说明:
        获取配置项
    参数:
        :param module: 模块名，为空时默认使用当前插件模块名
        :param config: 配置项名称
        :param default_value: 默认值
        :param prompt: 为空时提示
    """
    async def dependency(matcher: Matcher):
        module_ = module or matcher.plugin_name
        value = Config.get_config(module_, config, default_value)
        if value is None:
            await matcher.finish(prompt or f"配置项 {config} 未填写！")
        return value

    return Depends(dependency)


def CheckConfig(module: Optional[str] = None, config: Union[str, List[str]] = "", prompt: Optional[str] = None):
    """
    说明:
        检测配置项在配置文件中是否填写
    参数:
        :param module: 模块名，为空时默认使用当前插件模块名
        :param config: 需要检查的配置项名称
        :param prompt: 为空时提示
    """
    async def dependency(matcher: Matcher):
        module_ = module or matcher.plugin_name
        config_list = [config] if isinstance(config, str) else config
        for c in config_list:
            if Config.get_config(module_, c) is None:
                await matcher.finish(prompt or f"配置项 {c} 未填写！")

    return Depends(dependency)


async def _match(matcher: Matcher, event: MessageEvent, msg: Optional[str], func: Callable, contain_reply: bool):
    _list = func(event.message)
    if event.reply and contain_reply:
        _list = func(event.reply.message)
    if not _list and msg:
        await matcher.finish(msg)
    return _list


def ImageList(msg: Optional[str] = None, contain_reply: bool = True) -> List[str]:
    """
    说明:
        获取图片列表（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_img, contain_reply)

    return Depends(dependency)


def AtList(msg: Optional[str] = None, contain_reply: bool = True) -> List[str]:
    """
    说明:
        获取at列表（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_at, contain_reply)

    return Depends(dependency)


def FaceList(msg: Optional[str] = None, contain_reply: bool = True) -> List[str]:
    """
    说明:
        获取face列表（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_face, contain_reply)

    return Depends(dependency)


def PlaintText(msg: Optional[str] = None, contain_reply: bool = True) -> str:
    """
    说明:
        获取纯文本且（包括回复时），含有msg时不能为空，为空时提示并结束事件
    参数:
        :param msg: 提示文本
        :param contain_reply: 包含回复内容
    """
    async def dependency(matcher: Matcher, event: MessageEvent):
        return await _match(matcher, event, msg, get_message_text, contain_reply)

    return Depends(dependency)
