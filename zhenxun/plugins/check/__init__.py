from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from .data_source import Check

__plugin_meta__ = PluginMetadata(
    name="服务器自我检查",
    description="查看服务器当前状态",
    usage="""
    查看服务器当前状态
    指令:
        自检
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.SUPERUSER
    ).dict(),
)


check = Check()


_matcher = on_alconna(
    Alconna("自检"), rule=to_me(), permission=SUPERUSER, block=True, priority=1
)


@_matcher.handle()
async def _(session: EventSession, arparma: Arparma):
    image = await check.show()
    await MessageUtils.build_message(image).send()
    logger.info("自检", arparma.header_result, session=session)
