from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, UniMessage, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from .data_source import get_epic_free

__plugin_meta__ = PluginMetadata(
    name="epic免费游戏",
    description="可以不玩，不能没有，每日白嫖",
    usage="""
    epic
    """.strip(),
    extra=PluginExtraData(
        author="AkashiCoin",
        version="0.1",
    ).dict(),
)

_matcher = on_alconna(Alconna("epic"), priority=5, block=True)


@_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma):
    gid = session.id3 or session.id2
    type_ = "Group" if gid else "Private"
    msg_list, code = await get_epic_free(bot, type_)
    if code == 404 and isinstance(msg_list, str):
        await MessageUtils.build_message(msg_list).finish()
    elif isinstance(bot, (v11Bot, v12Bot)) and isinstance(msg_list, list):
        await bot.send_group_forward_msg(group_id=gid, messages=msg_list)
    elif isinstance(msg_list, UniMessage):
        await msg_list.send()
    logger.info(f"获取epic免费游戏", arparma.header_result, session=session)
