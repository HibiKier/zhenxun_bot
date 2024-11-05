from nonebot.rule import Rule
from nonebot.adapters import Bot, Event
from nonebot_plugin_uninfo import Uninfo
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna.uniseg.tools import reply_fetch
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna

from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils
from zhenxun.configs.utils import PluginExtraData
from zhenxun.utils.manager.message_manager import MessageManager

__plugin_meta__ = PluginMetadata(
    name="消息撤回",
    description="撤回自己触发的消息撤回，不允许撤回其他人触发消息的撤回哦",
    usage="""
    引用消息 撤回
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="其他").dict(),
)


def reply_check() -> Rule:
    """
    检查是否存在回复消息

    返回:
        Rule: Rule
    """

    async def _rule(bot: Bot, event: Event, session: Uninfo):
        if event.get_type() == "message":
            return (
                bool(await reply_fetch(event, bot))
                and PlatformUtils.get_platform(session) == "qq"
            )
        return False

    return Rule(_rule)


_matcher = on_alconna(Alconna("撤回"), priority=5, block=True, rule=reply_check())


@_matcher.handle()
async def _(bot: Bot, event: Event, session: Uninfo, arparma: Arparma):
    if reply := await reply_fetch(event, bot):
        if (
            MessageManager.check(session.user.id, reply.id)
            or session.user.id in bot.config.superusers
        ):
            try:
                await bot.delete_msg(message_id=reply.id)
                logger.info("撤回消息", arparma.header_result, session=session)
            except Exception:
                await MessageUtils.build_message("撤回失败，可能消息已过期...").send()
        else:
            await MessageUtils.build_message(
                "权限不足，不是你触发的消息不要胡乱撤回哦..."
            ).send()
