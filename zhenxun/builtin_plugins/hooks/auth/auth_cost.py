from nonebot.exception import IgnoredException
from nonebot_plugin_uninfo import Uninfo

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.user_console import UserConsole
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils


async def auth_cost(user: UserConsole, plugin: PluginInfo, session: Uninfo) -> int:
    """检测是否满足金币条件

    参数:
        plugin: PluginInfo
        session: Uninfo

    返回:
        int: 需要消耗的金币
    """
    if user.gold < plugin.cost_gold:
        """插件消耗金币不足"""
        try:
            await MessageUtils.build_message(
                f"金币不足..该功能需要{plugin.cost_gold}金币.."
            ).send()
        except Exception as e:
            logger.error("auth_cost 发送消息失败", "AuthChecker", session=session, e=e)
        logger.debug(
            f"{plugin.name}({plugin.module}) 金币限制.."
            f"该功能需要{plugin.cost_gold}金币..",
            "AuthChecker",
            session=session,
        )
        raise IgnoredException(f"{plugin.name}({plugin.module}) 金币限制...")
    return plugin.cost_gold
