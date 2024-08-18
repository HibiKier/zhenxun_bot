from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services import logger
from zhenxun.utils.enum import PluginType

from ._model import WordBank
from ._rule import check

__plugin_meta__ = PluginMetadata(
    name="词库问答回复操作",
    description="",
    usage="""""",
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.DEPENDANT
    ).dict(),
)

_matcher = on_message(priority=6, block=True, rule=check)


@_matcher.handle()
async def _(session: EventSession, state: T_State):
    if problem := state.get("problem"):
        gid = session.id3 or session.id2
        if result := await WordBank.get_answer(gid, problem):
            await result.send()
            logger.info(f"触发词条 {problem}", "词条检测", session=session)
